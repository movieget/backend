from datetime import datetime

from tortoise import fields, models
from decimal import Decimal

from app.common.consts import RefundStatus
from Payment.entity.payment import Payment


class Refund(models.Model):
    refund_id: int = fields.IntField(pk=True)
    refund_amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    refund_status: RefundStatus = fields.CharEnumField(RefundStatus, max_length=20)
    refund_time: datetime = fields.DatetimeField(auto_now_add=True)
    payment: fields.ForeignKeyRelation[Payment] = fields.ForeignKeyField('models.Payment', related_name='refunds')

    class Meta:
        table = "refund"

    def __str__(self) -> str:
        return f"Refund {self.refund_id}: {self.refund_amount} ({self.refund_status})"

# Payment 모델에 역참조 타입 힌트 추가
Payment.refunds: fields.ReverseRelation[Refund]