from src.common.handlers.exception_handler import BusinessException, ErrorCode
import logging
from src.app.v1.payment.schemas.requestDto import PaymentRequest
from src.app.v1.payment.schemas.responseDto import PaymentResponse
from src.app.v1.payment.repository.payment_repository import PaymentRepository
import base64
import httpx
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(self, payment_repository: PaymentRepository):
        load_dotenv()
        self.secret_key = self._get_secret_key()
        self.encoded_secret_key = self._get_encoded_secret_key()
        self.api_url = os.getenv("TOSS_API_URL")
        self.payment_repository = payment_repository

    def _get_secret_key(self):
        secret_key = os.getenv("TOSS_SECRET_KEY")
        if not secret_key:
            raise ValueError("TOSS_SECRET_KEY 환경 변수가 없습니다.")
        return secret_key

    def _get_encoded_secret_key(self):
        secret_key = os.getenv("TOSS_SECRET_KEY")
        if not secret_key:
            raise ValueError("TOSS_SECRET_KEY 환경 변수가 없습니다.")
        secret_key_with_colon = secret_key + ":"
        return base64.b64encode(secret_key_with_colon.encode("utf-8")).decode("utf-8")

    async def confirm_payment(self, paymentrequest: PaymentRequest):
        """
        토스 페이먼츠 결제 승인 API 호출
        """
        headers = {
            "Authorization": f"Basic {self.encoded_secret_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "paymentKey": paymentrequest.paymentKey,
            "orderId": paymentrequest.orderId,
            "amount": paymentrequest.amount,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.api_url}", headers=headers, json=payload)

                if response.status_code == 200:
                    toss_response = response.json()
                    logger.debug(f"{toss_response}")

                    payment_response = PaymentResponse(
                        paymentKey=toss_response["paymentKey"],
                        orderId=toss_response["orderId"],
                        amount=toss_response["totalAmount"],
                        **paymentrequest.model_dump(exclude={"paymentKey", "orderId", "amount"}),
                    )

                    await self.payment_repository.create_payment_data(paymentrequest)

                    # NOTE: model_dump는 Pydantic 모델 인스턴스의 모든 필드와 값을 파이썬 딕셔너리로 변환
                    return payment_response.model_dump()

                else:
                    error_response = response.json()
                    logger.debug(f"{response.json()}")
                    raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, detail=error_response)
            except httpx.RequestError as e:
                raise BusinessException(ErrorCode.INTERNAL_SERVER_ERROR, detail={"code": "INTERNAL_SERVER_ERROR", "message": str(e)})
