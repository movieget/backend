from tortoise import fields, models

class Seat(models.Model):
    seat_id = fields.IntField(pk=True)
    seat_number = fields.IntField()
    is_selected = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    screen_id = fields.ForeignKeyField("models.Screen",related_name="seat",on_delete=fields.CASCADE)

    class Meta:
        table = "seat"
