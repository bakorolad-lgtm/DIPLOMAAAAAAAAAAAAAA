from fastapi import FastAPI, Request
import httpx

from src.schemas import CreateQuizSchema, QuizAnswerSchema

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


@app.get("/courses")
async def get_courses():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COURSE_SERVICE}/courses")
        return r.json()


@app.get("/quiz")
async def get_quizzes():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{QUIZ_SERVICE}/quiz")
        return r.json()

@app.post("/quiz")
async def create_quizzes(quiz: CreateQuizSchema):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz", json=quiz.model_dump())
        return r.json()


@app.post("/quiz/answer")
async def create_quizzes(quiz_answer: QuizAnswerSchema):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz/answer", json=quiz_answer.model_dump())
        return r.json()
