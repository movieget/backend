from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from src.app.v1.book.entity.book import Book
from src.app.v1.book.schemas.responseDto import SeatResponse, SeatLayoutResponse, Row
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.cinema.entity.cinema import Cinema
from src.app.v1.screen.entity import screen_info
from src.app.v1.screen.entity.screen_info import ScreenInfo
from src.app.v1.screen.entity.seat import Seat
from src.app.v1.location.entity.location import Location
from src.app.v1.book.schemas.requestDto import BookRequest
from typing import List, Optional, Dict, Any

from src.common.models.consts import StatusEnum


class BookRepository:
    @staticmethod
    async def create_new_booking(user_id: int = None, status=StatusEnum.PENDING) -> Book:
        return await Book.create(user_id=user_id, status=status, booking_date=datetime.now())

    @staticmethod
    async def get_movies_by_date(screening_date: date):
        movies = await Movie.filter(screen_infos__screening_date=screening_date).distinct().values(
            "id", "title", "genre", "duration", "age_rating", "poster_image_url"
        )
        if not movies:
            raise HTTPException(status_code=404, detail="선택한 날짜에 상영하는 영화를 찾을 수 없습니다.")
        return movies

    @staticmethod
    async def get_locations_by_movie(movie_id: int):
        locations = await Location.filter(cinema__screens__screen_infos__movie_id=movie_id).distinct().values("id", "spot")
        if not locations:
            raise HTTPException(status_code=404, detail="선택한 영화를 상영하는 지역이 없습니다.")
        return locations

    @staticmethod
    async def get_cinemas_by_location(location_id: int):
        cinemas = await Cinema.filter(location_id=location_id).values("id", "cinema_name")
        if not cinemas:
            raise HTTPException(status_code=404, detail="해당 지역에 영화관이 없습니다.")
        return cinemas

    @staticmethod
    async def get_screenings_by_cinema_and_movie(cinema_id: int, movie_id: int):
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

    # 특정 사용자 ID와 상태에 따른 예약 목록을 조회
    @staticmethod
    async def get_bookings_by_user_and_status(user_id: int, status: str) -> List[Book]:
        bookings = await Book.filter(user_id=user_id, status=status).prefetch_related("movie", "location",
                                                                                      "cinema").all()
        if not bookings:
            detail = "예약된 정보가 없습니다." if status == "completed" else "취소된 예약이 없습니다."
            raise HTTPException(status_code=404, detail=detail)
        return bookings

    # 예약 상태 업데이트
    @staticmethod
    async def update_booking_status(book_id: int, status: str) -> Book:
        booking = await Book.get(id=book_id)
        booking.status = status
        await booking.save()
        return booking

    # 임시 예약 삭제
    @staticmethod
    async def delete_booking(book_id: int):
        await Book.filter(id=book_id, status="pending").delete()


    @staticmethod
    async def get_seat_layout(screen_id: int, user_id: int = None):
        seats = await Seat.filter(screen_id=screen_id).order_by("row", "column").all()

        if not seats:
            raise HTTPException(status_code=404, detail="지정한 화면 ID에 대한 좌석을 찾을 수 없습니다.")

        # 열(row)별로 좌석을 그룹화하여 배열 구성
        row_layout: Dict[str, List[SeatResponse]] = {}
        for seat in seats:
            seat_data = SeatResponse(
                seat_number=seat.seat_number,
                is_selected=seat.is_selected,
                row=seat.row,
                column=seat.column
            )
            if seat.row not in row_layout:
                row_layout[seat.row] = []
            row_layout[seat.row].append(seat_data)

        # 최종 좌석 배열을 반환할 형식으로 구성

        seat_layout = SeatLayoutResponse(
            screen_id=screen_id,
            rows=[Row(row=row, seats=seats) for row, seats in row_layout.items()]
        )


        return seat_layout


    # # 예약 데이터 생성 (예: 결제 후 저장)
    # @staticmethod
    # async def create_booking_data(book_data: dict) -> Book:
    #     return await Book.create(**book_data)

    # 상영 정보에 따라 좌석 상태 조회
   #  @staticmethod
   #  async def get_seat_availability(screen_info_id: int):
   #      available_seats = await Seat.filter(screen_info_id=screen_info_id, is_selected=False).values("id",
   #                                                                                                   "seat_number")
   #      reserved_seats = await Seat.filter(screen_info_id=screen_info_id, is_selected=True).values("id", "seat_number")
   #      return available_seats, reserved_seats
   #
   #  # 좌석 상태 업데이트
   #  @staticmethod
   #  async def update_seat_status(seat_ids: List[int], is_selected: bool):
   #      seats = await Seat.filter(id__in=seat_ids).all()
   #      if not seats:
   #          raise HTTPException(status_code=404, detail="유효하지 않은 좌석 정보입니다.")
   #
   #      # 좌석 상태 업데이트
   #      for seat in seats:
   #          seat.is_selected = is_selected
   #          await seat.save()
   #
   #
   #
   #
   #  @staticmethod
   #  async def payment_success(booking_id: int):
   #      booking = await book_repository.get_booking_by_id(booking_id)
   #      if not booking or booking.status != "PENDING":
   #          raise HTTPException(status_code=400, detail="Invalid booking ID or booking not in pending status.")
   #
   #      # 예약 상태를 'COMPLETED'로 업데이트
   #      await book_repository.update_booking_status(booking_id, "COMPLETED")
   #      return {"booking_id": booking_id, "status": "COMPLETED"}
   #
   #  @staticmethod
   #  async def payment_fail(booking_id: int):
   #      booking = await book_repository.get_booking_by_id(booking_id)
   #      if not booking or booking.status != "PENDING":
   #          raise HTTPException(status_code=400, detail="Invalid booking ID or booking not in pending status.")
   #
   #      # 예약 상태를 'CANCELLED'로 업데이트
   #      await book_repository.update_booking_status(booking_id, "CANCELLED")
   #      return {"booking_id": booking_id, "status": "CANCELLED"}
   #
   #
   #  @staticmethod
   #  async def create_reservation_and_redirect_to_payment(booking_data: BookRequest):
   #      # 임시 예약 저장 (PENDING 상태)
   #      temporary_booking = await book_repository.create_booking({
   #          "user_id": booking_data.user_id,
   #          "status": "PENDING",
   #          "screen_info_id": booking_data.screen_info_id,
   #          "adult_count": booking_data.adult_count,
   #          "child_count": booking_data.child_count,
   #          "selected_seat_ids": booking_data.selected_seat_ids
   #      })
   #
   #