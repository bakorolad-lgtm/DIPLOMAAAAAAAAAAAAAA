# api_gateway/src/app.py
from fastapi import FastAPI, Request, Response, Header
import httpx
import os
from src.schemas import CreateQuizSchema, QuizAnswerSchema
import json

app = FastAPI(title="API Gateway")

AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://auth-service:8000")
COURSE_SERVICE = os.getenv("COURSE_SERVICE", "http://course-service:8000")
QUIZ_SERVICE = os.getenv("QUIZ_SERVICE", "http://quiz-service:8000")

# Generic proxy helper that forwards Authorization header and body


async def forward_request(method: str, url: str, request: Request, auth: str | None = None):
    # Передаём все заголовки
    headers = dict(request.headers)
    if auth:
        headers["Authorization"] = auth

    # Извлекаем query параметры
    query_params = dict(request.query_params)

    # Извлекаем тело запроса
    raw_body = await request.body()
    content_type = request.headers.get("content-type", "")

    async with httpx.AsyncClient() as client:
        if "application/json" in content_type and raw_body:
            try:
                json_body = json.loads(raw_body)
            except json.JSONDecodeError:
                json_body = None
        else:
            json_body = None

        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=query_params,
            json=json_body,
            content=None if json_body else raw_body,
            timeout=30.0,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers={"content-type": response.headers.get("content-type", "application/json")},
    )


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
