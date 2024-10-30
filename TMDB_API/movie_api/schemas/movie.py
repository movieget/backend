from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime

class MovieBase(BaseModel):
    """
    영화 정보의 기본 Pydantic 모델

    Attributes:
        title (str): 영화 제목
        genre (str): 영화 장르 (기본값: "Action")
        release_date (date): 개봉일
        duration (int): 영화 상영 시간 (분)
        rating (float): 영화 평점
        status (str): 영화 상영 상태 (기본값: "상영 중")
        image_url (str): 영화 배경 이미지 URL
        poster_image_url (str): 영화 포스터 이미지 URL
        overview (str): 영화 줄거리
        trailer_url (Optional[str]): 영화 예고편 URL (선택적)
        age_rating (str): 영화 연령 등급 (기본값: "all")
    """
    title: str = Field(..., description="영화 제목")
    genre: str = Field(default="Action", description="영화 장르")
    release_date: date = Field(..., description="개봉일")
    duration: int = Field(..., description="영화 상영 시간 (분)")
    rating: float = Field(..., description="영화 평점")
    status: str = Field(default="상영 중", description="영화 상영 상태")
    image_url: str = Field(..., description="영화 배경 이미지 URL")
    poster_image_url: str = Field(..., description="영화 포스터 이미지 URL")
    overview: str = Field(..., description="영화 줄거리")
    trailer_url: Optional[str] = Field(default="", description="영화 예고편 URL")
    age_rating: str = Field(default="all", description="영화 연령 등급")

    @validator('release_date', pre=True)
    def parse_release_date(cls, value):
        """
        release_date를 문자열에서 date 객체로 변환합니다.

        Args:
            value: 변환할 날짜 값 (문자열 또는 date 객체)

        Returns:
            date: 변환된 date 객체

        Raises:
            ValueError: 날짜 형식이 올바르지 않을 경우
        """
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value

class MovieCreate(MovieBase):
    """
    영화 생성을 위한 Pydantic 모델
    MovieBase를 상속받아 추가적인 검증이나 필드를 정의할 수 있습니다.
    """
    pass

class MovieResponse(MovieBase):
    """
    영화 응답을 위한 Pydantic 모델

    MovieBase를 상속받아 추가 필드를 포함합니다:
    id (int): 영화의 고유 식별자
    created_at (datetime): 레코드 생성 시간
    updated_at (datetime): 레코드 최종 수정 시간
    """
    id: int = Field(..., description="영화의 고유 식별자")
    created_at: datetime = Field(..., description="레코드 생성 시간")
    updated_at: datetime = Field(..., description="레코드 최종 수정 시간")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Example Movie",
                "genre": "Action",
                "release_date": "2023-01-01",
                "duration": 120,
                "rating": 8.5,
                "status": "상영 중",
                "image_url": "https://example.com/movie_image.jpg",
                "poster_image_url": "https://example.com/movie_poster.jpg",
                "overview": "This is an example movie overview.",
                "trailer_url": "https://example.com/movie_trailer",
                "age_rating": "15+",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }