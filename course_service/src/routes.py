from fastapi import APIRouter
from src.database import async_session
from src.models import Course
from sqlalchemy.future import select

router = APIRouter(prefix="/courses")

@router.get("/")
async def get_courses():
    async with async_session() as session:
        result = await session.execute(select(Course))
        return result.scalars().all()

@router.post("/")
async def create_course(title: str, description: str, author_id: int):
    async with async_session() as session:
        course = Course(title=title, description=description, author_id=author_id)
        session.add(course)
        await session.commit()
        return {"message": "Course created"}
