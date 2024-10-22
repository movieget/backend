from fastapi import APIRouter
from src.app.api.v1_routes import user
from fastapi import FastAPI
from src.app.api.v1_routes import (
    book_router,
    book_quantity_router,
    available_book_router,
    confirmation_router,
    seat_router
)

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(book_router.router, prefix="/books", tags=["Reservation Options"])
api_router.include_router(book_quantity_router.router, prefix="/book/quantity", tags=["Reservation Quantity"])
api_router.include_router(seat_router.router, prefix="/seats", tags=["Seat Selection"])
api_router.include_router(confirmation_router.router, prefix="confirmation", tags=["Reservation Confirmation"])
api_router.include_router(available_book_router.router, prefix="/books/available", tags=["Reservation Quantity"])
# src/main.py




