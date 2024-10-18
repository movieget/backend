from tortoise import fields, models
from src.common.models.base_model import BaseModel


class ScreenInfo(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    screen_id = fields.ForeignKeyField("models.Screen", related_name="screen_infos", null=True, on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie", related_name="screen_infos", null=True, on_delete=fields.CASCADE)

    def __str__(self) -> str:
        return f"ScreenInfo {self.id}: {self.screen_id} "

    class Meta:
        table = "screen_info"
