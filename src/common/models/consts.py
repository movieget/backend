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


class RatingEnum(int, Enum):
    no_star = 0
    one_star = 1
    two_star = 2
    three_star = 3
    four_star = 4
    five_star = 5


class StatusEnum(str, Enum):
    PENDING = "진행중"  # 또는 대기 중
    COMPLETED = "완료"
    CANCELLED = "취소"


class MoviePriceEnum(int, Enum):  # IntEnum으로 사용해야 함
    adult = 14000  # 정수 값 유지
    child = 12000


class MovieGenreEnum(str, Enum):
    ACTION = "액션"
    DRAMA = "드라마"
    COMEDY = "코미디"
    HORROR = "공포"
    SCIFI = "SF"
    ROMANCE = "로맨스"
    ADVENTURE = "모험"
    ANIMATION = "애니메이션"
    FANTASY = "판타지"
    CRIME = "범죄"
    DOCUMENTARY = "다큐멘터리"
    MYSTERY = "미스터리"
    WAR = "전쟁"
    THRILLER = "스릴러"


class MovieStatusEnum(str, Enum):
    NOW_SHOWING = "상영 중"
    COMING_SOON = "개봉 예정"
    ENDED = "상영 종료"


class MovieAgeRatingEnum(str, Enum):
    ALL = "ALL"
    TWELVE = "12"
    FIFTEEN = "15"
    EIGHTEEN = "18"
