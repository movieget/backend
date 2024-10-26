# src/app/v1/payment/api/payment_routes.py
from fastapi import APIRouter, HTTPException
from src.app.v1.payment.service.payment_service import initiate_payment
from src.app.v1.book.repository import book_repository
from src.app.v1.book.schemas.book import BookRequest
from src.app.v1.book.schemas.book import PaymentResponse

router = APIRouter()

@router.post("/payment", response_model=PaymentResponse)
async def create_reservation_and_redirect_to_payment(booking_data: BookRequest):
    try:
        # 임시 예약 저장 (PENDING 상태)
        temporary_booking = await book_repository.create_booking({
            "user_id": booking_data.user_id,
            "status": "PENDING",
            "screen_info_id": booking_data.screen_info_id,
            "adult_count": booking_data.adult_count,
            "child_count": booking_data.child_count,
            "selected_seat_ids": booking_data.selected_seat_ids
        })

        # TossPay 결제 URL 생성
        payment_url = initiate_payment(temporary_booking)
        if not payment_url:
            raise HTTPException(status_code=500, detail="Failed to initiate payment")

        return {"booking_id": temporary_booking.id, "redirect_url": payment_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing payment: {str(e)}")
