from fastapi import APIRouter
from src.app.api.v1_routes import (
    user, book_option_router, confirm_router, seats_router,
    cancel_router,payment_router, payment_result_router,
)
from fastapi import FastAPI


api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(book_option_router.router, prefix="/", tags=["Booking Options"])
api_router.include_router(seats_router.router, prefix="/", tags=["Screen Seats"])
api_router.include_router(payment_result_router.router, prefix="/", tags=["Payment Result"])
api_router.include_router(confirm_router.router, prefix="/", tags=["Mypage Booking"])
api_router.include_router(cancel_router.router, prefix="/", tags=["Mypage Booking"])
api_router.include_router(payment_router.router, prefix="/", tags=["Payment"])
