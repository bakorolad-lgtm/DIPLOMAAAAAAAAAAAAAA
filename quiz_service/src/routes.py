# quiz_service/src/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.future import select
from .database import async_session
from .models import Quiz, Attempt
from typing import Dict, Any
import os
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/quiz")

# Try to reuse user_service.deps if present (monorepo mode).
# Otherwise use a lightweight local JWT check (suitable for separate containers).
try:
    from user_service.deps import require_role, get_current_user  # type: ignore
except Exception:
    # local lightweight auth fallback
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
    ALGORITHM = "HS256"
    auth_scheme = HTTPBearer()

    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        # payload must contain id and role
        uid = payload.get("id")
        role = payload.get("role")
        if uid is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        # We return a lightweight user-like object
        class U:
            def __init__(self, id, role):
                self.id = id
                self.role = role
        return U(uid, role)

    def require_role(roles):
        async def _require(user = Depends(get_current_user)):
            if user.role not in roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return user
        return _require


# CREATE QUIZ — только admin
@router.post("/")
async def create_quiz(payload: Dict[str, Any], admin = Depends(require_role(["admin"]))):
    """
    payload example:
    {
      "title": "Test 1",
      "questions": [
        {"id": 1, "text": "Q1", "options": ["A","B","C"], "correct": 0},
        {"id": 2, "text": "Q2", "options": ["X","Y","Z"], "correct": 2}
      ]
    }
    """
    if "title" not in payload or "questions" not in payload:
        raise HTTPException(status_code=400, detail="payload must contain title and questions")
    # Basic validation: every question must have 'id', 'text', 'options', 'correct'
    for q in payload["questions"]:
        if not isinstance(q, dict) or "id" not in q or "text" not in q or "options" not in q or "correct" not in q:
            raise HTTPException(status_code=400, detail="Each question must include id, text, options and correct")
    async with async_session() as session:
        quiz = Quiz(title=payload["title"], questions=payload["questions"])
        session.add(quiz)
        await session.commit()
        await session.refresh(quiz)
        return {"id": quiz.id, "title": quiz.title}


# GET QUIZ — returns quiz without revealing 'correct' field
@router.get("/{quiz_id}")
async def get_quiz(quiz_id: int, user = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        # do not expose 'correct' to regular users
        questions = []
        for q in quiz.questions:
            q_copy = dict(q)
            if "correct" in q_copy:
                q_copy.pop("correct")
            questions.append(q_copy)
        return {"id": quiz.id, "title": quiz.title, "questions": questions}


# SUBMIT answers and compare
@router.post("/{quiz_id}/submit")
async def submit_quiz(quiz_id: int, answers: Dict[str, Any], user = Depends(get_current_user)):
    """
    answers example: { "1": 0, "2": 2 } where keys are question 'id' values (strings typical in JSON)
    """
    async with async_session() as session:
        qres = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = qres.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        # Build map question_id -> question
        qmap = {}
        for q in quiz.questions:
            qmap[str(q.get("id"))] = q

        max_score = len(qmap)
        score = 0
        per_question = []

        # Accept both string keys and int keys; normalize to str
        norm_answers = {str(k): v for k, v in answers.items()}

        for qid, qobj in qmap.items():
            correct = qobj.get("correct")
            user_choice = norm_answers.get(qid)
            is_correct = (user_choice is not None) and (user_choice == correct)
            if is_correct:
                score += 1
            per_question.append({
                "question_id": qid,
                "correct": correct,
                "user_choice": user_choice,
                "is_correct": is_correct,
            })

        # save attempt record
        attempt = Attempt(quiz_id=quiz_id, user_id=user.id, answers=norm_answers, score=score, max_score=max_score)
        session.add(attempt)
        await session.commit()
        await session.refresh(attempt)

        return {
            "attempt_id": attempt.id,
            "score": score,
            "max_score": max_score,
            "per_question": per_question
        }


# Compare existing attempt (only owner or admin can view)
@router.get("/{quiz_id}/attempts/{attempt_id}/compare")
async def compare_attempt(quiz_id: int, attempt_id: int, user = Depends(get_current_user)):
    async with async_session() as session:
        res = await session.execute(select(Attempt).where(Attempt.id == attempt_id, Attempt.quiz_id == quiz_id))
        attempt = res.scalar_one_or_none()
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")

        # allow only owner or admin to view full compare
        if attempt.user_id != user.id and getattr(user, "role", None) != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

        # Fetch quiz to get correct answers
        qres = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = qres.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        qmap = {str(q.get("id")): q for q in quiz.questions}
        per_question = []
        # attempt.answers expected as dict with string keys
        stored_answers = {str(k): v for k, v in attempt.answers.items()}
        for qid, qobj in qmap.items():
            correct = qobj.get("correct")
            user_choice = stored_answers.get(qid)
            per_question.append({
                "question_id": qid,
                "correct": correct,
                "user_choice": user_choice,
                "is_correct": user_choice == correct
            })

        return {
            "attempt_id": attempt.id,
            "score": attempt.score,
            "max_score": attempt.max_score,
            "per_question": per_question
        }
