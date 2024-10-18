from tortoise import fields, models
from common.models.base_model import BaseModel


class Movie(BaseModel, models.Model):
    movie_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    genre = fields.CharEnumField()
    release_data = fields.DateField()
    duration = fields.IntField()
    rating = fields.IntField()
    status = fields.CharEnumField()
    image_url = fields.CharField(max_length=100)
    poster_image_url = fields.CharField(max_length=100)
    actor_Image_url = fields.CharField(max_length=100)
    overview = fields.TextField()
    trailer_url = fields.CharField(max_length=100)
    age_rating = fields.IntEnumField()

    def __str__(self):
        return self.title

    class Meta:
        table = 'movie'