from fastapi import APIRouter
from src.common.handlers.exception_handler import BusinessException, ErrorCode
import logging
from src.app.v1.payment.schemas.responseDto import PaymentResponse
from src.app.v1.payment.schemas.requestDto import PaymentRequest
from src.app.v1.payment.service.payment_service import PaymentService

logger = logging.getLogger(__name__)

payment_service = PaymentService()

router = APIRouter()


@router.post("/payment/confirm", response_model=PaymentResponse)
async def payment_confirm(paymentrequest: PaymentRequest):
    """
    결제 승인 엔드포인트
    """
    try:
        logger.debug(paymentrequest)
        return await payment_service.payment_confirm(paymentrequest)
    except Exception as e:
        raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, detail=str(e))
