from datetime import date, time, datetime

from pydantic import BaseModel as PydanticModel, ConfigDict
from typing import List, Literal, Optional


class MovieOption(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    genre: str
    duration: int
    age_rating: str
    poster_image_url: str


class LocationOption(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    spot: str


class CinemaOption(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cinema_name: str


class ScreeningOption(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    screening_date: date
    start_time: time
    end_time: time
    screen_id: int


class BookOptionsResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int | None
    movies: List[MovieOption]
    locations: List[LocationOption]
    cinemas: List[CinemaOption]
    screenings: List[ScreeningOption]


class UpdateResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    booking_id: int  # 업데이트된 예약 ID
    status: str  # 업데이트된 상태 (예: "COMPLETED", "CANCELED")
    message: str = "예약 상태가 성공적으로 업데이트되었습니다."  # 상태 업데이트에 대한 메시지 기본 값 설정=


class SeatInfo(PydanticModel):
    column: str | None
    status: bool | None


class RowInfo(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    row: str
    seats: List[SeatInfo]


class SeatLayoutResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    screen_id: int
    rows: List[RowInfo]


class MovieScreeningInfoResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    movie_title: str
    movie_poster: str  # s3 url
    screening_date: date
    screening_time: str
    cinema: str
    location: str
    adult_count: int | None  # 사용자 입력을 위한 공란
    child_count: int | None  # 사용자 입력을 위한 공란
    selected_seats: List[str]  # 사용자 입력을 위한 공란/좌석 정보를 리스트로 관리
    total_price: int | None = None


class PriceResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    adult_count: int  # 성인 수
    child_count: int  # 청소년 수
    total_price: int  # 총 가격
    selected_seats: List[int]  # 선택한 좌석 ID 리스트


# 예매 응답


class BookResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
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


class PaymentRedirectResponse(PydanticModel):
    book_id: int
    redirect_url: str


class CompletedBookingResponse(PydanticModel):
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


class CancelledBookingResponse(PydanticModel):
    booking_id: int
    poster_url: str
    title: str
    duration: int
    booking_date: str
    screening_date: str
    age_rating: Literal["all", "12", "15", "18"]
    total_price: int
    adult_count: int
    child_count: int
    screening_time: str
    spot: str
    cinema_name: str
    screen_number: int


class SuccessBookingResponse(PydanticModel):
    book_id: str
    message: str


class FailBookingResponse(PydanticModel):
    book_id: str
    message: str


#### 취소내역 ####
class PaymentFailureResponse(PydanticModel):
    book_id: Optional[int] = None
    poster_url: str = ""
    title: str
    age_rating: str
    canceled_date: datetime
    adult_count: int = 0
    child_count: int = 0
    spot: str
    cinema_name: str
    refund_amount: int = 0
    error_code: str
    error_message: str

class PaymentCancellationResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    poster_image_url: str
    title: str
    age_rating: Literal["All", "12", "15", "18"]
    canceled_date: datetime
    adult_count: int
    child_count: int
    spot: str
    cinema_name: str
    refund_amount: float
    cancellation_reason: str

class TossWebhookPayload(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    paymentKey: str
    orderId: str
    status: str
    transactionKey: str
    lastTransactionKey: str
    requestedAt: datetime
    approvedAt: datetime
    useEscrow: bool
    cultureExpense: bool
    card: dict | None
    virtualAccount: dict | None
    transfer: dict | None
    mobilePhone: dict | None
    giftCertificate: dict | None
    cashReceipt: dict | None
    discount: dict | None
    cancels: List[dict] | None
    secret: str
    type: str
    mid: str