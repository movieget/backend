from tortoise import fields, models
from src.common.models.base_model import BaseModel
from src.common.models.consts import PaymentMethod


class Payment(BaseModel, models.Model):
    payment_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_method = fields.CharEnumField(PaymentMethod, max_length=20)  # 수정 필요: IntEnumField로 변경
    payment_time = fields.DatetimeField()

    user = fields.ForeignKeyField("models.User", related_name="payments", null=True, on_delete=fields.CASCADE)
    book = fields.ForeignKeyField("models.Book", related_name="payments", on_delete=fields.CASCADE)

    class Meta:
        table = "payment"

    def __str__(self) -> str:
        return f"Payment {self.payment_id}: {self.payment_amount} ({self.payment_method})"
