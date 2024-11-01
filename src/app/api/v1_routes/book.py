import logging
from asyncio import gather
from typing import List, Dict, Optional, Any
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date, time, timedelta, datetime

from src.app.v1.book.schemas.requestDto import BookRequest, UsePointsRequest
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
from src.app.v1.user.repository.user_repository import UserRepository, PointRepository
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

    # 해당 상영관의 모든 좌석 데이터를 가져오기
    seats = await Seat.filter(screen_id=screen_info.screen.id).order_by("row", "column").all()
    if not seats:
        raise HTTPException(status_code=404, detail="해당 상영관의 좌석 정보를 찾을 수 없습니다.")

    # 각 상영관의 최대 좌석 수를 구함
    max_column = max(seat.column for seat in seats)

    # 좌석 레이아웃을 구성
    seat_layout = {}
    for seat in seats:
        row_label = seat.row
        if row_label not in seat_layout:
            seat_layout[row_label] = [None] * max_column  # 최대 좌석 수에 맞게 리스트 초기화

        # 좌석 정보를 해당 열 위치에 삽입
        seat_layout[row_label][seat.column - 1] = {
            "column": str(seat.column),
            "status": not bool(seat.is_selected) if seat.is_selected is not None else None
        }

    # 포맷팅된 응답 구성
    formatted_response = {
        "screen_id": screen_id,
        "rows": [
            {
                "row": row,
                "seats": [
                    seat if seat is not None else {"column": str(index + 1), "status": None}
                    for index, seat in enumerate(seat_layout[row])
                ]
            }
            for row in sorted(seat_layout.keys())
        ]
    }

    return formatted_response

@router.get("/points/{user_id}", response_model=Dict[str, int])
async def get_user_points(user_id: int):
    logging.debug(f"Received request for user_id: {user_id}")
    try:
        result = await BookRepository.get_user_total_points(user_id)
        if result is None:
            logging.error(f"User {user_id} not found")
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        logging.debug(f"Returning result: {result}")
        return result
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="서버 에러")


@router.post("/points/use", response_model=Dict[str, Any])
async def use_points_for_booking(request: UsePointsRequest):

    try:
        await PointRepository.deduct_points(request.user_id, request.total_point)
        await BookRepository.update_booking_status(request.book_id, StatusEnum.PENDING)

        return {
            "status": "진행중",
            "remaining_points": await PointRepository.get_remaining_points(request.user_id),
            "message": "포인트가 임시로 차감되었으며, 결제 진행 중입니다."
        }
    except Exception as e:
        logging.error(f"Error during point usage: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="포인트 사용 처리 중 오류가 발생했습니다.")


@router.get("/completed/", response_model=List[CompletedBookingResponse])
async def get_completed_bookings(user_id: int = Query(..., description="조회할 사용자의 ID")):

    completed_bookings = await BookRepository.get_completed_bookings_by_user(user_id)

    if not completed_bookings:
        raise HTTPException(status_code=404, detail="완료된 예약을 찾을 수 없습니다.")
    return completed_bookings


@router.get("/canceled/", response_model=List[CancelledBookingResponse])
async def get_canceled_bookings(user_id: int = Query(..., description="조회할 사용자의 ID")):

    canceled_bookings = await BookRepository.get_canceled_bookings_by_user(user_id)

    if not canceled_bookings:
        raise HTTPException(status_code=404, detail="취소된 예약을 찾을 수 없습니다.")
    return canceled_bookings
