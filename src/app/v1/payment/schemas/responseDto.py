from pydantic import BaseModel as PydanticModel
from typing import List


class PaymentResponse(PydanticModel):
    book_id: str
    poster_url: str
    title: str
    duration: int
    booking_date: str
    screening_date: str
    age_rating: str
    seats: List[str]
    adult_count: int
    child_count: int
    screening_time: str
    spot: str
    cinema_name: str
    screen_number: str
    adult_count: int
    child_count: int
    paymentKey: str
    orderId: str
    amount: int


class PaymentErrorResponse(PydanticModel):
    code: str
    message: str
