from tortoise import fields, models
from common.models.base_model import BaseModel


class Location(BaseModel, models.Model):
    location_id = fields.IntField(pk=True)
    spot = fields.CharField(max_length=10)
    longitude = fields.IntField()
    latitude = fields.IntField()

    def __str__(self):
        return self.name

    class Meta:
        table = "location"