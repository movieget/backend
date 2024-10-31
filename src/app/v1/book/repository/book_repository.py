from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException

from src.app.v1.book.entity import book
from src.app.v1.book.entity.book import Book
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.cinema.entity.cinema import Cinema
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.location.entity.location import Location
from src.app.v1.book.schemas.requestDto import BookRequest
from typing import List, Dict
import logging

from src.app.v1.user.repository.user_repository import PointRepository
from src.common.models.consts import StatusEnum

from datetime import datetime, date, time


class BookRepository:
    @staticmethod
    async def get_all_booking_data(screening_date: date) -> List[Dict]:
        logging.info(f"Fetching all booking data for screening date: {screening_date}")

        screen_infos = await ScreenInfo.filter(screening_date=screening_date).prefetch_related("movie", "screen__cinema__location").all()

        result = []
        for screen_info in screen_infos:
            # start_time과 end_time이 이미 datetime 객체인 경우 time() 메서드를 사용하여 시간 정보만 추출
            start_time = screen_info.start_time.time() if isinstance(screen_info.start_time, datetime) else screen_info.start_time
            end_time = screen_info.end_time.time() if isinstance(screen_info.end_time, datetime) else screen_info.end_time

            result.append(
                {
                    "movie": {
                        "id": screen_info.movie.id,
                        "title": screen_info.movie.title,
                        "genre": screen_info.movie.genre,
                        "duration": screen_info.movie.duration,
                        "age_rating": screen_info.movie.age_rating,
                        "poster_image_url": screen_info.movie.poster_image_url,
                    },
                    "location": {"id": screen_info.screen.cinema.location.id, "spot": screen_info.screen.cinema.location.spot},
                    "cinema": {"id": screen_info.screen.cinema.id, "cinema_name": screen_info.screen.cinema.cinema_name},
                    "screening": {
                        "id": screen_info.id,
                        "screen_id": screen_info.screen.id,
                        "screening_date": screen_info.screening_date,
                        "start_time": start_time,
                        "end_time": end_time,
                    },
                }
            )

        if not result:
            logging.warning(f"No booking data found for screening date: {screening_date}")

        return result

    @staticmethod
    async def create_user_booking(user_id: int, status: StatusEnum = StatusEnum.PENDING, screen_info_id=None) -> Book:
        logging.info("create_user_booking method is loaded")
        # 예약 생성 로직
        new_user_booking = await Book.create(user_id=user_id, status=status, screen_info_id=screen_info_id)
        return new_user_booking

    # @staticmethod
    # async def create_new_booking(user_id: int = None, status: str = "pending", screen_info_id: int = None) -> Book:
    #     if screen_info_id is None:
    #         logging.error("screen_info_id is required but was not provided.")
    #         raise HTTPException(status_code=400, detail="screen_info_id is required to create a booking.")
    #
    #     logging.info(
    #         f"Creating a new booking with user_id: {user_id}, screen_info_id: {screen_info_id}, and status: {status}")
    #     new_booking = await Book.create(user_id=user_id, screen_info_id=screen_info_id, status=status)
    #     logging.info(f"New booking created with ID: {new_booking.id}")
    #     return new_booking
    # @staticmethod
    # async def get_movies_by_date(screening_date: date) -> List[Movie]:
    #     logging.info(f"Fetching movies for screening date: {screening_date}")
    #     movies = await Movie.filter(screen_infos__screening_date=screening_date).distinct().values(
    #         "id", "title", "genre", "duration", "age_rating", "poster_image_url"
    #     )
    #     if not movies:
    #         logging.warning(f"No movies found for screening date: {screening_date}")
    #         raise HTTPException(status_code=404, detail="해당 날짜에 상영하는 영화를 찾을 수 없습니다.")
    #     return movies
    #
    # @staticmethod
    # async def get_locations_by_movie(movie_id: int) -> List[Location]:
    #     logging.info(f"Fetching locations for movie_id: {movie_id}")
    #     # `Location`과 `Cinema`, `Screen`, `ScreenInfo` 간의 관계를 기반으로 올바른 경로 설정
    #     locations = await Location.filter(
    #         cinemas__screens__screen_infos__movie_id=movie_id  # 관계 설정을 다시 확인하고 수정
    #     ).distinct().values("id", "spot")
    #
    #     if not locations:
    #         logging.warning(f"No locations found for movie_id: {movie_id}")
    #         raise HTTPException(status_code=404, detail="선택한 영화를 상영하는 지역이 없습니다.")
    #     logging.info(f"Found locations: {locations}")
    #     return locations
    #
    # @staticmethod
    # async def get_cinemas_by_location(location_id: int) -> List[Cinema]:
    #     logging.info(f"Fetching cinemas for location_id: {location_id}")
    #     cinemas = await Cinema.filter(location_id=location_id).values("id", "cinema_name")
    #     if not cinemas:
    #         logging.warning(f"No cinemas found for location_id: {location_id}")
    #         raise HTTPException(status_code=404, detail="해당 지역에 영화관이 없습니다.")
    #     return cinemas
    #
    # @staticmethod
    # async def get_screenings_by_cinema_and_movie(cinema_id: int, movie_id: int) -> List[ScreenInfo]:
    #     logging.info(f"Fetching screenings for cinema_id: {cinema_id}, movie_id: {movie_id}")
    #     screenings = await ScreenInfo.filter(screen__cinema_id=cinema_id, movie_id=movie_id).values(
    #         "id", "screening_date", "start_time", "end_time", "screen_id"
    #     )
    #     if not screenings:
    #         logging.warning(f"No screenings found for cinema_id: {cinema_id}, movie_id: {movie_id}")
    #         raise HTTPException(status_code=404, detail="상영 정보가 존재하지 않습니다.")
    #     return screenings

    @staticmethod
    async def get_bookings_by_user_and_status(user_id: int, status: str) -> List[Book]:
        logging.info(f"Fetching bookings for user_id: {user_id} with status: {status}")
        bookings = (
            await Book.filter(user_id=user_id, status=status)
            .prefetch_related("screen_info__movie", "screen_info__screen__cinema", "screen_info__screen__cinema__location", "book_seats__seat")
            .all()
        )
        logging.info(f"Found {len(bookings)} bookings for user_id: {user_id} with status: {status}")
        return bookings

    # 예약 생성
    @staticmethod
    async def create_booking(booking_data: BookRequest, user_id: int) -> Book:
        logging.info(f"Creating booking for user_id: {user_id} with data: {booking_data}")
        try:
            await Movie.get(id=booking_data.movie_id)
            await Cinema.get(id=booking_data.cinema_id)
            await ScreenInfo.get(id=booking_data.screen_info_id)
        except DoesNotExist as e:
            logging.error(f"Invalid movie, cinema, or screen info data: {e}")
            raise HTTPException(status_code=404, detail="유효하지 않은 영화, 영화관 또는 상영 정보입니다.")

        # Book 인스턴스 생성
        new_booking = await Book.create(user_id=user_id, screen_info_id=booking_data.screen_info_id, status="pending")
        logging.info(f"New booking created with ID: {new_booking.id}")

        points_earned = (booking_data.adult_count + booking_data.child_count) * 100
        await PointRepository.update_points(user_id, points_earned)

        return new_booking

    @staticmethod
    async def get_completed_bookings_by_user(user_id: int) -> List[dict]:
        logging.info(f"Fetching completed bookings for user_id: {user_id}")

        completed_bookings = (
            await Book.filter(user_id=user_id, status=StatusEnum.COMPLETED)
            .prefetch_related(
                "screen_info__movie",
                "screen_info__screen",
                "screen_info__screen__cinema",
                "screen_info__screen__cinema__location",
                "book_seats__seat",
            )
            .all()
        )

        if not completed_bookings:
            logging.info(f"No completed bookings found for user_id: {user_id}")
        else:
            logging.info(f"Found {len(completed_bookings)} completed bookings for user_id: {user_id}")

        booking_data = []
        for booking in completed_bookings:
            start_time = datetime.min + booking.screen_info.start_time
            screening_time = start_time.strftime("%H:%M")
            seats = [str(book_seat.seat.seat_number) for book_seat in booking.book_seats]
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
            screen_number_str = "".join(filter(str.isdigit, booking.screen_info.screen.screen_number))
            screen_number = int(screen_number_str) if screen_number_str else None

            booking_info = {
                "booking_id": booking.id,
                "poster_url": booking.screen_info.movie.poster_image_url,
                "title": booking.screen_info.movie.title,
                "duration": booking.screen_info.movie.duration,
                "booking_date": booking.book_time.strftime("%Y-%m-%d"),
                "screening_date": booking.screen_info.screening_date.strftime("%Y-%m-%d"),
                "age_rating": age_rating,
                "seats": seats,
                "total_price": booking.movie_price,
                "adult_count": booking.adult_count,
                "child_count": booking.child_count,
                "screening_time": screening_time,
                "spot": spot,
                "cinema_name": booking.screen_info.screen.cinema.cinema_name,
                "screen_number": screen_number,
            }
            booking_data.append(booking_info)
            logging.debug(f"Added booking data for booking_id: {booking.id}")

        logging.info(f"Completed fetching booking data for user_id: {user_id}")
        return booking_data

    @staticmethod
    async def get_canceled_bookings_by_user(user_id: int) -> List[dict]:
        logging.info(f"Fetching canceled bookings for user_id: {user_id}")

        canceled_bookings = (
            await Book.filter(user_id=user_id, status=StatusEnum.CANCELLED)
            .prefetch_related(
                "screen_info__movie",
                "screen_info__screen",
                "screen_info__screen__cinema",
                "screen_info__screen__cinema__location",
                "book_seats__seat",
            )
            .all()
        )

        if not canceled_bookings:
            logging.info(f"No canceled bookings found for user_id: {user_id}")
        else:
            logging.info(f"Found {len(canceled_bookings)} canceled bookings for user_id: {user_id}")

        booking_data = []
        for booking in canceled_bookings:
            start_time = datetime.min + booking.screen_info.start_time
            screening_time = start_time.strftime("%H:%M")
            seats = [str(book_seat.seat.seat_number) for book_seat in booking.book_seats]
            location = await booking.screen_info.screen.cinema.location
            spot = location.spot if location else "Unknown"

            age_rating = booking.screen_info.movie.age_rating.value
            screen_number_str = "".join(filter(str.isdigit, booking.screen_info.screen.screen_number))
            screen_number = int(screen_number_str) if screen_number_str else None

            booking_info = {
                "booking_id": booking.id,
                "poster_url": booking.screen_info.movie.poster_image_url,
                "title": booking.screen_info.movie.title,
                "duration": booking.screen_info.movie.duration,
                "booking_date": booking.book_time.strftime("%Y-%m-%d"),
                "screening_date": booking.screen_info.screening_date.strftime("%Y-%m-%d"),
                "age_rating": age_rating,
                "seats": seats,
                "total_price": booking.movie_price,
                "adult_count": booking.adult_count,
                "child_count": booking.child_count,
                "screening_time": screening_time,
                "spot": spot,
                "cinema_name": booking.screen_info.screen.cinema.cinema_name,
                "screen_number": screen_number,
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

    @staticmethod
    async def complete_booking(booking_id: int):
        try:
            booking = await book.get(id=booking_id)

            if booking.status == StatusEnum.COMPLETED:
                point_earned = (booking.adult_count + booking.child_count + booking.screening_time) * 100
                await PointRepository.update_points(booking.user_id, point_earned)
            return booking
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="예매 정보를 찾을 수 없습니다.")

