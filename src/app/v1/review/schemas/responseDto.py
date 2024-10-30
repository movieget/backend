from pydantic import BaseModel as PydanticModel, ConfigDict, Field
from datetime import datetime


# NOTE: 전체 Review로 List 형태로 전달
# NOTE: Field의 ...은 default 값이 없음, default= 으로 변경 가능
class ReviewsResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    userProfile: str = Field(..., alias="image_url")
    userId: str = Field(..., alias="username")
    score: int = Field(..., alias="rating")
    title: str
    content: str = Field(..., alias="contents")
    reviewImage: str = Field(..., alias="review_image_url")
    creationDate: datetime = Field(..., alias="registration_date")


class ReviewImageResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    review_image_url: str


class ReviewUpdateResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    review_image_url: str
    contents: str
