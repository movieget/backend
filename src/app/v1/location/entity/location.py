from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Location(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    spot = fields.CharField(max_length=20)
    longitude = fields.FloatField(null=True)
    latitude = fields.FloatField(null=True)

    def __str__(self):
        return self.spot

    class Meta:
        table = "location"
