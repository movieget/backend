from src.app.v1.screen.entity.seat import Seat
from src.app.v1.book.schemas.requestDto import SuccessBookingRequest, FailBookingRequest
from src.app.v1.book.schemas.responseDto import SuccessBookingResponse, FailBookingResponse
from tortoise.transactions import in_transaction
from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.screen.repository.screeninfo_repository import ScreenInfoRepository
from src.app.v1.user.entity.point_history import PointHistory
from src.app.v1.user.repository.user_repository import PointRepository
from src.common.handlers.exception_handler import BusinessException, ErrorCode
import logging

logger = logging.getLogger(__name__)


class BookService:

    def __init__(
            self, book_repository: BookRepository,
            screeninfo_repository: ScreenInfoRepository,
            point_repository: PointRepository,
    ):
        self.book_repository = book_repository
        self.screeninfo_repository = screeninfo_repository
        self.point_repository = point_repository
    async def update_success_booking(self, user_id: int, screen_id: int, successrequest: SuccessBookingRequest) -> SuccessBookingResponse:
        screen_info = await self.screeninfo_repository.get_screen_info_id(screen_id, successrequest.screening_date, successrequest.screening_time)
        if not screen_info:
            raise BusinessException(ErrorCode.SCREEN_NOT_FOUND, detail=f"Screen {screen_info.id}를 찾을 수 없습니다.")

        seat_ids = await self.book_repository.get_seat_ids_by_screen(screen_id, successrequest.seats)

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

            if successrequest.total_point > 0:
                await PointHistory.create(
                    user_id=user_id,
                    change_type="이용 내역",
                    points=successrequest.total_point,
                    description=successrequest.title
                )

            total_point_add = (successrequest.adult_count + successrequest.child_count) * 100
            await self.point_repository.update_points(
                user_id=user_id,
                points_to_add=total_point_add,
                change_type="예매 적립",
                description=successrequest.title
            )
        logger.info(f"{user_id}에게 {total_point_add}적립되었습니다.")
        return SuccessBookingResponse(message="예약이 성공적으로 완료되었습니다.", book_id=str(book.id))

    async def update_fail_booking(self, user_id: int, screen_id: int, failrequest: FailBookingRequest) -> FailBookingResponse:
        screen_info = await self.screeninfo_repository.get_screen_info_id(screen_id, failrequest.screening_date, failrequest.screening_time)
        if not screen_info:
            raise BusinessException(ErrorCode.SCREEN_NOT_FOUND, detail=f"Screen {screen_info.id}를 찾을 수 없습니다.")

        # seat_ids = await self.book_repository.get_seat_ids_by_screen(screen_id, failrequest.seats)

        # # 선택된 좌석이 이미 예약된 경우 예외 발생
        # for seat_id in seat_ids:
        #     seat = await Seat.get(id=seat_id)  # 좌석 조회
        #     if seat.is_selected:  # 이미 선택된 좌석인지 확인
        #         raise BusinessException(ErrorCode.SEAT_ALREADY_SELECTED, detail=f"좌석 {seat_id}는 이미 선택되었습니다.")

        async with in_transaction():
            await self.point_repository.restore_points(user_id, failrequest.points_to_restore)
            # 예약 상태를 'CANCELLED'로 업데이트
            book = await self.book_repository.update_book(
                book_id=failrequest.book_id,
                status="취소",
                adult_count=failrequest.adult_count,
                child_count=failrequest.child_count,
                user_id=user_id,
                screen_info_id=screen_info.id,
            )
            await PointHistory.filter(
                user_id=user_id,
                change_type="이용 내역",
                points=failrequest.points_to_restore,
                description=failrequest.title
            ).delete()

            # 선택된 좌석의 상태를 업데이트 (is_selected를 False로 설정)
            # for seat_id in seat_ids:
            #     seat = await Seat.get(id=seat_id)
            #     seat.is_selected = False
            #     await seat.save()

        return FailBookingResponse(message="예약이 취소되었습니다.", book_id=str(book.id))
