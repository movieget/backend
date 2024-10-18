from tortoise import fields, models
from src.common.models.base_models import BaseModel
from src.common.models.base_models.constant import RatingEnum

class Review(BaseModel, models.Model):
    review_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    username = fields.CharField(max_length=20)
    contents = fields.TextField(null=False)
    review_image_url = fields.CharField(max_length=50)
    rating = fields.CharEnumField(RatingEnum, max_length=20, default=RatingEnum.no_star)
    registration_date = fields.DateField
    user_id = fields.ForeignKeyField("models.User", related_name="reviews", on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie", related_name="reviews", on_delete=fields.CASCADE)

    class Meta:
        table_name = 'reviews'