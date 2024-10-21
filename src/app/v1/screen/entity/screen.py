from tortoise import fields, models

class Screen(models.Model):
    screen_id = fields.IntField(pk=True)
    screen_number = fields.CharField(max_length=30)
    total_seats = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    cinema_id = fields.ForeignKeyField("models.Cinema",related_name="screen",on_delete=fields.CASCADE)

    class Meta:
        table = "screen"
        