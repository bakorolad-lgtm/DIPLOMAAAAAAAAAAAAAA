from fastapi import APIRouter, Depends
from src.utils import role_required
from src.schemas import CreateCourseSchema
from src.clients.users import UserClient
from src.database import async_session
from src.models import Course
from sqlalchemy.future import select

router = APIRouter(prefix="/courses")

@router.get("")
async def get_courses():
    async with async_session() as session:
        result = await session.execute(select(Course))
        return result.scalars().all()

@router.post("", dependencies=[Depends(role_required("admin"))])
async def create_course(course: CreateCourseSchema, author: dict = Depends(UserClient().get_user_by_token)):
    async with async_session() as session:
        course = Course(title=course.title, description=course.description, author_id=author["id"])
        session.add(course)
        await session.commit()
        return {"message": "Course created"}
