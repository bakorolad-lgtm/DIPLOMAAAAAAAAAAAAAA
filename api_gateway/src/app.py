from fastapi import HTTPException, Header
from fastapi import FastAPI, Request
import httpx

from src.schemas import CreateCourseSchema, CreateQuizSchema, GetCourseSchema, GetQuizCheckAnswers, GetQuizSchema, QuizAnswerSchema

app = FastAPI(title="API Gateway", root_path="/api")

AUTH_SERVICE = "http://auth-service:8000"
COURSE_SERVICE = "http://course-service:8000"
QUIZ_SERVICE = "http://quiz-service:8000"


@app.post("/auth/register")
async def register(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_SERVICE}/auth/register", params=data)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()

@app.post("/auth/login")
async def login(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_SERVICE}/auth/login", params=data)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.get("/auth")
async def get_users(request: Request, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{AUTH_SERVICE}/auth", headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.patch("/auth/{user_id}/make_admin")
async def make_user_user(user_id: int, role: str, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{AUTH_SERVICE}/auth/{user_id}", params={"role": role}, headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.post("/courses")
async def create_course(course: CreateCourseSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{COURSE_SERVICE}/courses", headers=headers, json=course.model_dump())
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.get("/courses/{course_id}", response_model=GetCourseSchema)
async def get_course(course_id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COURSE_SERVICE}/courses/{course_id}")
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()

@app.get("/courses", response_model=list[GetCourseSchema])
async def get_courses():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{COURSE_SERVICE}/courses")
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.get("/quiz", response_model=list[GetQuizSchema])
async def get_quizzes():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{QUIZ_SERVICE}/quiz")
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        response = r.json()
        print(response)
        print(type(response))
        result = []
        for quiz in response:
            for question in quiz["questions"]:
                question.pop("correct_answer")

            result.append(quiz)

        return response


@app.post("/quiz")
async def create_quizzes(quiz: CreateQuizSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz", json=quiz.model_dump(), headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.post("/quiz/answer")
async def create_quizzes(quiz_answer: QuizAnswerSchema, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{QUIZ_SERVICE}/quiz/answer", json=quiz_answer.model_dump(), headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()


@app.get("/quiz/user/answers")
async def get_user_answers(user_id: int, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{QUIZ_SERVICE}/quiz/user/answers", params={"user_id": user_id}, headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()

@app.get("/quiz/check_answers", response_model=list[GetQuizCheckAnswers])
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
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()

@app.delete("/quiz/{quiz_id}")
async def delete_quiz(quiz_id: int, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{QUIZ_SERVICE}/quiz/{quiz_id}", headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()

@app.delete("/courses/{course_id}")
async def delete_course(course_id: int, token: str = Header(alias="Authorization")):
    headers = {}
    if token:
        headers = {"Authorization": token}
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{COURSE_SERVICE}/courses/{course_id}", headers=headers)
        if r.status_code != 200:
            print(r.json())
            raise HTTPException(status_code=r.status_code, detail="Error")
        return r.json()
