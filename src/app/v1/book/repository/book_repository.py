from datetime import date
from typing import List

from tortoise.transactions import in_transaction

from src.app.v1.cinema.entity.cinema import Cinema
from src.app.v1.location.entity.location import Location
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.book.entity.book import Book
from src.app.v1.book.entity.bookseat import BookSeat
from src.app.v1.screen.entity.seat import Seat

# 예약 (book_id) 생성
async def create_new_booking(user_id: int, screen_info_id: int):
    new_booking = await Book.create(
        user_id=user_id,
        screen_info_id=screen_info_id,
        status="PENDING"
    )
    return new_booking


# 특정 날짜에 상영하는 영화 목록 조회
async def get_movies_by_date(screening_date: date):
    return await Movie.filter(screen_infos__screening_date=screening_date).distinct().values("id", "title", "genre", "duration", "age_rating", "poster_image_url")


# 특정 영화에 따라 지역 목록 조회
async def get_locations_by_movie(movie_id: int):
    return await Location.filter(cinema__screens__screen_infos__movie_id=movie_id).distinct().values("id", "spot")

# 특정 지역에 있는 영화관 목록 조회
async def get_cinemas_by_location(location_id: int):
    return await Cinema.filter(location_id=location_id).values("id", "cinema_name")


# 영화관에 따른 상영 시간 조회
async def get_screenings_by_cinema_and_movie(cinema_id: int, movie_id: int):
    return await ScreenInfo.filter(screen__cinema_id=cinema_id, movie_id=movie_id).values("id", "screening_date", "start_time", "end_time", "screen__screen_number")


# 예매 데이터 생성
async def create_booking(book_data: dict):
    return await Book.create(**book_data)

#  특정 사용자 ID와 상태에 따른 예약 목록을 조회
async def get_bookings_by_user_and_status(user_id: int, status: str) -> List[Book]:

    return await Book.filter(user_id=user_id, status=status).all()


# 상영 정보에 따라 좌석 상태 조회
async def get_seat_availability(screen_info_id: int):
    available_seats = await Seat.filter(screen_info_id=screen_info_id, is_selected=False).values("id", "seat_number")
    reserved_seats = await Seat.filter(screen_info_id=screen_info_id, is_selected=True).values("id", "seat_number")
    return available_seats, reserved_seats

# 좌석 상태 업데이트
async def update_seat_status(seat_ids: list, is_selected: bool):
    await Seat.filter(id__in=seat_ids).update(is_selected=is_selected)
