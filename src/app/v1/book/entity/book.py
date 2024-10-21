from tortoise import fields, models
import datetime as dt


class Book(models.Model):
    book_id = fields.IntField(pk=True)
    book_time = fields.DatetimeField(auto_now_add=True) # 예약시간
    movie_id = fields.IntField() #영화 제목
    adult_count = fields.IntField(default=0) # 성인
    child_count = fields.IntField(default=0) # 유아
    total_price = fields.DecimalField(max_digits=10, decimal_places=2) # 총 결제 가격
    status = fields.CharField(max_length=50, default='예약 대기 중') # 결제 상태(결제중, 결제완료 상태도 필요한지?)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Meta:
    table_name = "book"