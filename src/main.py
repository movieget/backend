from fastapi import APIRouter, FastAPI

from src.core.database.connection import database_initialize
from src.app.api.root_routes import api_router

app = FastAPI()
app.include_router(api_router)

api_router = APIRouter(prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    await database_initialize(app)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8080)
