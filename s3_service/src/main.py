from fastapi import FastAPI
from src.routes import router

app = FastAPI(title="S3 Service")

app.include_router(router)
