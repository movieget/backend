from tortoise import fields, models

"""
Tortoise ORM의 맥락에서 필드는 모델의 속성을 정의하는 데 사용되는 다양한 필드 유형을 제공하는 모듈.
필드 유형은 모델에 해당하는 데이터베이스 테이블의 열을 나타냅니다. 
Tortoise에서 필드를 가져올 때 CharField, IntField, DateField 등과 같은 다양한 필드 클래스를 사용하여 
데이터베이스 모델의 각 필드의 구조와 제약 조건을 정의할 수 있습니다
"""


class BaseModel(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abtract = True
