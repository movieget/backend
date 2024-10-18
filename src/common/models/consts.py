from enum import Enum


class RefundStatus(str, Enum):
    PENDING = "보류중"
    APPROVED = "승인됨"
    REJECTED = "거부됨"
    COMPLETED = "완료됨"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"


class RatingEnum(str, Enum):
    no_star = "☆☆☆☆☆"
    one_star = "★☆☆☆☆"
    two_star = "★★☆☆☆"
    three_star = "★★★☆☆"
    four_star = "★★★★☆"
    five_star = "★★★★★"


class StatusEnum(str, Enum):
    PENDING = "진행 중"  # 또는 대기 중
    COMPLETED = "완료"
    CANCELLED = "취소"


class MoviePriceEnum(str, Enum):
    adult = "14000"
    child = "12000"


class MovieGenreEnum(str, Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    HORROR = "Horror"
    SCIFI = "Sci-Fi"
    ROMANCE = "Romance"


class MovieStatusEnum(str, Enum):
    NOW_SHOWING = "상영 중"
    COMING_SOON = "상영 예정"
    ENDED = "상영 종료"

class MovieAgeRatingEnum(int, Enum):
    basic = 12
    middle = 15
    high = 18