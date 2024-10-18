from enum import Enum

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