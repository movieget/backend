import logging
from asyncio import gather
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date, time, timedelta, datetime

from src.app.v1.book.schemas.requestDto import BookRequest
from src.app.v1.book.schemas.responseDto import (
    BookOptionsResponse,
    SeatLayoutResponse,
    MovieOption,
    LocationOption,
    CinemaOption,
    ScreeningOption,
    PaymentRedirectResponse,
    CompletedBookingResponse,
    CancelledBookingResponse,
)

from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.book.schemas.responseDto import BookResponse
from src.common.models.consts import StatusEnum

from datetime import datetime, timedelta

router = APIRouter()

logging.basicConfig(level=logging.INFO)


async def get_current_user(user_id: int | None = Query(None)) -> int | None:
    print(f"[get_current_user] Received user_id: {user_id}")
    if user_id is not None:
        user = await UserRepository().get_user(user_id)
        if user:
            return user_id
    return None  # None을 반환하여 비회원 처리


@router.get("/options", response_model=BookOptionsResponse)
async def booking_options(screening_date: str = Query(..., description="상영 날짜 (YYYY-MM-DD)"), user_id: int | None = Depends(get_current_user)):
    logging.info(f"Request for booking options on {screening_date} with user_id: {user_id}")

    book_id = None
    logging.info(f"Checking user_id value: {user_id}")
    if user_id:
        new_user_booking = await BookRepository.create_user_booking(user_id=user_id, status=StatusEnum.PENDING)
        book_id = new_user_booking.id
        logging.info(f"생성된 book_id: {book_id} for user_id: {user_id}")
    else:
        logging.info("유저가 인증이 안되고, book_id 생성이 안됨")

    try:
        all_data = await BookRepository.get_all_booking_data(date.fromisoformat(screening_date))
    except HTTPException as e:
        logging.error(f"Error fetching booking data: {str(e)}")
        raise e

    movies = {}
    locations = {}
    cinemas = {}
    screenings = []

    for item in all_data:
        movie = item["movie"]
        if movie["id"] not in movies:
            movies[movie["id"]] = MovieOption(**movie)

        location = item["location"]
        if location["id"] not in locations:
            locations[location["id"]] = LocationOption(**location)

        cinema = item["cinema"]
        if cinema["id"] not in cinemas:
            cinemas[cinema["id"]] = CinemaOption(**cinema)

        screening = item["screening"]

        # Convert timedelta to time if necessary
        start_time = screening["start_time"]
        end_time = screening["end_time"]
        if isinstance(start_time, timedelta):
            start_time = (datetime.min + start_time).time()
        if isinstance(end_time, timedelta):
            end_time = (datetime.min + end_time).time()

        screenings.append(
            ScreeningOption(
                id=screening["id"],
                screen_id=screening["screen_id"],
                screening_date=screening["screening_date"],
                start_time=start_time,
                end_time=end_time,
            )
        )

    logging.info("Returning all booking options")
    return BookOptionsResponse(
        book_id=book_id, movies=list(movies.values()), locations=list(locations.values()), cinemas=list(cinemas.values()), screenings=screenings
    )


@router.get("/{screen_id}", response_model=SeatLayoutResponse)
async def get_seat_layout(screen_id: int):
    # ScreenInfo 및 관련 Screen 데이터를 조회
    screen_info = await ScreenInfo.get(id=screen_id).prefetch_related("screen")

    if not screen_info:
        raise HTTPException(status_code=404, detail="해당 screen_id에 대한 상영관 정보를 찾을 수 없습니다.")

    # 상영관의 최대 열 수를 동적으로 설정
    max_column = screen_info.screen.total_seats

    # 좌석 데이터를 조회
    seats = await Seat.filter(screen_id=screen_info.screen.id).order_by("row", "column").all()

    if not seats:
        raise HTTPException(status_code=404, detail="해당 상영관의 좌석 정보를 찾을 수 없습니다.")

    # 좌석 데이터를 행별로 정리
    seat_layout = {}
    for seat in seats:
        row_label = seat.row
        if row_label not in seat_layout:
            seat_layout[row_label] = [None] * max_column

        # 비어있는 좌석은 True, 선택된 좌석은 False로 설정
        seat_layout[row_label][seat.column - 1] = {
            "column": str(seat.column),
            "status": not bool(seat.is_selected) if seat.is_selected is not None else None
        }

    # 없는 좌석을 null 값으로 유지
    formatted_response = {
        "screen_id": screen_id,
        "rows": [
            {"row": row, "seats": [
                seat if seat is not None else {"column": None, "status": None}
                for seat in seat_layout[row]
            ]}
            for row in sorted(seat_layout.keys())
        ]
    }

    return formatted_response


@router.post("/payment/tosspay", response_model=PaymentRedirectResponse)
async def redirect_to_payment(booking: BookRequest):
    # 임시 리다이렉트 URL
    redirect_url = f"https://example-payment.com/checkout?orderId=order-{booking.booking_id}"

    return PaymentRedirectResponse(book_id=booking.booking_id, redirect_url=redirect_url)


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/completed/", response_model=List[CompletedBookingResponse])
async def get_completed_bookings(user_id: int = Query(..., description="조회할 사용자의 ID")):
    logger.info(f"Fetching completed bookings for user_id: {user_id}")
    completed_bookings = await BookRepository.get_completed_bookings_by_user(user_id)

    if not completed_bookings:
        logger.info(f"No completed bookings found for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="완료된 예약을 찾을 수 없습니다.")

    logger.info(f"Found {len(completed_bookings)} completed bookings for user_id: {user_id}")
    return completed_bookings


@router.get("/canceled/", response_model=List[CancelledBookingResponse])
async def get_canceled_bookings(user_id: int = Query(..., description="조회할 사용자의 ID")):
    logger.info(f"Fetching canceled bookings for user_id: {user_id}")
    canceled_bookings = await BookRepository.get_canceled_bookings_by_user(user_id)

    if not canceled_bookings:
        logger.info(f"No canceled bookings found for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="취소된 예약을 찾을 수 없습니다.")
    logger.info(f"Found {len(canceled_bookings)} canceled bookings for user_id: {user_id}")
    return canceled_bookings
