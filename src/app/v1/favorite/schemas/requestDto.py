from pydantic import BaseModel, ConfigDict


class FavoriteAddRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    is_liked: bool
    movie_id: int
