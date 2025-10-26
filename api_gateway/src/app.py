# api_gateway/src/app.py
from fastapi import FastAPI, Request, Response, Header
import httpx
import os
from src.schemas import CreateQuizSchema, QuizAnswerSchema

app = FastAPI(title="API Gateway")

AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://auth-service:8000")
COURSE_SERVICE = os.getenv("COURSE_SERVICE", "http://course-service:8000")
QUIZ_SERVICE = os.getenv("QUIZ_SERVICE", "http://quiz-service:8000")

# Generic proxy helper that forwards Authorization header and body
async def forward_request(method: str, url: str, request: Request, auth: str | None = None):
    headers = {}
    if auth:
        headers["Authorization"] = auth
    # copy other headers if needed (Content-Type is usually enough)
    if "content-type" in request.headers:
        headers["content-type"] = request.headers["content-type"]

    body = await request.body()
    async with httpx.AsyncClient() as client:
        r = await client.request(method, url, headers=headers, content=body, timeout=30.0)
        return Response(content=r.content, status_code=r.status_code, headers=r.headers)

@app.post("/auth/{path:path}")
async def proxy_auth(path: str, request: Request):
    return await forward_request("POST", f"{AUTH_SERVICE}/auth/{path}", request)

@app.get("/courses")
async def get_courses(request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("GET", f"{COURSE_SERVICE}/courses", request, auth=authorization)

@app.post("/courses")
async def post_course(request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("POST", f"{COURSE_SERVICE}/courses", request, auth=authorization)

@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: int, request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("GET", f"{QUIZ_SERVICE}/quiz/{quiz_id}", request, auth=authorization)

@app.post("/quiz")
async def create_quiz(request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("POST", f"{QUIZ_SERVICE}/quiz", request, auth=authorization)

@app.post("/quiz/{quiz_id}/submit")
async def submit_quiz(quiz_id: int, request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("POST", f"{QUIZ_SERVICE}/quiz/{quiz_id}/submit", request, auth=authorization)

@app.get("/quiz/{quiz_id}/attempts/{attempt_id}/compare")
async def compare_attempt(quiz_id: int, attempt_id: int, request: Request, authorization: str | None = Header(default=None)):
    return await forward_request("GET", f"{QUIZ_SERVICE}/quiz/{quiz_id}/attempts/{attempt_id}/compare", request, auth=authorization)
