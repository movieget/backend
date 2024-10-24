from tortoise import fields, models
from src.common.models.base_model import BaseModel
from src.common.models.consts import RefundStatus


class Refund(BaseModel, models.Model):
    refund_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    refund_status = fields.CharEnumField(RefundStatus, max_length=20)  # 수정 필요: IntEnumField로 변경
    refund_time = fields.DatetimeField(auto_now_add=True)
    payment = fields.OneToOneField("models.Payment", related_name="refunds", null=True)

    class Meta:
        table = "refund"

    def __str__(self) -> str:
        return f"Refund {self.refund_id}: {self.refund_amount} ({self.refund_status})"


# Payment 모델에 역참조 타입 힌트 추가
# Payment 모델에 역참조 타입 힌트 추가
# Payment.refunds: fields.ReverseRelation[Refund]
