from pydantic import BaseModel as PydanticModel, ConfigDict
from datetime import date


class ReviewCreateRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    contents: str
    rating: int
    registration_data: date


class ReviewImageRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    review_image_url: str


class ReviewUpdateRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    review_image_url: str
    contents: str
