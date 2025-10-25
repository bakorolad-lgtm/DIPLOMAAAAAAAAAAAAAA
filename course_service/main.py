from fastapi import FastAPI
from . import database, models, routes

app = FastAPI(title="Course Service")

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app.include_router(routes.router)
