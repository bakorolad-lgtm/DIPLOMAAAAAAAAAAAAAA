# tests/test_integration.py
import pytest
import httpx

BASE_USER = "http://localhost:8000"       # user_service
BASE_COURSE = "http://localhost:8001"     # course_service
BASE_QUIZ = "http://localhost:8002"       # quiz_service

@pytest.mark.asyncio
async def test_full_flow():
    async with httpx.AsyncClient() as client:
        # 1. Регистрируем администратора
        await client.post(f"{BASE_USER}/auth/register", params={
            "email": "admin@example.com",
            "password": "1234",
            "role": "admin"
        })

        # 2. Логинимся и получаем токен
        res = await client.post(f"{BASE_USER}/auth/login", json={
            "email": "admin@example.com",
            "password": "1234"
        })
        print("LOGIN RESPONSE:", res.status_code, res.text)  # <-- добавили лог
        assert res.status_code == 200, f"Login failed: {res.text}"
        token = res.json()["access_token"]

        # 3. Создаём курс (через course_service)
        res = await client.post(
            f"{BASE_COURSE}/courses/",
            params={"title": "Python 101", "description": "Intro"},
            headers=headers
        )
        assert res.status_code == 200, res.text
        print("✅ Курс создан:", res.json())

        # 4. Создаём опрос (через quiz_service)
        quiz_payload = {
            "title": "Python basics",
            "questions": [
                {"id": 1, "text": "Что делает print?", "options": ["Вывод", "Ввод"], "correct": 0},
                {"id": 2, "text": "Как обозначается список?", "options": ["[]", "{}"], "correct": 0}
            ]
        }
        res = await client.post(f"{BASE_QUIZ}/quiz/", json=quiz_payload, headers=headers)
        assert res.status_code == 200, res.text
        quiz_id = res.json()["id"]
        print("✅ Опрос создан:", res.json())

        # 5. Отправляем ответы
        answers = {"1": 0, "2": 0}
        res = await client.post(f"{BASE_QUIZ}/quiz/{quiz_id}/submit", json=answers, headers=headers)
        print("✅ Отправлены ответы:", res.json())
        assert res.json()["score"] == 2
