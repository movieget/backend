from tortoise import fields, models


class User(models.Model):
    user_id = fields.IntField(pk=True)
    password = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)
    name = fields.CharField(max_length=30)
    points = fields.IntField()
    nickname = fields.CharField(max_length=30)
    phone_number = fields.CharField(max_length=20)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    class Meta:
        table = "users"
