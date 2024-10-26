from typing import List

from src.app.v1.book.entity.book import Book
from src.app.v1.book.repository import book_repository
from src.app.v1.book.schemas.book import BookRequest, BookResponse
from fastapi import HTTPException

from src.app.v1.cinema.entity.cinema import Cinema
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.screen.entity.screen_info import ScreenInfo


async def create_booking(booking_data: BookRequest, user_id: int) -> BookResponse:
    # 영화, 영화관, 상영 정보 가져오기
    movie = await Movie.get(id=booking_data.movie_id)
    cinema = await Cinema.get(id=booking_data.cinema_id)
    screen_info = await ScreenInfo.get(id=booking_data.screen_info_id)

    # 임시 예약 생성
    new_booking = await book_repository.create_new_booking(user_id=user_id, screen_info_id=booking_data.screen_info_id)

    # 좌석 예약 처리
    await book_repository.update_seat_status(booking_data.selected_seat_ids, is_selected=True)

    # 응답 구성
    return BookResponse(
        book_id=new_booking.id,
        movie_title=movie.title,
        cinema_name=cinema.cinema_name,
        screen_number=screen_info.screen.screen_number,
        start_time=screen_info.start_time,
        end_time=screen_info.end_time,
        total_price=calculate_total_price(booking_data.adult_count, booking_data.child_count),
        reserved_seats=booking_data.selected_seat_ids
    )


# 유저가 예약한 모든 예약 정보 가져오기
async def get_completed_bookings_by_user_id(user_id: int) -> List[Book]:
    return await book_repository.get_bookings_by_user_and_status(user_id=user_id, status="COMPLETED")


# 유저가 취소한 모든 예약 정보 가져오기
async def get_canceled_bookings_by_user_id(user_id: int) -> List[Book]:
    return await book_repository.get_bookings_by_user_and_status(user_id=user_id, status="CANCELED")

# 총 가격 계산 로직
def calculate_total_price(adult_count: int, child_count: int) -> float:
    adult_price = 14000
    child_price = 12000
    return (adult_count * adult_price) + (child_count * child_price)

async def get_booking_by_id(book_id: int):
    try:
        # 예매 정보를 Book 테이블에서 조회
        booking = await Book.get(id=book_id).prefetch_related("user", "screen_info", "seats")
        return booking
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="예약정보를 찾을 수 없습니다.")

