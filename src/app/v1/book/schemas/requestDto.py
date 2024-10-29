from typing import List

from pydantic import BaseModel, ConfigDict
from datetime import date

class BookRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    screening_date: date
    movie_id: int
    location_id: int
    cinema_id: int
    screen_info_id: int
    adult_count: int
    child_count: int
    selected_seat_ids: List[int]


class SeatSelectionRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    selected_seat_ids: List[str]




