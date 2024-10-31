from pydantic import BaseModel as PydanticModel, ConfigDict


class FavoriteAddRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    is_liked: bool
    movie_id: int

class FavoriteCheckRequest(PydanticModel):
    model_config = ConfigDict(from_attributes=True)
    movie_id: int