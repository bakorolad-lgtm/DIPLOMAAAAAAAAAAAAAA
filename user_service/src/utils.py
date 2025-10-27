import bcrypt
import jwt

SECRET_KEY = "SECRET"

def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode()


def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_token(user_id: int, role: str):
    return jwt.encode({"id": user_id, "role": role}, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):    
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
