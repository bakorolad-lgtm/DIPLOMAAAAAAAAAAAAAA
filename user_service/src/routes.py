from fastapi import APIRouter, HTTPException, Depends, Header
import jwt
from sqlalchemy.future import select
from src.models import User
from src.database import async_session
from src.utils import decode_token, hash_password, role_required, verify_password, create_token

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
        print(email)
        print(password)
        print(verify_password(password, user.password))
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_token(user.id, user.role)
        return {"token": token, "role": user.role}


@router.get("/me")
async def get_me(token: str = Header(alias="Authorization")):
    try:
        payload = decode_token(token)
        user_id = payload.get("id")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": user.id, "email": user.email, "role": user.role}


@router.get("", dependencies=[Depends(role_required("admin"))])
async def get_users():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.role == "student"))
        users = result.scalars().all()
        return [{"id": user.id, "email": user.email, "role": user.role} for user in users]


@router.get("/{user_id}")
async def get_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": user.id, "email": user.email, "role": user.role}


@router.patch("/{user_id}")
async def update_user(user_id: int, role: str, dependencies=[Depends(role_required("admin"))]):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = role
        await session.commit()
        return {"id": user.id, "email": user.email, "role": user.role}
