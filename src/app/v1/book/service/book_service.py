from src.app.v1.screen.entity.seat import Seat
from src.app.v1.book.schemas.requestDto import SuccessBookingRequest, FailBookingRequest
from src.app.v1.book.schemas.responseDto import SuccessBookingResponse, FailBookingResponse
from tortoise.transactions import in_transaction
from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.screen.repository.screeninfo_repository import ScreenInfoRepository
from src.common.handlers.exception_handler import BusinessException, ErrorCode
import logging

logger = logging.getLogger(__name__)


class BookService:

    def __init__(self, book_repository: BookRepository, screeninfo_repository: ScreenInfoRepository):
        self.book_repository = book_repository
        self.screeninfo_repository = screeninfo_repository

    async def update_success_booking(self, user_id: int, screen_id: int, successrequest: SuccessBookingRequest) -> SuccessBookingResponse:
        screen_info = await self.screeninfo_repository.get_screen_info_id(screen_id, successrequest.screening_date, successrequest.screening_time)
        if not screen_info:
            raise BusinessException(ErrorCode.SCREEN_NOT_FOUND, detail="Screen {screen_info.id}를 찾을 수 없습니다.")
        logging.info(f"screen_info = {screen_info} ???")

        seat_ids = await self.book_repository.get_seat_ids_by_screen(screen_id, successrequest.seats)
        logging.info(f"screen_info = {seat_ids} ???")

        # 선택된 좌석이 이미 예약된 경우 예외 발생
        for seat_id in seat_ids:
            seat = await Seat.get(id=seat_id)  # 좌석 조회
            if seat.is_selected:  # 이미 선택된 좌석인지 확인
                raise BusinessException(ErrorCode.SEAT_ALREADY_SELECTED, detail=f"좌석 {seat_id}는 이미 선택되었습니다.")

        async with in_transaction():
            # 예약 정보 업데이트
            book = await self.book_repository.update_book(
                book_id=successrequest.book_id,
                status="완료",
                adult_count=successrequest.adult_count,
                child_count=successrequest.child_count,
                user_id=user_id,
                screen_info_id=screen_info.id,
            )

            # 선택된 좌석의 상태를 업데이트 (is_selected를 True로 설정)
            for seat_id in seat_ids:
                seat = await Seat.get(id=seat_id)
                seat.is_selected = True
                await seat.save()

        return SuccessBookingResponse(message="예약이 성공적으로 완료되었습니다.", book_id=book.id)

    async def update_fail_booking(self, user_id: int, screen_id: int, failrequest: FailBookingRequest) -> FailBookingResponse:
        screen_info = self.screeninfo_repository.get_screen_info_id(screen_id, failrequest.screening_date, failrequest.screening_time)
        if not screen_info:
            raise BusinessException(ErrorCode.SCREEN_NOT_FOUND, detail="Screen {screen_info.id}를 찾을 수 없습니다.")
        logging.info(f"screen_info = {screen_info} ???")

        seat_ids = self.book_repository.get_seat_ids_by_screen(screen_id, failrequest.seats)
        logging.info(f"screen_info = {seat_ids} ???")

        # 선택된 좌석이 이미 예약된 경우 예외 발생
        for seat_id in seat_ids:
            seat = await Seat.get(id=seat_id)  # 좌석 조회
            if seat.is_selected:  # 이미 선택된 좌석인지 확인
                raise BusinessException(ErrorCode.SEAT_ALREADY_SELECTED, detail=f"좌석 {seat_id}는 이미 선택되었습니다.")

        async with in_transaction():
            # 예약 상태를 'CANCELLED'로 업데이트
            book = await self.book_repository.update_book(
                book_id=failrequest.book_id,
                status="취소",
                adult_count=failrequest.adult_count,
                child_count=failrequest.child_count,
                user_id=user_id,
                screen_info_id=screen_info.id,
            )

            # 선택된 좌석의 상태를 업데이트 (is_selected를 True로 설정)
            for seat_id in seat_ids:
                seat = await Seat.get(id=seat_id)
                seat.is_selected = True
                await seat.save()

        return FailBookingResponse(message="예약이 취소되었습니다.", book_id=book.id)
