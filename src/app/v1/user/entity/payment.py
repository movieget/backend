from tortoise import fields
from src.common.models.base_model import BaseModel
from decimal import Decimal
from datetime import datetime
from src.common.models.consts import PaymentMethod

# 다른 모델들을 import 예제 수정 필요
from src.app.v1.user.entity.user import User
from src.app.v1.user.entity.book import Book
from src.app.v1.user.entity.refund import Refund
from app.Alert.entity.alert import Alert


class Payment(BaseModel):
    payment_id: int = fields.IntField(pk=True)
    payment_amount: Decimal = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_method: PaymentMethod = fields.CharEnumField(PaymentMethod, max_length=20)
    payment_time: datetime = fields.DatetimeField()
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    book: fields.ForeignKeyRelation[Book] = fields.ForeignKeyField('models.Book', related_name='payments')
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User', related_name='payments')
    refund: fields.ForeignKeyRelation[Refund] = fields.ForeignKeyField('models.Refund', related_name='payments',
                                                                       null=True)
    alert: fields.ForeignKeyRelation[Alert] = fields.ForeignKeyField('models.Alert', related_name='payments', null=True)

    class Meta:
        table = "payment"

    def __str__(self) -> str:
        return f"Payment {self.payment_id}: {self.payment_amount} ({self.payment_method})"


# 역참조를 위한 타입 힌트
Book.payments: fields.ReverseRelation[Payment]
User.payments: fields.ReverseRelation[Payment]
Refund.payments: fields.ReverseRelation[Payment]
Alert.payments: fields.ReverseRelation[Payment]