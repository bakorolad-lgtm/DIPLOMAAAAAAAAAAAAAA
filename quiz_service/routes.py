from fastapi import APIRouter
from .database import async_session
from .models import Quiz
from sqlalchemy.future import select

router = APIRouter(prefix="/quiz")

@router.get("/")
async def get_quizzes():
    async with async_session() as session:
        result = await session.execute(select(Quiz))
        return result.scalars().all()

@router.post("/")
async def create_quiz(title: str, questions: list):
    async with async_session() as session:
        quiz = Quiz(title=title, questions=questions)
        session.add(quiz)
        await session.commit()
        return {"message": "Quiz created"}
