from pydantic import BaseModel as PydanticModel, ConfigDict
from datetime import date

# from fastapi import UploadFile


class ReviewCreateRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    contents: str
    rating: int
    registration_data: date


# class ReviewImageRequest(PydanticModel):
#     model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
#     user_id: int
#     image_file: UploadFile


class ReviewUpdateRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    review_image_url: str
    contents: str
