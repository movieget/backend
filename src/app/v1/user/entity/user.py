from tortoise import fields, models
from src.common.models.base_model import BaseModel


class User(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=100, unique=True)
    nickname = fields.CharField(max_length=50)
    phone_number = fields.CharField(max_length=16, null=True)
    image_url = fields.CharField(max_length=255, null=True)
    oauth_provider = fields.CharField(max_length=20)
    birthday = fields.CharField(max_length=10, null=True)
    kakao_id = fields.CharField(max_length=50, unique=True, null=True)  # 추가된 필드
    is_active = fields.BooleanField(default=True)
    is_deleted = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_login = fields.DatetimeField(null=True)

    class Meta:
        table = "user"
