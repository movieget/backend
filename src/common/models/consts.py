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
    no_star = "0"
    one_star = "1"
    two_star = "2"
    three_star = "3"
    four_star = "4"
    five_star = "5"


class StatusEnum(str, Enum):
    PENDING = "pending"  # 또는 대기 중
    COMPLETED = "completed"
    CANCELED = "canceled"


class MoviePriceEnum(int, Enum):  # IntEnum으로 사용해야 함
    adult = 14000  # 정수 값 유지
    child = 12000


class MovieGenreEnum(str, Enum):
# 액션, 전쟁, 코미디, 판타지
    ACTION = "액션"
    WAR = "전쟁"
    DRAMA = "드라마"
    COMEDY = "코미디"
    HORROR = "공포"
    SCIFI = "SF"
    ROMANCE = "로맨스"
    ADVENTURE= "모험"
    DOCUMENTARY = "다큐멘터리"
    MYSTERY = "미스터리"
    THRILLER = "스릴러"
    ANIMATION = "애니메이션"


class MovieStatusEnum(str, Enum):
    NOW_SHOWING = "상영 중"
    COMING_SOON = "상영 예정"
    ENDED = "상영 종료"


class MovieAgeRatingEnum(str, Enum):
    ALL = "All"
    AGE_12 = "12"
    AGE_15 = "15"
    AGE_18 = "18"


