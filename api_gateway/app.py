from fastapi import FastAPI, Request
import httpx

app = FastAPI(title="API Gateway")

AUTH_SERVICE = "http://auth-service:8000"
COURSE_SERVICE = "http://course-service:8000"
QUIZ_SERVICE = "http://quiz-service:8000"


@app.post("/auth/{path:path}")
async def proxy_auth(path: str, request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AUTH_SERVICE}/auth/{path}", json=data)
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
