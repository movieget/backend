from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Favorite(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    added_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="favorites", null=True, on_delete=fields.CASCADE)
    movie = fields.ForeignKeyField("models.Movie", related_name="favorite_by", null=True, on_delete=fields.CASCADE)

    class Meta:
        table = "favorite"
