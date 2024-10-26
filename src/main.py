from fastapi import APIRouter, FastAPI
import sys
from pathlib import Path
from src.app.api.v1_routes import (
    user, book_option_router, seats_router,
    cancel_router, confirm_router, payment_router,
    payment_result_router,
)
from src.core.database.connection import database_initialize


# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))



app = FastAPI()

api_router = APIRouter(prefix="/api/v1")
# database_initialize(app)
database_initialize(app)
# 라우터 연결
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(book_option_router.router, prefix="/books", tags=["Booking Options"])
api_router.include_router(seats_router.router, prefix="/seats", tags=["Screen Seats"])
api_router.include_router(payment_result_router.router, prefix="/payment", tags=["Payment Results"])
api_router.include_router(confirm_router.router, prefix="/mypage", tags=["Mypage Booking"])
api_router.include_router(cancel_router.router, prefix="/mypage", tags=["Mypage Booking"])
api_router.include_router(payment_router.router, prefix="/payment", tags=["Payment"])

# 라우터를 FastAPI 애플리케이션에 등록
app.include_router(api_router)
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
