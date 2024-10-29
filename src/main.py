from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, tracemalloc
from pathlib import Path

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.app.api.root import api_router as root_router
from src.common.handlers.db_handler import lifespan

tracemalloc.start()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")

# root_router를 api_router에 포함
api_router.include_router(root_router)

# api_router를 app에 포함
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8000)
