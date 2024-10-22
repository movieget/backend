from fastapi import APIRouter, FastAPI
from tortoise import Tortoise

from src.app.api.v1_routes import book_router, book_quantity_router, seat_router, confirmation_router, \
    available_book_router
from src.core.database.connection import database_initialize, TORTOISE_ORM

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")
database_initialize(app)

# 라우터 연결
api_router.include_router(book_router.router, prefix="/books", tags=["Reservation Options"])
api_router.include_router(book_quantity_router.router, prefix="/book/quantity", tags=["Reservation Quantity"])
api_router.include_router(seat_router.router, prefix="/seats", tags=["Seat Selection"])
api_router.include_router(confirmation_router.router, prefix="/confirmation", tags=["Reservation Confirmation"])
api_router.include_router(available_book_router.router, prefix="/books/available", tags=["Reservation Quantity"])

# 라우터를 FastAPI 애플리케이션에 등록
app.include_router(api_router)

database_initialize(app)





@app.on_event("startup")
async def startup_event():
    await database_initialize(app)


@app.get("/")
async def root():
    return {"message": "Welcome"}
# TODO : 나중에 할 것
# FIXME :
#  NOTE :


if __name__ == "__main__":
    import uvicorn
    import asyncio

    uvicorn.run(app, host="0.0.0.0", port=8080)
