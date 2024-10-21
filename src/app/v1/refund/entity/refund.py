from tortoise import fields, models

class Refund(models.Model):
    refund_id = fields.IntField(pk=True)
    refund_amount = fields.DecimalField()
    refund_status = fields.CharEnumField()
    refund_time = fields.DatetimeField()
    payment_id =  fields.ForeignKeyField("models.payment",related_name="refund",on_delete=fields.CASCADE)

    class Meta:
        table = "refund"