from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.future import select
from .database import async_session
from .models import Course
import httpx

router = APIRouter(prefix="/courses")

AUTH_SERVICE_URL = "http://user-service:8000"

async def get_current_user(Authorization: str = Header(...)):
    """Получаем текущего пользователя через user_service"""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{AUTH_SERVICE_URL}/auth/me", headers={"Authorization": Authorization})
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return res.json()

def require_role(roles: list):
    async def _require(user = Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return _require

@router.get("/")
async def list_courses(user=Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Course))
        return result.scalars().all()

@router.post("/")
async def create_course(
    title: str,
    description: str,
    user=Depends(require_role(["teacher", "admin"]))
):
    async with async_session() as session:
        c = Course(title=title, description=description, author_id=user["id"])
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return {"id": c.id, "title": c.title}
