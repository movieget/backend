from fastapi import APIRouter
from src.app.api.v1_routes import (
    user,
    book,
    user_kakao,
    favorite,
    movie,
)


api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(book.router, prefix="/books", tags=["Books"])

api_router.include_router(user_kakao.router, prefix="/user", tags=["User_kakao"]),

api_router.include_router(favorite.router, tags=["Favorites"])
api_router.include_router(movie.router, prefix="/movie", tags=["Movie"])
