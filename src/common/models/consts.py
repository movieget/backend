from enum import Enum


class RefundStatus(str, Enum):
    PENDING = "보류중"
    APPROVED = "승인됨"
    REJECTED = "거부됨"
    COMPLETED = "완료됨"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"