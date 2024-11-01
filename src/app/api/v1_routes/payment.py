from fastapi import APIRouter, Depends
from src.common.handlers.exception_handler import BusinessException, ErrorCode
import logging
from src.app.v1.payment.schemas.responseDto import PaymentResponse
from src.app.v1.payment.schemas.requestDto import PaymentRequest
from src.app.v1.payment.repository.payment_repository import PaymentRepository
from src.app.v1.payment.service.payment_service import PaymentService

logger = logging.getLogger(__name__)


router = APIRouter()


def get_payment_repository():
    # 여기서 PaymentRepository를 초기화하는 로직을 구현합니다.
    # 데이터베이스 연결 등이 필요할 수 있습니다.
    return PaymentRepository()


def get_payment_service(payment_repository: PaymentRepository = Depends(get_payment_repository)):
    return PaymentService(payment_repository)


@router.post("/payment/confirm", response_model=PaymentResponse)
async def payment_confirm(paymentrequest: PaymentRequest, payment_service: PaymentService = Depends(get_payment_service)):
    """
    결제 승인 엔드포인트
    """
    try:
        logger.debug(paymentrequest)
        return await payment_service.confirm_payment(paymentrequest)

    except Exception as e:
        raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, detail=str(e))

    # try:
    #     payment_success = await payment_service.confirm_payment(paymentrequest)
    #
    #     if payment_success:
    #         await PointService.confirm_point_deduction(paymentrequest.user_id)
    #         await BookingService.update_booking_status(paymentrequest.book_id, StatusEnum.COMPLETED)
    #
    #         return {
    #             "status": "완료",
    #             "message": "결제가 성공적으로 완료되었습니다.",
    #             "remaining_points": remaining_points,
    #             **paymentrequest.dict()
    #         }
    #     else:
    #         # 결제 실패 처리
    #         await PointService.restore_points(paymentrequest.user_id)
    #         await BookingService.update_booking_status(paymentrequest.book_id, StatusEnum.CANCELLED)
    #
    #         return {
    #             "status": "취소",
    #             "message": "결제가 실패했습니다. 포인트가 복구되었습니다.",
    #             **paymentrequest.dict()  # 결제 요청 데이터를 포함
    #         }
    # except Exception as e:
    #     raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, detail=str(e))
