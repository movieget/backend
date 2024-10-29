from asyncio import gather
from datetime import date
from typing import List, Dict
from fastapi import HTTPException

from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.book.schemas.responseDto import BookOptionsResponse, MovieOption, LocationOption, CinemaOption, \
    ScreeningOption, BookResponse, SeatLayoutResponse



#여기도 회원일 경우에 들어오는 방법도 있으므로 access token을 통해 인증 -> 리팩토링

async def get_book_options(screening_date: date, user_id: int | None) -> BookOptionsResponse:

    movies = await BookRepository.get_movies_by_date(screening_date=screening_date)
    if not movies:
        raise HTTPException(status_code=404, detail="해당 날짜에 상영하는 영화를 찾을 수 없습니다.")
    print(f"Movies for {screening_date}: {movies}")

    new_booking = await BookRepository.create_new_booking(user_id=user_id, status="pending")
    book_id = new_booking.id
    # # 로그인 상태에 따라 book_id 생성 (회원은 실제 book_id, 비회원은 임시 book_id)
    # if user_id is not None:
    #     new_booking = await BookRepository.create_new_booking(user_id=user_id, status="pending")
    # else:
    #     new_booking = await BookRepository.create_new_booking(user_id=None, status="pending")
    # book_id = new_booking.id


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
            cinema_options = [CinemaOption(id=cinema["id"], cinema_name=cinema["cinema_name"]) for cinema in cinemas]
            all_cinemas.extend(cinema_options)

            screening_tasks = [BookRepository.get_screenings_by_cinema_and_movie(cinema.id, movie.id) for cinema in cinema_options]
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


async def get_completed_bookings(user_id: int) ->List[BookResponse]:
# async def get_completed_bookings(user: User = Depends(get_current_user)):

    bookings = await BookRepository.get_bookings_by_user_and_status(user_id=user_id, status="completed")

    if not bookings:
        raise HTTPException(status_code=404, detail="예약된 정보가 없습니다.")


    return [
        BookResponse(
            poster_url=booking.screen_info.movie.poster_image_url,
            movie_info=f"{booking.screen_info.movie.title}, {booking.screen_info.movie.age_rating}세 이상",
            booking_date=booking.book_time.strftime("%Y-%m-%d"),
            screening_date=booking.screen_info.screening_date.strftime("%Y-%m-%d"),
            seats=[f"{seat.seat.row}{seat.seat.seat_number}" for seat in booking.book_seats],
            total_price=booking.movie_price * (booking.adult_count + booking.child_count),
            person_count=f"성인{booking.adult_count} / 청소년{booking.child_count}",
            screening_time=booking.screen_info.start_time.strftime("%H:%M"),
            location=booking.screen_info.screen.cinema.location.spot,
            cinema=booking.screen_info.screen.cinema.cinema_name,
            screen_number=booking.screen_info.screen.screen_number
        )
        # BookResponse(
        #     poster_url=booking.movie.poster_url,
        #     movie_info=f"{booking.movie.title}, {booking.movie.age_limit}세 이상",
        #     booking_date=booking.booking_date,
        #     screening_date=booking.screening_date,
        #     seats=booking.seats,
        #     total_price=booking.total_price,
        #     person_count=f"성인{booking.adult_count} / 청소년{booking.child_count}",
        #     screening_time=booking.screening_time,
        #     location=booking.location.name,
        #     cinema=booking.cinema.name
        # )
        for booking in bookings
    ]

async def get_user_canceled_bookings(user_id: int) -> List[BookResponse]:
# async def get_user_canceled_bookings(user: User = Depends(get_current_user)):

    canceled_bookings = await BookRepository.get_bookings_by_user_and_status(user_id=user_id, status="canceled")

    if not canceled_bookings:
        raise HTTPException(status_code=404, detail="취소된 예약이 없습니다.")

    return [
        BookResponse(
            poster_url=booking.movie.poster_url,
            movie_info=f"{booking.movie.title}, {booking.movie.age_limit}세 이상",
            booking_date=booking.booking_date,
            screening_date=booking.screening_date,
            seats=booking.seats,
            total_price=booking.total_price,
            person_count=f"성인{booking.adult_count} / 청소년{booking.child_count}",
            screening_time=booking.screening_time,
            location=booking.location.name,
            cinema=booking.cinema.name
        )
        for booking in canceled_bookings
    ]

# 특정 상영관의 좌석 레이아웃 가져오기
async def get_seat_layout(screen_id: int) -> SeatLayoutResponse:
    return await BookRepository.get_seat_layout(screen_id=screen_id)

# # 좌석 예약 처리
# async def reserve_seats(seat_ids: List[int], book_id: int):
#     async with in_transaction() as transaction:
#         # 좌석들이 이미 예약되어 있는지 확인
#         seats = await BookRepository.get_seat_availability(screen_info_id=book_id)
#         if any(seat.is_selected for seat in seats):
#             raise HTTPException(status_code=400, detail="이미 예약된 좌석이 있습니다.")
#
#         # 좌석 예약 처리
#         await BookRepository.update_seat_status(seat_ids=seat_ids, is_selected=True)
#         await transaction.commit()