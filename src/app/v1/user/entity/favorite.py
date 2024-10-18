from tortoise import fields, models
from src.common.models.base_models import BaseModel

class Favorite(BaseModel, models.Model):
    favorite_id = fields.IntField(pk=True)
    added_at = fields.DatetimeField(auto_now_add=True)
    user_id = fields.ForeignKeyField("models.User", related_name="favorites", on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie", related_name="favorites", on_delete=fields.CASCADE)

    class Meta:
        table_name = 'favorites'