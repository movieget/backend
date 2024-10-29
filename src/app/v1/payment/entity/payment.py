from tortoise import fields, models
from src.common.models.base_model import BaseModel


class Payment(BaseModel, models.Model):
    paymentKey = fields.CharField(max_length=50)
    orderId = fields.CharField(max_length=50)
    amount = fields.IntField()

    user = fields.ForeignKeyField("models.User", related_name="payments", null=True, on_delete=fields.CASCADE)
    book = fields.ForeignKeyField("models.Book", related_name="payments", on_delete=fields.CASCADE)

    class Meta:
        table = "payment"
