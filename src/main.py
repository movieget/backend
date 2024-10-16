from fastapi import APIRouter, FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import TORTOISE_ORM

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")


app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome"}


# Tortoise ORM 초기화
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
