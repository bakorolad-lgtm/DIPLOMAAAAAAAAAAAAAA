from fastapi import FastAPI
from src.database import engine
from src.models import Base
from src.routes import router

app = FastAPI(title="Auth Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)
