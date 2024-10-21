from tortoise import fields, models

class Payment(models.Model):
    payment_id = fields.IntField(pk=True)
    payment_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    payment_method = fields.CharEnumField()
    payment_time = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    book_id = fields.ForeignKeyField("models.Book",related_name="payment",on_delete=fields.CASCADE)
    user_id = fields.ForeignKeyField("models.User",related_name="payment",on_delete=fields.CASCADE)
    refund_id = fields.ForeignKeyField("models.Refund",related_name="payment",on_delete=fields.CASCADE)
    alert_id = fields.ForeignKeyField("models.Alert",related_name="payment",on_delete=fields.CASCADE)

    class Meta:
        table = "payment"

