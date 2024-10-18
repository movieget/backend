from tortoise import fields, models
from common.models.base_model import BaseModel


class SreenInfo(BaseModel, models.Model):
    screen_info_id = fields.IntField(pk=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    screen_id = fields.ForeignKeyField(
        "models.Screen", related_name="Sreen_Info", on_delete=fields.CASCADE
    )
    location_id = fields.ForeignKeyField(
        "models.Movie", related_name="Sreen_Info", on_delete=fields.CASCADE
    )
