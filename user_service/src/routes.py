from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.future import select
from pydantic import BaseModel
from jose import JWTError, jwt
import os

from .database import async_session
from .models import User
from .utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth")

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(email: str, password: str, role: str = "student"):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        user = User(email=email, password=hash_password(password), role=role)
        session.add(user)
        await session.commit()
        return {"message": "registered"}

@router.post("/login")
async def login(data: LoginRequest):
    email = data.email
    password = data.password
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"id": user.id, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

@router.get("/me")
async def get_current_user(Authorization: str = Header(...)):
    """Проверяет токен и возвращает данные пользователя"""
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = Authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"id": payload["id"], "role": payload["role"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
