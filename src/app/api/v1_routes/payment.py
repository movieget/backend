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
