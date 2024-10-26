# src/app/v1/payment/api/payment_routes.py
from fastapi import APIRouter, HTTPException, Depends
from src.app.v1.book.repository import book_repository
from src.app.v1.book.schemas.book import PaymentUpdateResponse
from src.app.v1.user.dependencies import get_current_user
from src.app.v1.user.entity.user import User

router = APIRouter()


@router.post("/payment/success", response_model=PaymentUpdateResponse)
async def payment_success(booking_id: int, user: User = Depends(get_current_user)):

    try:
        booking = await book_repository.get_booking_by_id(booking_id)
        if not booking or booking.status != "PENDING":
            raise HTTPException(status_code=400, detail="Invalid booking ID or booking not in pending status.")

        # 예약 상태를 'COMPLETED'로 업데이트
        await book_repository.update_booking_status(booking_id, "COMPLETED")
        return {"booking_id": booking_id, "status": "COMPLETED"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing booking: {str(e)}")


@router.post("/payment/fail", response_model=PaymentUpdateResponse)
async def payment_fail(booking_id: int, user=Depends(get_current_user)):
    try:
        booking = await book_repository.get_booking_by_id(booking_id)
        if not booking or booking.status != "PENDING":
            raise HTTPException(status_code=400, detail="Invalid booking ID or booking not in pending status.")

        # 예약 상태를 'CANCELLED'로 업데이트
        await book_repository.update_booking_status(booking_id, "CANCELLED")
        return {"booking_id": booking_id, "status": "CANCELLED"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling booking: {str(e)}")
