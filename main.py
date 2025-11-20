from fastapi import UploadFile, FastAPI
import httpx


app = FastAPI(title="API Gateway")


S3_SERVICE = "http://localhost:8000"

@app.get("/send")
async def send_file():
    with open("pyproject.toml", "rb") as f:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{S3_SERVICE}/courses/upload_file",
                headers={"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwicm9sZSI6ImFkbWluIn0.vYDiTa3iYSO-KGYfvn9jOrjEJIyd70-sui3AqkDxXTs"},
                files={"file": ("pyproject.toml", f.read(), "text/plain")}
            )
            print(r.json())
