from tortoise import fields, models

class Screen_Info(models.Model):
    screen_info_id = fields.IntField(pk=True)
    start_time = fields.DatetimeField(auto_now=False, auto_now_add=False)
    end_time = fields.DatetimeField(auto_now=False, auto_now_add=False)
    created_at = fields.DatetimeField(auto_now=False, auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=False, auto_now_add=True)
    screen_id = fields.ForeignKeyField("models.Screen",related_name="screen_info",on_delete=fields.CASCADE)
    movie_id = fields.ForeignKeyField("models.Movie",related_name="screen_info",on_delete=fields.CASCADE)

    class Meta:
        table = "screen_info"
        