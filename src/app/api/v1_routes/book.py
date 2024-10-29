from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date
from src.app.v1.book.schemas.responseDto import (BookOptionsResponse, SeatLayoutResponse,
                                                 UpdateResponse)
from src.app.v1.book.service.book_service import get_book_options
from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.book.schemas.responseDto import BookResponse
router = APIRouter()

#여기도 회원일 경우에 들어오는 방법도 있으므로 access token을 통해 인증 -> 리팩토링

async def get_current_user(user_id: int = Query(None)) -> int | None:
    user = await UserRepository().get_user(user_id)
    if user:
        return user_id
    else:
        raise HTTPException(status_code=404, detail="해당 ID로 사용자를 찾을 수 없습니다.")

@router.get("/books/options", response_model=BookOptionsResponse)
async def booking_options(
    screening_date: str = Query(default=date.today().strftime("%Y-%m-%d"), description="상영 날짜 (YYYY-MM-DD)"),
    user_id: int | None = Depends(get_current_user)
):
    # 회원이면 실제 book_id 생성 (임시 예약 생성)
    book_id = None
    if user_id is not None:
        new_booking = await BookRepository.create_new_booking(user_id=user_id, status="pending")
        book_id = new_booking.id

    response = await get_book_options(screening_date, user_id, book_id=book_id)
    return response

@router.get("/{screen_id}", response_model=SeatLayoutResponse)
async def get_seat_layout(screen_id: int, user_id: int = Query(None)):
    return await BookRepository.get_seat_layout(screen_id=screen_id)

@router.post("/payment/tosspay")
#
# @router.post("/payment/success", response_model=UpdateResponse)
# async def payment_success(booking_id: int):
#     booking = await BookRepository.get_booking_by_id(booking_id)
#     if booking.status != "PENDING":
#         raise HTTPException(status_code=400, detail="유효하지 않은 예약 상태입니다.")
#     return await BookRepository.update_booking_status(booking_id=booking_id, status="COMPLETED")
#
# @router.post("/payment/fail", response_model=UpdateResponse)
# async def payment_fail(booking_id: int):
#     booking = await BookRepository.get_booking_by_id(booking_id)
#     if booking.status != "PENDING":
#         raise HTTPException(status_code=400, detail="유효하지 않은 예약 상태입니다.")
#     return await BookRepository.update_booking_status(booking_id=booking_id, status="CANCELED")

@router.get("/completed", response_model=List[BookResponse])
async def get_completed_bookings(user_id: int = Query(...)):
    print(f"Received user_id for completed bookings: {user_id}")
    # return await BookRepository.get_bookings_by_user_and_status(user_id=user_id, status="completed")
    try:
        bookings = await get_completed_bookings(user_id)
        if not bookings:
            raise HTTPException(status_code=404, detail="예약된 정보가 없습니다.")
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail="예매 내역을 조회하는 중 오류가 발생했습니다.")
@router.get("/canceled/", response_model=List[BookResponse])
async def get_user_canceled_bookings(user_id: int =Query(...)):
    return await BookRepository.get_bookings_by_user_and_status(user_id=user_id, status="canceled")



