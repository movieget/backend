from datetime import datetime

from tortoise import fields
from src.common.models.base_model import BaseModel

from typing import Optional

from src.app.v1.user.entity.payment import Payment


class PaymentHistory(BaseModel):
    history_id: int = fields.IntField(pk=True)
    contents: str = fields.CharField(max_length=20)

    # Payment와의 관계
    payment: Optional[fields.ForeignKeyRelation[Payment]] = fields.ForeignKeyField(
        'app.payment.entity.payment.Payment',
        related_name='histories',
        null=True
    )

    class Meta:
        table = "payment_history"

    def __str__(self) -> str:
        return f"Payment History {self.history_id}: {self.contents}"

# Payment 모델에 역참조 타입 힌트 추가
# Payment.histories: fields.ReverseRelation[PaymentHistory]