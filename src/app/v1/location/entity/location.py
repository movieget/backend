from tortoise import fields, models

class Location(models.Model):
    location_id = fields.IntField(pk=True)
    spot = fields.CharField(max_length=10)
    longitude = fields.IntField()
    latitude = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table_name = "location"
