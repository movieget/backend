from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from src.common.handlers.exception_handler import BusinessException, ErrorCode
from src.app.v1.book.entity.bookseat import BookSeat
from src.app.v1.book.entity import book
from src.app.v1.book.entity.book import Book
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.screen.entity.seat import Seat
from typing import List, Dict
import logging, re
from src.app.v1.user.entity.user import User
from src.app.v1.user.repository.user_repository import PointRepository
from src.common.models.consts import StatusEnum

from datetime import datetime, date

logger = logging.getLogger(__name__)


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

    @staticmethod
    async def get_user_total_points(user_id: int) -> Dict[str, int]:
        logging.debug(f"Fetching total points for user_id: {user_id}")
        try:
            user = await User.get(id=user_id)
            logging.debug(f"User found: {user.id}, points: {user.point}")
            return {"user_id": user.id, "available_points": user.point}
        except DoesNotExist:
            logging.error(f"User {user_id} does not exist.")
            return None
        except Exception as e:
            logging.error(f"Error fetching total points for user {user_id}: {e}", exc_info=True)
            return None

    @staticmethod
    async def update_book(book_id: str, status: str, adult_count: int, child_count: int, user_id: int, screen_info_id: int) -> Book:
        book = await Book.get(id=book_id)
        book.status = status
        book.adult_count = adult_count
        book.child_count = child_count
        book.user_id = user_id  # 사용자 ID 추가
        book.screen_info_id = screen_info_id  # 스크린 정보 ID 추가
        await book.save()
        return book

    @staticmethod
    async def update_booking_status(book_id: int, status: str) -> None:
        try:
            booking = await Book.get(id=book_id)
            booking.status = status
            await booking.save()
        except DoesNotExist:
            raise ValueError("해당 예매 정보를 찾을 수 없습니다.")

    @staticmethod
    async def get_seat_ids_by_screen(screen_id: int, seat_numbers: List[str]) -> List[int]:
        seat_ids = []

        for seat_number in seat_numbers:
            match = re.match(r"([A-Z])(\d+)", seat_number)
            if not match:
                raise ValueError(f"Invalid seat format: {seat_number}")

            row = match.group(1)
            column = int(match.group(2))

            try:
                # 좌석을 조회하여 ID를 가져옴
                seat = await Seat.get(screen_id=screen_id, row=row, column=column)
                seat_ids.append(seat.id)  # 좌석 ID만 추가
            except DoesNotExist:
                raise ValueError(f"Seat {seat_number} does not exist for screen {screen_id}")

        return seat_ids
