from pydantic import BaseModel, ConfigDict
from typing import List

"""# NOTE
일반적으로, Entity에 created_at이 있다면 이 값은 이미 데이터베이스에서 설정되어 있을 것입니다. 
DTO로 변환할 때 이 값을 그대로 사용하면 됩니다. Pydantic의 from_attributes = True 설정 (이전의 orm_mode = True)을 사용하면, 
ORM 모델의 속성을 자동으로 DTO 필드에 매핑해줍니다
"""


class FavoriteItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    movie_id: int


class UserFavoritesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    favorites: List[FavoriteItemResponse]
    total_count: int


class FavoriteAddResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    movie_id: int
