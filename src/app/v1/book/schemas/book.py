from datetime import date, datetime, time

from pydantic import BaseModel
from typing import List, Optional

class MovieOption(BaseModel):
    id: int
    title: str
    genre: str
    duration: int
    age_rating: str
    poster_image_url: str
    class Config:
        orm_mode = True
class LocationOption(BaseModel):
    id: int
    spot: str
    class Config:
        orm_mode = True
class CinemaOption(BaseModel):
    id: int
    cinema_name: str
    class Config:
        orm_mode = True
class ScreeningOption(BaseModel):
    id: int
    screening_date: date
    start_time: time
    end_time: time
    class Config:
        orm_mode = True
class BookOptionsResponse(BaseModel):
    book_id: int
    movies: List[MovieOption]
    locations: List[LocationOption]
    cinemas: List[CinemaOption]
    screenings: List[ScreeningOption]
    class Config:
        orm_mode = True

class SeatResponse(BaseModel):
    seat_number: int
    is_selected: bool
    row: str
    column: int

class Row(BaseModel):
    row: str
    seats: List[Optional[SeatResponse]]

class SeatLayoutResponse(BaseModel):
    screen_id: int
    rows: List[Row]

    class Config:
        orm_mode = True



class MovieScreeningInfoResponse(BaseModel):
    movie_title: str
    movie_poster: str #s3 url
    screening_date: date
    screening_time: str
    cinema: str
    location: str
    adult_count: Optional[int]  # 사용자 입력을 위한 공란
    child_count: Optional[int]  # 사용자 입력을 위한 공란
    selected_seats: List[str]  # 사용자 입력을 위한 공란/좌석 정보를 리스트로 관리
    total_price: Optional[int]
    class Config:
        orm_mode = True

class PaymentResponse(BaseModel):
    booking_id: int
    redirect_url: str
    class Config:
        orm_mode = True
# 예매 요청 DTO
class BookRequest(BaseModel):
    screening_date: date  # 상영 날짜 (YYYY-MM-DD 형식)
    movie_id: int  # 영화 ID
    location_id: int # 지역 ID
    cinema_id: int  # 영화관 ID
    screen_info_id: int  # 상영 정보 (시간 포함) ID
    adult_count: int  # 성인 수
    child_count: int  # 청소년 수
    selected_seat_ids: List[int]  # 선택된 좌석 ID 리스트
    class Config:
        orm_mode = True


# 선택된 좌석 ID들의 리스트를 나타내는 스키마
class SeatSelectionRequest(BaseModel):
    selected_seat_ids: List[str]  # 좌석 ID 목록, 예: ["a1", "a2"]
    class Config:
        orm_mode = True

class PriceResponse(BaseModel):
    adult_count: int  # 성인 수
    child_count: int  # 청소년 수
    total_price: int  # 총 가격
    selected_seats: List[int]  # 선택한 좌석 ID 리스트

    class Config:
        orm_mode = True

# 예매 응답

class BookResponse(BaseModel):
    poster_url: str  # 포스터 URL
    movie_info: str  # 영화 이름 및 연령 제한 (예: "영화이름, 12세 이상")
    booking_date: date  # 예매일
    screening_date: date  # 상영일
    seats: List[str]  # 좌석 목록 (예: ["a1", "a2"])
    total_price: int  # 총 가격
    person_count: str  # 인원수 (예: "성인3 / 청소년3")
    screening_time: str  # 상영 시간
    location: str  # 지점 정보
    cinema: str  # 상영관 정보
    class Config:
        orm_mode = True

class PaymentUpdateResponse(BaseModel):
    booking_id: int
    status: str
    class Config:
        orm_mode = True





