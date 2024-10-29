from fastapi import Query, HTTPException
from tortoise.exceptions import DoesNotExist
from src.app.v1.user.entity.user import User


class UserRepository:
    async def get_user(self, user_id: int) -> User | None:
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None


