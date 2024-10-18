from tortoise import fields, models
from src.common.models.base_model import BaseModel


class User(BaseModel, models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password_hash = fields.CharField(max_length=128)
    email = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "users"
