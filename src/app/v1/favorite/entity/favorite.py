from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Favorite(BaseModel, models.Model):
    favorite_id = fields.IntField(pk=True)
    added_at = fields.DatetimeField(auto_now_add=True)
    user_id = fields.ForeignKeyField(
        "models.User", related_name="favorite", on_delete=fields.CASCADE
    )
    movie_id = fields.ForeignKeyField(
        "models.Movie", related_name="favorite", on_delete=fields.CASCADE
    )

    class Meta:
        table = "favorite"
