from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from src.models import User
from src.database import async_session
from src.utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(email: str, password: str):
    async with async_session() as session:
        user = User(email=email, password=hash_password(password))
        session.add(user)
        await session.commit()
        return {"message": "User registered"}

@router.post("/login")
async def login(email: str, password: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_token(user.id, user.role)
        return {"token": token}
