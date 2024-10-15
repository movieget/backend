from fastapi import APIRouter, FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import TORTOISE_ORM

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router()

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


# 애플리케이션 시작 시 실행될 이벤트
@app.on_event("startup")
async def startup_event():
    print("Application is starting up...")


# 애플리케이션 종료 시 실행될 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
