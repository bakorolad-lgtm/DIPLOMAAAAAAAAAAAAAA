from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from .database import async_session
from .models import User
from .utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(email: str, password: str, role: str = "student"):
    async with async_session() as session:
        # проверка на существующий
        result = await session.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        user = User(email=email, password=hash_password(password), role=role)
        session.add(user)
        await session.commit()
        return {"message": "registered"}

@router.post("/login")
async def login(email: str, password: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"id": user.id, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
