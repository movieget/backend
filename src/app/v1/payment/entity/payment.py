from tortoise import fields, models
from src.common.models.base_model import BaseModel
from decimal import Decimal
from datetime import datetime
from src.common.models.consts import PaymentMethod


class Payment(BaseModel, models.Model):
    # payment_id: int = fields.IntField(pk=True)
    payment_amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_method: PaymentMethod = fields.CharEnumField(PaymentMethod, max_length=20)
    payment_time: datetime = fields.DatetimeField()

    user = fields.ForeignKeyField("models.User", related_name="payments", null=True, on_delete=fields.CASCADE)
    book = fields.ForeignKeyField("models.Book", related_name="payments", on_delete=fields.CASCADE)

    class Meta:
        table = "payment"

    def __str__(self) -> str:
        return f"Payment {self.payment_id}: {self.payment_amount} ({self.payment_method})"
