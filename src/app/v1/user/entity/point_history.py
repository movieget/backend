from tortoise import fields, models

class PointHistory(models.Model):
    id = fields.IntField(pk=True)
    change_type = fields.CharField(max_length=10)
    points = fields.IntField()
    description = fields.CharField(max_length=30)
    created_at = fields.DatetimeField(auto_now_add=True)
    payment = fields.ForeignKeyField("models.Payment", related_name="point_histories", null=True,
                                     on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="point_histories")
    class Meta:
        table = "point_history"
