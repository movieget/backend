from tortoise import fields, models

class Movie(models.Model):
    movie_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=30)
    genre = fields.CharEnumField()
    release_data = fields.DatetimeField()
    duration = fields.IntField()
    rating = fields.IntField()
    status = fields.CharEnumField()
    image_url = fields.CharField(max_length=100)
    poster_image_url = fields.CharField(max_length=100)
    actor_image_url = fields.CharField(max_length=100)
    overview = fields.TextField()
    trailer_url = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

