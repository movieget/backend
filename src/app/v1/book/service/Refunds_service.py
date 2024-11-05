from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from tortoise.transactions import in_transaction
from src.app.v1.book.schemas.responseDto import PaymentFailureResponse, PaymentCancellationResponse
from src.app.v1.payment.entity.payment import Payment
from src.app.v1.payment.entity.payment_history import PaymentHistory
from src.app.v1.refund.entity.refund import Refund
from src.app.v1.book.entity.book import Book
from src.app.v1.user.entity.user import User
from src.app.v1.user.entity.point_history import PointHistory
from src.core.configs.database_config import settings
import httpx
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def restore_points(user_id: int, book_id: int, amount: int):
    async with in_transaction() as conn:
        try:
            # 사용자 조회
            user = await User.get(id=user_id).using_db(conn)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # 포인트 이력 생성
            await PointHistory.create(
                user_id=user_id,
                book_id=book_id,
                points=amount,
                change_type="REFUND",
                description="결제 취소로 인한 포인트 환불",
                using_db=conn
            )

            # 사용자 포인트 업데이트
            user.points += amount
            await user.save(using_db=conn)

            logger.info(f"Points restored for user {user_id}: {amount} points")
        except Exception as e:
            logger.error(f"Error restoring points: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to restore points")


