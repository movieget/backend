from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ActorImageBase(BaseModel):
    """
    배우 이미지의 기본 Pydantic 모델

    Attributes:
        image_url (str): 배우 이미지의 URL
        movie_id (Optional[int]): 관련 영화의 ID (선택적)
    """

    image_url: str = Field(..., description="배우 이미지의 URL")
    movie_id: Optional[int] = Field(None, description="관련 영화의 ID (선택적)")


class ActorImageCreate(ActorImageBase):
    """
    배우 이미지 생성을 위한 Pydantic 모델
    ActorImageBase를 상속받아 추가적인 검증이나 필드를 정의할 수 있습니다.
    """

    pass


class ActorImageResponse(ActorImageBase):
    """
    배우 이미지 응답을 위한 Pydantic 모델

    ActorImageBase를 상속받아 추가 필드를 포함합니다:
    id (int): 이미지의 고유 식별자
    created_at (datetime): 레코드 생성 시간
    updated_at (datetime): 레코드 최종 수정 시간
    """

    id: int = Field(..., description="이미지의 고유 식별자")
    created_at: datetime = Field(..., description="레코드 생성 시간")
    updated_at: datetime = Field(..., description="레코드 최종 수정 시간")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "image_url": "https://example.com/actor_image.jpg",
                "movie_id": 123,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
            }
        }
