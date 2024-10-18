from tortoise import fields, models
from src.common.models.base_models import BaseModel

class Alert(BaseModel, models.Model):
    alert_id = fields.IntField(pk=True)
    message = fields.CharField(max_length=50)
    noti_type = fields.CharField(max_length=20)
    user_id = fields.ForeignKeyField("models.User", related_name="alerts", on_delete=fields.CASCADE)
    book_id = fields.ForeignKeyField("models.Book", related_name="alerts", on_delete=fields.CASCADE)
    payment_id = fields.ForeignKeyField("models.Payment", related_name="alerts", on_delete=fields.CASCADE)

    class Meta:
        table_name = 'alerts'