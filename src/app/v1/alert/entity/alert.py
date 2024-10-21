from tortoise import fields, models, Model


class Alert(models.Model):
    alert_id = fields.BigIntField(pk=True)
    message = fields.CharField(max_length=50) # 알림 메세지
    noti_type = fields.CharField(max_length=20) # 알림 타입
    created_at = fields.DatetimeField(auto_now_add=True) #생성 일자
    updated_at = fields.DatetimeField(auto_now=True) # 업데이트
    payment_id = fields.ForeignKeyField("models.Payment",related_name="alert",on_delete=fields.CASCADE)
    #결제 상세 내용
    user_id = fields.ForeignKeyField("models.User",related_name="alert",on_delete=fields.CASCADE)
    #결제 유저
    movie_id = fields.ForeignKeyField("models.Movie",related_name="alert",on_delete=fields.CASCADE)
    #결제 영화
    class Meta:
        table = "alert"