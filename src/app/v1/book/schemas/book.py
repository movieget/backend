from pydantic import BaseModel
from typing import List

# 예매 요청 DTO
class BookRequest(BaseModel):
    screening_date: str  # 상영 날짜 (YYYY-MM-DD 형식)
    movie_id: int  # 영화 ID
    location_id: int # 지역 ID
    cinema_id: int  # 영화관 ID
    screen_info_id: int  # 상영 정보 (시간 포함) ID
    adult_count: int  # 성인 수
    child_count: int  # 청소년 수
    selected_seat_ids: List[int]  # 선택된 좌석 ID 리스트

    class Config:
        orm_mode = True


# 좌석 선택 DTO
class SeatSelection(BaseModel):
    seat_id: int  # 선택된 좌석의 ID
    seat_number: int  # 선택된 좌석의 번호
    is_selected: bool  # 좌석 선택 여부

    class Config:
        orm_mode = True

# 선택된 좌석 ID들의 리스트를 나타내는 스키마
class SeatSelectionRequest(BaseModel):
    selected_seat_ids: List[int]  # 선택된 좌석 ID들의 리스트

# 예매 응답
class BookResponse(BaseModel):
    book_id: int  # 예약 ID
    movie_title: str  # 영화 제목
    cinema_name: str  # 영화관 이름
    screen_number: str  # 상영관 번호
    start_time: str  # 상영 시작 시간
    end_time: str  # 상영 종료 시간
    total_price: float  # 총 결제 금액
    reserved_seats: List[SeatSelection]  # 예약된 좌석 리스트

    class Config:
        orm_mode = True


# 좌석 예약 가능 여부 응답 DTO
class SeatAvailabilityResponse(BaseModel):
    available_seats: List[SeatSelection]  # 예약 가능한 좌석 리스트
    unavailable_seats: List[SeatSelection]  # 예약 불가능한 좌석 리스트

    class Config:
        orm_mode = True


# 가격 계산
class PriceCalculation(BaseModel):
    adult_count: int  # 성인 수
    child_count: int  # 청소년 수
    total_price: int  # 총 가격

    class Config:
        orm_mode = True