from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from src.app.v1.book.entity.book import Book
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.cinema.entity.cinema import Cinema
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.location.entity.location import Location
from src.app.v1.book.schemas.requestDto import BookRequest
from typing import List
import logging

from src.common.models.consts import StatusEnum


class BookRepository:
    @staticmethod
    async def create_new_booking(user_id: int = None, status: str = "pending") -> Book:
        new_booking = await Book.create(user_id=user_id, status=status)
        return new_booking

    @staticmethod
    async def get_movies_by_date(screening_date: date) ->List[Movie]:
        movies = await Movie.filter(screen_infos__screening_date=screening_date).distinct().values(
            "id", "title", "genre", "duration", "age_rating", "poster_image_url"
        )
        if not movies:
            raise HTTPException(status_code=404, detail="선택한 날짜에 상영하는 영화를 찾을 수 없습니다.")
        return movies

    @staticmethod
    async def get_locations_by_movie(movie_id: int) -> List[Location]:
        locations = await Location.filter(cinema__screens__screen_infos__movie_id=movie_id).distinct().values("id", "spot")
        if not locations:
            raise HTTPException(status_code=404, detail="선택한 영화를 상영하는 지역이 없습니다.")
        return locations

    @staticmethod
    async def get_cinemas_by_location(location_id: int) -> List[Cinema]:
        cinemas = await Cinema.filter(location_id=location_id).values("id", "cinema_name")
        if not cinemas:
            raise HTTPException(status_code=404, detail="해당 지역에 영화관이 없습니다.")
        return cinemas

    @staticmethod
    async def get_screenings_by_cinema_and_movie(cinema_id: int, movie_id: int) -> List[ScreenInfo]:
        screenings = await ScreenInfo.filter(screen__cinema_id=cinema_id, movie_id=movie_id).values(
            "id", "screening_date", "start_time", "end_time", "screen_id"
        )
        if not screenings:
            raise HTTPException(status_code=404, detail="상영 정보가 존재하지 않습니다.")
        return screenings

    @staticmethod
    async def get_bookings_by_user_and_status(user_id: int, status: str) -> List[Book]:
        bookings = await Book.filter(user_id=user_id, status=status).prefetch_related(
            "screen_info__movie",
            "screen_info__screen__cinema",
            "screen_info__screen__cinema__location",
            "book_seats__seat"
        ).all()

        return bookings
    # 예약 생성
    @staticmethod
    async def create_booking(booking_data: BookRequest, user_id: int) -> Book:
        try:
            await Movie.get(id=booking_data.movie_id)
            await Cinema.get(id=booking_data.cinema_id)
            await ScreenInfo.get(id=booking_data.screen_info_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="유효하지 않은 영화, 영화관 또는 상영 정보입니다.")

        # Book 인스턴스 생성
        return await Book.create(
            user_id=user_id,
            screen_info_id=booking_data.screen_info_id,
            status="pending"
        )


    @staticmethod
    @staticmethod
    async def get_completed_bookings_by_user(user_id: int) -> List[dict]:
        logging.info(f"Fetching completed bookings for user_id: {user_id}")

        completed_bookings = await Book.filter(
            user_id=user_id, status=StatusEnum.COMPLETED
        ).prefetch_related(
            "screen_info__movie", "screen_info__screen", "screen_info__screen__cinema",
            "screen_info__screen__cinema__location"
        ).all()

        if not completed_bookings:
            logging.info(f"No completed bookings found for user_id: {user_id}")
        else:
            logging.info(f"Found {len(completed_bookings)} completed bookings for user_id: {user_id}")

        booking_data = []
        for booking in completed_bookings:
            location = await booking.screen_info.screen.cinema.location
            spot = location.spot if location else "Unknown"
            try:
                # 여기에서 movie_price 값을 가져오는지 확인
                total_price = booking.movie_price
                logging.debug(f"Total price calculated: {total_price}")
            except Exception as e:
                logging.error(f"Error accessing movie_price: {e}")
                total_price = 0

            age_rating = booking.screen_info.movie.age_rating.value
            screen_number_str = ''.join(filter(str.isdigit, booking.screen_info.screen.screen_number))
            screen_number = int(screen_number_str) if screen_number_str else None

            booking_info = {
                "booking_id": booking.id,
                "poster_url": booking.screen_info.movie.poster_image_url,
                "title": booking.screen_info.movie.title,
                "duration": booking.screen_info.movie.duration,
                "booking_date": booking.book_time.strftime("%Y-%m-%d"),
                "screening_date": booking.screen_info.screening_date.strftime("%Y-%m-%d"),
                "age_rating": age_rating,
                "seats": [seat.seat_number for seat in await booking.book_seats],
                "total_price": total_price,  # 수정된 부분
                "adult_count": booking.adult_count,
                "child_count": booking.child_count,
                "screening_time": booking.screen_info.start_time.strftime("%H:%M"),
                "spot": spot,
                "cinema_name": booking.screen_info.screen.cinema.cinema_name,
                "screen_number": screen_number
            }
            booking_data.append(booking_info)
            logging.debug(f"Added booking data for booking_id: {booking.id}")

        logging.info(f"Completed fetching booking data for user_id: {user_id}")
        return booking_data

    @staticmethod
    async def get_canceled_bookings_by_user(user_id: int) -> List[dict]:
        logging.info(f"Fetching canceled bookings for user_id: {user_id}")

        canceled_bookings = await Book.filter(
            user_id=user_id, status=StatusEnum.CANCELED
        ).prefetch_related(
            "screen_info__movie", "screen_info__screen", "screen_info__screen__cinema",
            "screen_info__screen__cinema__location"
        ).all()

        if not canceled_bookings:
            logging.info(f"No canceled bookings found for user_id: {user_id}")
        else:
            logging.info(f"Found {len(canceled_bookings)} canceled bookings for user_id: {user_id}")

        booking_data = []
        for booking in canceled_bookings:
            location = await booking.screen_info.screen.cinema.location
            spot = location.spot if location else "Unknown"

            age_rating = booking.screen_info.movie.age_rating.value
            screen_number_str = ''.join(filter(str.isdigit, booking.screen_info.screen.screen_number))
            screen_number = int(screen_number_str) if screen_number_str else None

            booking_info = {
                "booking_id": booking.id,
                "poster_url": booking.screen_info.movie.poster_image_url,
                "title": booking.screen_info.movie.title,
                "duration": booking.screen_info.movie.duration,
                "booking_date": booking.book_time.strftime("%Y-%m-%d"),
                "screening_date": booking.screen_info.screening_date.strftime("%Y-%m-%d"),
                "age_rating": age_rating,
                "seats": [seat.seat_number for seat in await booking.book_seats],
                "total_price": booking.movie_price,
                "adult_count": booking.adult_count,
                "child_count": booking.child_count,
                "screening_time": booking.screen_info.start_time.strftime("%H:%M"),
                "spot": spot,
                "cinema_name": booking.screen_info.screen.cinema.cinema_name,
                "screen_number": screen_number
            }
            booking_data.append(booking_info)
            logging.debug(f"Added canceled booking data for booking_id: {booking.id}")

        logging.info(f"Completed fetching canceled booking data for user_id: {user_id}")
        return booking_data


    @staticmethod
    async def get_seat_layout(screen_id: int) -> List[Seat]:
        seats = await Seat.filter(screen_id=screen_id).order_by("row", "seat_number").all()

        if not seats:
            raise HTTPException(status_code=404, detail="지정한 화면 ID에 대한 좌석을 찾을 수 없습니다.")
        return seats
