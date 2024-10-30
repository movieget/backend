from fastapi import APIRouter
from src.app.api.v1_routes import (
    user,
    book_option_router,
    confirm_router,
    seats_router,
    cancel_router,
    payment_router,
    payment_result_router,
    favorite,
    movie_routor,
)


api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(book_option_router.router, prefix="/books", tags=["Booking Options"])
api_router.include_router(seats_router.router, prefix="/seats", tags=["Screen Seats"])
api_router.include_router(payment_result_router.router, prefix="/payment", tags=["Payment Result"])
api_router.include_router(confirm_router.router, prefix="/mypage", tags=["Mypage Booking"])
api_router.include_router(cancel_router.router, prefix="/mypage", tags=["Mypage Booking"])
api_router.include_router(payment_router.router, prefix="/payment", tags=["Payment"])
api_router.include_router(favorite.router, prefix="/favorites", tags=["Favorites"])
api_router.include_router(movie_routor.router, prefix="/movies", tags=["Movies"])

