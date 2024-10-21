from tortoise import fields, models

class Cinema(models.Model):
    cinema_id = fields.IntField(pk=True)
    cinema_name = fields.CharField(max_length=30)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    location = fields.ForeignKeyField("models.Location",related_name="cinema",on_delete=fields.CASCADE)

    class Meta:
        table = "cinema"