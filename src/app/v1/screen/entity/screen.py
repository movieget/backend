from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Screen(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    screen_number = fields.CharField(max_length=30)
    total_seats = fields.IntField()
    cinema_id = fields.ForeignKeyField("models.Cinema", related_name="screens", null=True, on_delete=fields.CASCADE)

    def __str__(self) -> str:
        return self.screen_number

    class Meta:
        table = "screen"
