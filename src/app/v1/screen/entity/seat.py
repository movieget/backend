from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Seat(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    seat_number = fields.IntField()
    is_selected = fields.BooleanField(default=False)
    screen_id = fields.ForeignKeyField("models.Screen", related_name="seats")

    def __str__(self) -> str:
        return str(self.seat_number)

    class Meta:
        table = "seat"
