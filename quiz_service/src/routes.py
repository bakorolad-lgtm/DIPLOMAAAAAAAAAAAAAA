from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from src.clients.users import UserClient
from src.utils import role_required, self_or_admin
from src.schemas import CreateQuizSchema, QuizAnswerSchema
from src.database import async_session
from src.models import Quiz, QuizAnswers
from sqlalchemy.future import select

router = APIRouter(prefix="/quiz")

@router.get("")
async def get_quizzes():
    async with async_session() as session:
        result = await session.execute(select(Quiz))
        return result.scalars().all()

@router.post("", dependencies=[Depends(role_required("admin"))])
async def create_quiz(quiz: CreateQuizSchema):
    async with async_session() as session:
        quiz = Quiz(
            title=quiz.title,
            questions=[question.model_dump() for question in quiz.questions]
        )
        session.add(quiz)
        await session.commit()
        return {"message": "Quiz created"}


@router.post("/answer")
async def answer_quiz(quiz_answer: QuizAnswerSchema, user: dict = Depends(UserClient().get_user_by_token)):
    async with async_session() as session:
        quiz = await session.get(Quiz, quiz_answer.quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        quiz_answers = (await session.execute(
            select(QuizAnswers)
            .where(
                QuizAnswers.quiz_id == quiz_answer.quiz_id,
                QuizAnswers.user_id == user["id"]
            )
        )).scalars()

        if quiz_answers.first():
            raise HTTPException(status_code=400, detail="You have already answered this quiz")

        for answer in quiz_answer.answers:
            print(quiz.questions)
            question_id_map = {question["id"]: question for question in quiz.questions}
            if answer.question_id not in question_id_map:
                raise HTTPException(status_code=400, detail="Invalid question id")
            if answer.answer not in question_id_map[answer.question_id]["answers"]:
                raise HTTPException(status_code=400, detail="Invalid answer")

            quiz_answer = QuizAnswers(
                quiz_id=quiz_answer.quiz_id,
                question_id=answer.question_id,
                user_id=user["id"],
                answer=answer.answer
            )
            session.add(quiz_answer)
        await session.commit()
        return {"message": "Quiz answered"}


@router.get("/check_answers")
async def check_quiz_answers(quiz_id: int, user: int = Depends(self_or_admin), user_id: str | None = None):
    quiz_user_id = None
    if user["role"] == "admin":
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not provided")

        user = await UserClient().get_user(user_id)
        quiz_user_id = user["id"]
    else:
        quiz_user_id = user["id"]

    async with async_session() as session:
        answers = (await session.execute(
            select(QuizAnswers)
            .where(
                QuizAnswers.quiz_id == quiz_id,
                QuizAnswers.user_id == quiz_user_id
            )
        )).scalars()
        quiz = await session.get(Quiz, quiz_id)
        result = []
        questions_map = {question["id"]: question for question in quiz.questions}
        for answer in answers:
            if questions_map[answer.question_id]["correct_answer"] == answer.answer:
                result.append({
                    "title": questions_map[answer.question_id]["title"],
                    "answers": questions_map[answer.question_id]["answers"],
                    "is_correct": True
                })
            else:
                result.append({
                    "title": questions_map[answer.question_id]["title"],
                    "answers": questions_map[answer.question_id]["answers"],
                    "is_correct": False
                })

        return result
