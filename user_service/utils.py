from passlib.hash import bcrypt
import jwt

SECRET_KEY = "SECRET"

def hash_password(password: str):
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str):
    return bcrypt.verify(password, hashed)

def create_token(user_id: int, role: str):
    return jwt.encode({"id": user_id, "role": role}, SECRET_KEY, algorithm="HS256")
