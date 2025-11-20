from fastapi import APIRouter, Depends
from sqlalchemy import delete
from src.utils import role_required
from src.schemas import CreateCourseSchema
from src.clients.users import UserClient
from src.database import async_session
from src.models import Course, CourseBlock
from sqlalchemy.future import select

router = APIRouter(prefix="/courses")

@router.get("")
async def get_courses():
    async with async_session() as session:
        result = await session.execute(select(Course))
        response = []
        for course in result.scalars().all():
            response.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "author": await UserClient().get_user(course.author_id)
            })
        return response


@router.get("/{course_id}")
async def get_courses(course_id: int):
    async with async_session() as session:
        course = (await session.execute(select(Course).where(Course.id == course_id))).scalar()
        response = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "author": await UserClient().get_user(course.author_id)
        }
        return response

@router.post("", dependencies=[Depends(role_required("admin"))])
async def create_course(course: CreateCourseSchema, author: dict = Depends(UserClient().get_user_by_token)):
    async with async_session() as session:
        course_entity = Course(title=course.title, author_id=author["id"])
        session.add(course_entity)
        await session.commit()
        await session.refresh(course_entity)
        for index, block in enumerate(course.blocks):
            block.course_id = course_entity.id
            block.elem_number = index
            session.add(CourseBlock(**block.model_dump()))

        await session.commit()

        return {
            "id": course_entity.id,
            "title": course_entity.title,
            "author": await UserClient().get_user(author["id"]),
            "block": sorted(course.blocks, key=lambda block: block.elem_number)
        }

@router.delete("/{course_id}", dependencies=[Depends(role_required("admin"))])
async def delete_course(course_id: int):
    async with async_session() as session:
        await session.execute(delete(Course).where(Course.id == course_id))
        await session.commit()
