from pydantic import BaseModel as PydanticModel
from datetime import date


class PaymentRequest(PydanticModel):
    book_id: str
    poster: str
    age: str
    duration: int
    title: str
    date: date
    start_time: str
    location: str
    cinema: str
    screen_id: str
    screening_date: str
    adult_count: str
    child_count: str
    paymentKey: str
    orderId: str
    amount: int