async def handle_payment_failure(book_id: Optional[int], error_code: str, error_message: str) -> PaymentFailureResponse:
    logger.info(f"Handling payment failure for book_id: {book_id}")
    try:
        if book_id is None:
            logger.warning("Book ID is None, creating generic failure response")
            return PaymentFailureResponse(
                book_id=None,
                poster_url="",
                title="Unknown",
                age_rating="All",
                canceled_date=datetime.now(),
                adult_count=0,
                child_count=0,
                spot="Unknown",
                cinema_name="Unknown",
                refund_amount=0,
                error_code=error_code,
                error_message=error_message
            )

        book = await Book.get(id=book_id).prefetch_related('movie', 'cinema', 'cinema__location')
        movie = await book.movie
        cinema = await book.cinema
        location = await cinema.location

        # 포인트 복구 로직 (만약 포인트를 사용했다면)
        point_history = await PointHistory.filter(book_id=book_id).first()
        if point_history:
            logger.info(f"Restoring points for book_id: {book_id}")
            await restore_points(point_history.user_id, book_id, point_history.points)

        response = PaymentFailureResponse(
            book_id=book_id,
            poster_url=movie.poster_image_url,
            title=movie.title,
            age_rating=movie.age_rating,
            canceled_date=datetime.now(),
            adult_count=book.adult_count,
            child_count=book.child_count,
            spot=location.spot,
            cinema_name=cinema.cinema_name,
            refund_amount=0,  # 결제 실패이므로 환불 금액은 0
            error_code=error_code,
            error_message=error_message
        )
        logger.info(f"Payment failure response created for book_id: {book_id}")
        return response
    except Exception as e:
        logger.error(f"Error in handle_payment_failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def handle_payment_cancellation(payment_key: str) -> PaymentCancellationResponse:
    logger.info(f"Handling payment cancellation for payment_key: {payment_key}")
    try:
        payment = await Payment.filter(payment_key=payment_key).first().prefetch_related(
            'book', 'book__movie', 'book__cinema', 'book__cinema__location'
        )
        if not payment:
            logger.error(f"Payment not found for payment_key: {payment_key}")
            raise HTTPException(status_code=404, detail="Payment not found")

        book = await payment.book
        movie = await book.movie
        cinema = await book.cinema
        location = await cinema.location

        # 결제 취소 정보 조회
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.TOSS_API_URL}/v1/payments/{payment_key}",
                headers={"Authorization": f"Basic {settings.TOSS_SECRET_KEY}"}
            )
            payment_info = response.json()
            logger.info(f"Toss API response for payment_key {payment_key}: {payment_info}")

        # 환불 처리
        refund_amount = payment_info['cancelAmount']
        refund = await Refund.create(
            book=book,
            amount=refund_amount,
            reason=payment_info['cancels'][0]['reason']
        )
        logger.info(f"Refund created for book_id: {book.id}, amount: {refund_amount}")

        # 결제 이력 업데이트
        await PaymentHistory.create(
            payment=payment,
            status='CANCELED',
            amount=refund_amount
        )
        logger.info(f"Payment history updated for payment_id: {payment.id}")

        # 포인트 복구 로직
        point_history = await PointHistory.filter(book_id=book.id).first()
        if point_history:
            logger.info(f"Restoring points for book_id: {book.id}")
            await restore_points(point_history.user_id, book.id, point_history.points)

        response = PaymentCancellationResponse(
            book_id=book.id,
            poster_url=movie.poster_image_url,
            title=movie.title,
            age_rating=movie.age_rating,
            canceled_date=datetime.fromisoformat(payment_info['canceledAt']),
            adult_count=book.adult_count,
            child_count=book.child_count,
            spot=location.spot,
            cinema_name=cinema.cinema_name,
            refund_amount=refund_amount,
            cancellation_reason=payment_info['cancels'][0]['reason']
        )
        logger.info(f"Payment cancellation response created for book_id: {book.id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in handle_payment_cancellation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def restore_points(user_id: int, book_id: int, amount: int):
    async with in_transaction() as conn:
        try:
            # 사용자 조회
            user = await User.get(id=user_id).using_db(conn)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # 포인트 이력 생성
            await PointHistory.create(
                user_id=user_id,
                book_id=book_id,
                points=amount,
                change_type="REFUND",
                description="결제 취소로 인한 포인트 환불",
                using_db=conn
            )

            # 사용자 포인트 업데이트
            user.points += amount
            await user.save(using_db=conn)

            logger.info(f"Points restored for user {user_id}: {amount} points")
        except Exception as e:
            logger.error(f"Error restoring points: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to restore points")


async def handle_payment_failure(book_id: Optional[int], error_code: str, error_message: str) -> PaymentFailureResponse:
    logger.info(f"Handling payment failure for book_id: {book_id}")
    try:
        if book_id is None:
            logger.warning("Book ID is None, creating generic failure response")
            return PaymentFailureResponse(
                book_id=None,
                poster_url="",
                title="Unknown",
                age_rating="All",
                canceled_date=datetime.now(),
                adult_count=0,
                child_count=0,
                spot="Unknown",
                cinema_name="Unknown",
                refund_amount=0,
                error_code=error_code,
                error_message=error_message
            )

        book = await Book.get(id=book_id).prefetch_related('movie', 'cinema', 'cinema__location')
        movie = await book.movie
        cinema = await book.cinema
        location = await cinema.location

        # 포인트 복구 로직 (만약 포인트를 사용했다면)
        point_history = await PointHistory.filter(book_id=book_id).first()
        if point_history:
            logger.info(f"Restoring points for book_id: {book_id}")
            await restore_points(point_history.user_id, book_id, point_history.points)

        response = PaymentFailureResponse(
            book_id=book_id,
            poster_url=movie.poster_image_url,
            title=movie.title,
            age_rating=movie.age_rating,
            canceled_date=datetime.now(),
            adult_count=book.adult_count,
            child_count=book.child_count,
            spot=location.spot,
            cinema_name=cinema.cinema_name,
            refund_amount=0,  # 결제 실패이므로 환불 금액은 0
            error_code=error_code,
            error_message=error_message
        )
        logger.info(f"Payment failure response created for book_id: {book_id}")
        return response
    except Exception as e:
        logger.error(f"Error in handle_payment_failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def handle_payment_cancellation(payment_key: str) -> PaymentCancellationResponse:
    logger.info(f"Handling payment cancellation for payment_key: {payment_key}")
    try:
        payment = await Payment.filter(payment_key=payment_key).first().prefetch_related(
            'book', 'book__movie', 'book__cinema', 'book__cinema__location'
        )
        if not payment:
            logger.error(f"Payment not found for payment_key: {payment_key}")
            raise HTTPException(status_code=404, detail="Payment not found")

        book = await payment.book
        movie = await book.movie
        cinema = await book.cinema
        location = await cinema.location

        # 결제 취소 정보 조회
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.TOSS_API_URL}/v1/payments/{payment_key}",
                headers={"Authorization": f"Basic {settings.TOSS_SECRET_KEY}"}
            )
            payment_info = response.json()
            logger.info(f"Toss API response for payment_key {payment_key}: {payment_info}")

        # 환불 처리
        refund_amount = payment_info['cancelAmount']
        refund = await Refund.create(
            book=book,
            amount=refund_amount,
            reason=payment_info['cancels'][0]['reason']
        )
        logger.info(f"Refund created for book_id: {book.id}, amount: {refund_amount}")

        # 결제 이력 업데이트
        await PaymentHistory.create(
            payment=payment,
            status='CANCELED',
            amount=refund_amount
        )
        logger.info(f"Payment history updated for payment_id: {payment.id}")

        # 포인트 복구 로직
        point_history = await PointHistory.filter(book_id=book.id).first()
        if point_history:
            logger.info(f"Restoring points for book_id: {book.id}")
            await restore_points(point_history.user_id, book.id, point_history.points)

        response = PaymentCancellationResponse(
            book_id=book.id,
            poster_url=movie.poster_image_url,
            title=movie.title,
            age_rating=movie.age_rating,
            canceled_date=datetime.fromisoformat(payment_info['canceledAt']),
            adult_count=book.adult_count,
            child_count=book.child_count,
            spot=location.spot,
            cinema_name=cinema.cinema_name,
            refund_amount=refund_amount,
            cancellation_reason=payment_info['cancels'][0]['reason']
        )
        logger.info(f"Payment cancellation response created for book_id: {book.id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in handle_payment_cancellation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")