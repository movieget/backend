from pydantic import BaseModel as PydanticModel, ConfigDict, Field
from datetime import date
from typing import List


# NOTE: 전체 Review로 List 형태로 전달
# NOTE: Field의 ...은 default 값이 없음, default= 으로 변경 가능
class ReviewsResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    image_url: str | None = Field(..., alias="userProfile")
    username: str = Field(..., alias="userId")
    rating: int = Field(..., alias="score")
    title: str
    contents: str = Field(..., alias="content")
    review_image_url: str | None = Field(..., alias="reviewImage")
    registration_date: date = Field(..., alias="creationDate")


class ReviewListResponse(PydanticModel):
    reviews: List[ReviewsResponse]
    total: int
    next_page: int | None


class ReviewCreateResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
    user_id: int
    title: str
    contents: str = Field(..., alias="content")
    rating: int = Field(..., alias="score")
    review_image_url: str | None = Field(..., alias="reviewImage")
    registration_date: date = Field(..., alias="creationDate")


class ReviewImageResponse(PydanticModel):
    reviewImage: str = Field(..., alias="review_image_url")


class ReviewUpdateResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    review_image_url: str
    contents: str
