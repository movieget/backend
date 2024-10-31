from src.app.v1.payment.entity.payment import Payment
from src.app.v1.payment.schemas.requestDto import PaymentRequest


class PaymentRepository:
    @staticmethod
    async def create_payment_data(paymentrequest: PaymentRequest) -> PaymentRequest | None:
        return await Payment.create(
            paymentrequest.book_id,
            paymentrequest.paymentKey,
            paymentrequest.orderId,
            paymentrequest.amount,
        )
