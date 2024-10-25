from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Seat(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    seat_number = fields.IntField() #좌석번호
    is_selected = fields.BooleanField(default=False)# 예약 여부
    row = fields.CharField(max_length=10) # 열 번호
    column = fields.IntField() # 행(A,B,C)
    screen = fields.ForeignKeyField("models.Screen", related_name="seats", on_delete=fields.CASCADE)

    def __str__(self) -> str:
        return f"Seat {self.row}{self.column} in Screen {self.screen_id}"

    class Meta:
        table = "seat"
