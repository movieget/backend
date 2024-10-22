from tortoise import fields, models
from src.common.models.base_model import BaseModel


class ActorImage(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    image_url = fields.CharField(max_length=255)
    movie = fields.ForeignKeyField("models.Movie", related_name="actor_images", null=True, on_delete=fields.CASCADE)

    class Meta:
        table = "actor_image"
