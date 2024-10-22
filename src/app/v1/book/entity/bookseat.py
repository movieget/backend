from tortoise import fields, models
from src.common.models.base_model import BaseModel


class BookSeat(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    book = fields.ForeignKeyField("models.Book", related_name="book_seats", on_delete=fields.CASCADE)
    seat = fields.ForeignKeyField("models.Seat", related_name="book_seats", on_delete=fields.CASCADE)

    class Meta:
        table = "book_seat"
