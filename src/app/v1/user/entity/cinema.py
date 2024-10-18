from tortoise import fields, models
from common.models.base_model import BaseModel


class Cinema(BaseModel, models.Model):
    cinema_id = fields.IntField(pk=True)
    cinema_name = fields.CharField(max_length=30, unique=True)
    location_id = fields.OneToOneField(
        "models.Location", related_name="cinemas", on_delete=fields.CASCADE
    )

    def __str__(self):
        return self.cinema_name

    class Meta:
        table = "cinema"
