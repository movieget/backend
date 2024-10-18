from datetime import datetime

from tortoise import fields, models
from src.common.models.base_model import BaseModel


class PaymentHistory(BaseModel, models.Model):
    id: int = fields.IntField(pk=True)
    contents: str = fields.CharField(max_length=20)

    # Payment와의 관계
    payment = fields.ForeignKeyField("models.Payment", related_name="histories", null=True)

    class Meta:
        table = "payment_history"

    def __str__(self) -> str:
        return f"Payment History {self.history_id}: {self.contents}"


# Payment 모델에 역참조 타입 힌트 추가
# Payment.histories: fields.ReverseRelation[PaymentHistory]
