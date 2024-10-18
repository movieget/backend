from fastapi import APIRouter, FastAPI
from core.configs.database_config import database_initialize

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")


app.include_router(api_router)
database_initialize(app)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
