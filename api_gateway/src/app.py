from fastapi import Header
from fastapi import FastAPI, Request
import httpx

from src.schemas import CreateCourseSchema, CreateQuizSchema, QuizAnswerSchema

app = FastAPI(title="API Gateway")

AUTH_SERVICE = "http://auth-service:8000"
COURSE_SERVICE = "http://course-service:8000"
QUIZ_SERVICE = "http://quiz-service:8000"


@app.post("/auth/{path:path}")
async def proxy_auth(path: str, request: Request):
    data = await request.json()
    print(data)
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_SERVICE}/auth/{path}", params=data)
        return r.json()


@app.post("/courses")
async def create_course(course: CreateCourseSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{COURSE_SERVICE}/courses", headers=headers, json=course.model_dump())
        return r.json()


@app.get("/courses")
async def get_courses():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COURSE_SERVICE}/courses")
        return r.json()


@app.get("/quiz")
async def get_quizzes():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{QUIZ_SERVICE}/quiz")
        response = r.json()
        response.pop("correct_answer")
        return response


@app.post("/quiz")
async def create_quizzes(quiz: CreateQuizSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz", json=quiz.model_dump(), headers=headers)
        return r.json()


@app.post("/quiz/answer")
async def create_quizzes(quiz_answer: QuizAnswerSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz/answer", json=quiz_answer.model_dump(), headers=headers)
        return r.json()


@app.get("/quiz/check_answers")
async def check_quiz_answers(quiz_id: int, token: str = Header(alias="Authorization"), user_id: str | None = None):
    headers = {}
    if token:
        headers = {"Authorization": token}
    params = {
        "quiz_id": quiz_id
    }
    if user_id:
        params["user_id"] = user_id

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{QUIZ_SERVICE}/quiz/check_answers", headers=headers, params=params)
        return r.json()
