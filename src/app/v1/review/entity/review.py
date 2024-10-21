from tortoise import fields, models
from src.common.models.base_model import BaseModel
from src.common.models.consts import RatingEnum


class Review(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    username = fields.CharField(max_length=20)
    contents = fields.TextField(null=False)
    review_image_url = fields.CharField(max_length=50)
    rating = fields.CharEnumField(RatingEnum, max_length=20, default=RatingEnum.no_star)
    registration_date = fields.DateField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="reviews", on_delete=fields.CASCADE)
    movie = fields.ForeignKeyField("models.Movie", related_name="reviews", on_delete=fields.CASCADE)

    class Meta:
        table_name = "review"
