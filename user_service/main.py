from fastapi import FastAPI
from . import models, database, routes

app = FastAPI(title="Auth Service")

@app.on_startup("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app.include_router(routes.router)
