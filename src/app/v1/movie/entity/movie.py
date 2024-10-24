from tortoise import fields, models
from src.common.models.base_model import BaseModel
from src.common.models.consts import MovieGenreEnum, MovieStatusEnum, MovieAgeRatingEnum


class Movie(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    genre = fields.CharEnumField(MovieGenreEnum, default=MovieGenreEnum.ACTION)  # CharEnumField는 적합
    release_data = fields.DateField()
    duration = fields.IntField()
    rating = fields.IntField()
    status = fields.CharEnumField(MovieStatusEnum, default=MovieStatusEnum.NOW_SHOWING)  # CharEnumField는 적합
    image_url = fields.CharField(max_length=100)
    poster_image_url = fields.CharField(max_length=255)
    overview = fields.TextField()
    trailer_url = fields.CharField(max_length=100)
    age_rating = fields.CharEnumField(MovieAgeRatingEnum, default=MovieAgeRatingEnum.ALL)  # CharEnumField는 적합

    def __str__(self):
        return self.title

    class Meta:
        table = "movie"
