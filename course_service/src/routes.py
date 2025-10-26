from fastapi import APIRouter, Depends, HTTPException
from .models import Course
from .database import async_session
from sqlalchemy.future import select
import httpx
from fastapi import Depends, HTTPException, Header

router = APIRouter(prefix="/courses")

AUTH_SERVICE_URL = "http://user-service:8000"

async def get_current_user(token: str = Header(...)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/auth/me", headers={"Authorization": token})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()
    
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
