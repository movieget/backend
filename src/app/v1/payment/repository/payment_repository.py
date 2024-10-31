from src.app.v1.payment.entity.payment import Payment
from src.app.v1.payment.schemas.requestDto import PaymentRequest


class PaymentRepository:
    @staticmethod
    async def create_payment_data(paymentrequest: PaymentRequest) -> PaymentRequest | None:
        return await Payment.create(
            book_id=paymentrequest.book_id,
            paymentKey=paymentrequest.paymentKey,
            orderId=paymentrequest.orderId,
            amount=paymentrequest.amount,
        )
