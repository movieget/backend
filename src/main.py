from fastapi import APIRouter, FastAPI
from tortoise import Tortoise
from core.configs.database_config import database_initialize, TORTOISE_ORM

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")
database_initialize(app)

app.include_router(api_router)


# @app.on_event("startup")
# async def startup_event():
#     await database_initialize(app)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8080)
