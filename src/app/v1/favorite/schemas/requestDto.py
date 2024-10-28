from pydantic import BaseModel, ConfigDict


class FavoriteAddRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    movie_id: int
