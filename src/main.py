from fastapi import APIRouter, FastAPI
import sys
from pathlib import Path
from src.app.api.root import api_router as root_router
from src.core.database.connection import database_initialize


# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

app = FastAPI()
app.include_router(root_router)
api_router = APIRouter(prefix="/api/v1")

# 라우터 연결
api_router.include_router(root_router)

database_initialize(app)


@app.on_event("startup")
async def startup_event():
    await database_initialize(app)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8000)
