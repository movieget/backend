from tortoise import fields, models
from src.common.models.base_model import BaseModel
from src.common.models.consts import MoviePriceEnum, StatusEnum


class Book(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    book_time = fields.DatetimeField(auto_now_add=True)
    status = fields.CharEnumField(StatusEnum, max_length=20, default=StatusEnum.PENDING)  # CharEnumField는 적합
    # price = fields.IntEnumField(MoviePriceEnum) # 수정 필요: IntEnumField로 변경
    adult_count = fields.IntField(default=0)
    child_count = fields.IntField(default=0)
    user = fields.ForeignKeyField("models.User", related_name="books", on_delete=fields.CASCADE, null=True)
    screen_info = fields.ForeignKeyField("models.ScreenInfo", related_name="books", on_delete=fields.CASCADE, null=True)  # null 허용

    class Meta:
        table = "book"

    @property
    def movie_price(self) -> int:
        adult_price = 14000
        child_price = 12000
        return self.adult_count * adult_price + self.child_count * child_price
