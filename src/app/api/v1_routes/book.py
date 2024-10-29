from asyncio import gather
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date

from src.app.v1.book.schemas.requestDto import BookRequest
from src.app.v1.book.schemas.responseDto import (BookOptionsResponse, SeatLayoutResponse,
                                                 UpdateResponse, MovieOption, LocationOption, CinemaOption,
                                                 ScreeningOption, Row, SeatResponse, PaymentRedirectResponse,
                                                 CompletedBookingResponse, CancelledBookingResponse)
from src.app.v1.book.service.book_service import get_book_options
from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.book.schemas.responseDto import BookResponse
router = APIRouter()

#여기도 회원일 경우에 들어오는 방법도 있으므로 access token을 통해 인증 -> 리팩토링

async def get_current_user(user_id: int = Query(None)) -> int | None:
    print(f"[get_current_user] Received user_id: {user_id}")
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

    movies = await BookRepository.get_movies_by_date(screening_date=screening_date)
    if not movies:
        raise HTTPException(status_code=404, detail="해당 날짜에 상영하는 영화를 찾을 수 없습니다.")
    print(f"Movies for {screening_date}: {movies}")

    movie_options = [
        MovieOption(
            id=movie["id"], title=movie["title"], genre=movie["genre"],
            duration=movie["duration"], age_rating=movie["age_rating"],
            poster_image_url=movie["poster_image_url"]
        ) for movie in movies
    ]

    location_tasks = [BookRepository.get_locations_by_movie(movie.id) for movie in movie_options]
    location_results = await gather(*location_tasks)

    all_locations, all_cinemas, all_screenings = [], [], []
    for movie, locations in zip(movie_options, location_results):
        location_options = [LocationOption(id=location["id"], spot=location["spot"]) for location in locations]
        all_locations.extend(location_options)

        cinema_tasks = [BookRepository.get_cinemas_by_location(location.id) for location in location_options]
        cinema_results = await gather(*cinema_tasks)
        for cinemas in cinema_results:
            cinema_options = [CinemaOption(id=cinema["id"], cinema_name=cinema["cinema_name"]) for cinema in
                              cinemas]
            all_cinemas.extend(cinema_options)

            screening_tasks = [BookRepository.get_screenings_by_cinema_and_movie(cinema.id, movie.id) for cinema in
                               cinema_options]
            screening_results = await gather(*screening_tasks)
            for screenings in screening_results:
                screening_options = [
                    ScreeningOption(
                        id=screening["id"],
                        screen_id=screenings["screen_id"],
                        screening_date=screening["screening_date"],
                        start_time=screening["start_time"],
                        end_time=screening["end_time"]
                    )
                    for screening in screenings
                ]
                all_screenings.extend(screening_options)

    return BookOptionsResponse(
        book_id=book_id,
        movies=movie_options,
        locations=all_locations,
        cinemas=all_cinemas,
        screenings=all_screenings
    )


@router.get("/{screen_id}", response_model=Dict[str, List[Dict[str, int]]])
async def get_seat_layout(screen_id: int):
    # 특정 screen_id에 대한 좌석 데이터를 조회
    seats = await Seat.filter(screen_id=screen_id).order_by("row", "column").all()

    if not seats:
        raise HTTPException(status_code=404, detail="해당 상영관의 좌석 정보를 찾을 수 없습니다.")

    # 좌석 데이터를 행별로 정리
    seat_layout = {}
    for seat in seats:
        if seat.row not in seat_layout:
            seat_layout[seat.row] = []
        seat_layout[seat.row].append({
            "seat_number": seat.seat_number,
            "column": seat.column,
            "is_selected": seat.is_selected
        })

    return seat_layout
@router.post("/payment/tosspay", response_model=PaymentRedirectResponse)
async def redirect_to_payment(booking: BookRequest):
    # 임시 리다이렉트 URL
    redirect_url = f"https://example-payment.com/checkout?orderId=order-{booking.booking_id}"

    return PaymentRedirectResponse(book_id=booking.booking_id, redirect_url=redirect_url)

@router.get("/completed/", response_model=List[CompletedBookingResponse])
async def get_completed_bookings(user_id: int = Query(..., description="조회할 사용자의 ID")):
    # BookRepository에서 데이터베이스로부터 예약 정보를 가져옵니다.
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

