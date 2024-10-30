from typing import List, Literal

from pydantic import BaseModel, ConfigDict
from datetime import date


class BookRequest(BaseModel):
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


class SeatSelectionRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    selected_seat_ids: List[str]
