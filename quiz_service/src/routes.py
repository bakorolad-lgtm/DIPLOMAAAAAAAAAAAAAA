from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from .database import async_session
from .models import Quiz, Attempt
from user_service.deps import require_role, get_current_user  # предположим, что user_service dependency импортируем или дублируем
from typing import Dict

router = APIRouter(prefix="/quiz")

# CREATE QUIZ — только admin
@router.post("/")
async def create_quiz(payload: dict, admin = Depends(require_role(["admin"]))):
    """
    payload example:
    {
      "title": "Test 1",
      "questions": [
        {"id": 1, "text": "Q1", "options": ["A","B","C"], "correct": 0},
        {"id": 2, "text": "Q2", "options": ["A","B","C"], "correct": 2}
      ]
    }
    """
    async with async_session() as session:
        quiz = Quiz(title=payload["title"], questions=payload["questions"])
        session.add(quiz)
        await session.commit()
        await session.refresh(quiz)
        return {"id": quiz.id, "title": quiz.title}

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: int, user = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        # не возвращаем поле correct для каждого вопроса студенту
        questions = []
        for q in quiz.questions:
            q_copy = dict(q)
            if "correct" in q_copy:
                q_copy.pop("correct")
            questions.append(q_copy)
        return {"id": quiz.id, "title": quiz.title, "questions": questions}

# SUBMIT answers and compare
@router.post("/{quiz_id}/submit")
async def submit_quiz(quiz_id: int, answers: Dict[int, int], user = Depends(get_current_user)):
    """
    answers example: { "1": 0, "2": 2 } where keys are question 'id' values
    """
    async with async_session() as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = result.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        # Compute score
        max_score = len(quiz.questions)
        score = 0
        per_question = []
        # build map question_id -> question
        qmap = {q.get("id"): q for q in quiz.questions}
        for qid, qobj in qmap.items():
            correct = qobj.get("correct")
            user_choice = answers.get(str(qid)) if isinstance(answers.keys().__iter__().__next__(), str) else answers.get(qid)
            # allow both str and int keys
            # if user_choice is None: treat as wrong (no answer)
            is_correct = (user_choice is not None) and (user_choice == correct)
            if is_correct:
                score += 1
            per_question.append({"question_id": qid, "correct": correct, "user_choice": user_choice, "is_correct": is_correct})

        # save attempt
        attempt = Attempt(quiz_id=quiz_id, user_id=user.id, answers=answers, score=score, max_score=max_score)
        session.add(attempt)
        await session.commit()
        await session.refresh(attempt)

        return {"attempt_id": attempt.id, "score": score, "max_score": max_score, "per_question": per_question}

# Optional: compare endpoint to get a previous attempt and correct answers
@router.get("/{quiz_id}/attempts/{attempt_id}/compare")
async def compare_attempt(quiz_id: int, attempt_id: int, user = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Attempt).where(Attempt.id == attempt_id, Attempt.quiz_id == quiz_id))
        attempt = result.scalar_one_or_none()
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        # also return correct answers from quiz
        qres = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        quiz = qres.scalar_one_or_none()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        qmap = {q.get("id"): q for q in quiz.questions}
        per_question = []
        for qid, qobj in qmap.items():
            correct = qobj.get("correct")
            user_choice = attempt.answers.get(str(qid)) or attempt.answers.get(qid)
            per_question.append({"question_id": qid, "correct": correct, "user_choice": user_choice, "is_correct": user_choice == correct})
        return {"attempt_id": attempt.id, "score": attempt.score, "max_score": attempt.max_score, "per_question": per_question}
