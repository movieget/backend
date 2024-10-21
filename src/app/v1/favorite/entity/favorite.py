from tortoise import fields, models

class Favorite(models.Model):
    favorite_id = fields.BigIntField(pk=True)
    added_at = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    user_id = fields.ForeignKeyField("models.User", related_name="favorite", on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie", related_name="favorite", on_delete=fields.CASCADE)

    class Meta:
        table = "favorite"