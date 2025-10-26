from fastapi import APIRouter, Depends, HTTPException
from .models import Course
from .database import async_session
from sqlalchemy.future import select
from user_service.deps import require_role, get_current_user

router = APIRouter(prefix="/courses")

@router.get("/")
async def list_courses():
    async with async_session() as session:
        r = await session.execute(select(Course))
        return r.scalars().all()

@router.post("/")
async def create_course(title: str, description: str, user = Depends(require_role(["teacher", "admin"]))):
    async with async_session() as session:
        c = Course(title=title, description=description, author_id=user.id)
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return {"id": c.id, "title": c.title}
