from pydantic import BaseModel as PydanticModel, ConfigDict
from src.app.v1.movie.schemas.movie_schema import MovieListItem
from typing import List, Dict, Optional

"""# NOTE
일반적으로, Entity에 created_at이 있다면 이 값은 이미 데이터베이스에서 설정되어 있을 것입니다. 
DTO로 변환할 때 이 값을 그대로 사용하면 됩니다. Pydantic의 from_attributes = True 설정 (이전의 orm_mode = True)을 사용하면, 
ORM 모델의 속성을 자동으로 DTO 필드에 매핑해줍니다
"""


class FavoriteItemResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    movie_id: int


class FavoriteItemResponse(MovieListItem):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FavoriteMovieResponse(PydanticModel):
    favorite_id: int
    movie_id: int
    is_liked: bool
    title: str
    poster_image: str
    age_rating: str
    genre: str
    overview: Optional[str] = None
    trailer_url: Optional[str] = None
    duration: Optional[int] = None
    rating: Optional[int] = None
    total_likes: int


class UserFavoritesResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    favorites: List[FavoriteMovieResponse]
    # total_count: int


class FavoriteAddResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_liked: bool
    user_id: int
    movie_id: int


class FavortieCheckResponse(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    is_liked: bool
    user_id: int
    movie_id: int
