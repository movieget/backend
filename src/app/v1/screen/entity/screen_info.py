from tortoise import fields, models
from src.common.models.base_model import BaseModel


class ScreenInfo(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    screening_date = fields.DateField()
    start_time = fields.TimeField()
    end_time = fields.TimeField()
    screen = fields.ForeignKeyField("models.Screen", related_name="screen_infos", on_delete=fields.CASCADE)
    movie = fields.ForeignKeyField(
        "models.Movie", related_name="screen_infos",
        on_delete=fields.CASCADE
    )

    def __str__(self) -> str:
        return f"ScreenInfo {self.id}: {self.screen_id} "

    class Meta:
        table = "screen_info"
