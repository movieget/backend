from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Cinema(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    cinema_name = fields.CharField(max_length=30, unique=True)
    location = fields.OneToOneField("models.Location", related_name="cinema", on_delete=fields.CASCADE)

    def __str__(self):
        return self.cinema_name

    class Meta:
        table = "cinema"
