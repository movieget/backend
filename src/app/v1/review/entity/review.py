from tortoise import fields, models


class RatingEnum(str, Enum):
    one_star = "1점"
    two_star = "2점"
    three_star = "3점"
    four_star = "4점"
    five_star = "5점"


class Review(models.Model):
    review_id = fields.IntField(pk=True)#프라이머리 키 pk
    title = fields.CharField(max_length=255)
    username = fields.CharField(max_length=50)
    contents = fields.TextField()
    review_image_url = fields.CharField(max_length=50)
    rating = fields.CharEnumField(RatingEnum,max_length=50)
    registration_date = fields.DateField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user_id = fields.ForeignKeyField("models.User",related_name="reviews",on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie",related_name="reviews",on_delete=fields.CASCADE)

    class Meta:
        table = "review"