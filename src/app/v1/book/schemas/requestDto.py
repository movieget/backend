from typing import List, Literal
from pydantic import BaseModel as PydanticModel, ConfigDict


class BookRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    booking_id: int
    poster_url: str
    title: str
    duration: int
    booking_date: str
    screening_date: str
    age_rating: Literal["all", "12", "15", "18"]
    seats: List[str]
    total_price: int
    adult_count: int
    child_count: int
    screening_time: str
    spot: str
    cinema_name: str
    screen_number: int


class SuccessBookingRequest(PydanticModel):
    book_id: str
    poster_url: str
    title: str
    duration: int
    booking_date: str
    screening_date: str
    age_rating: str
    seats: List[str]
    total_price: int
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


class FailBookingRequest(PydanticModel):
    book_id: str
    poster_url: str
    title: str
    duration: int
    booking_date: str
    screening_date: str
    age_rating: str
    seats: List[str]
    total_price: int
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


class SeatSelectionRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    selected_seat_ids: List[str]


class UsePointsRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    book_id: int
    total_point: int
