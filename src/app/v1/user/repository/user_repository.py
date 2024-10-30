from tortoise.exceptions import DoesNotExist
from src.app.v1.user.entity.user import User


class UserRepository:
    async def get_user(self, user_id: int) -> User | None:
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None

    async def get_kakao_user(self, kakao_id: int) -> User | None:
        try:
            return await User.get(kakao_id=kakao_id)
        except DoesNotExist:
            return None

    async def create_user(
        self, username: str, email: str, nickname: str, birthday: str, phone_number: str, oauth_provider: str, image_url: str, kakao_id: int
    ) -> User:
        # 새 유저 생성
        return await User.create(
            username=username,
            email=email,
            nickname=nickname,
            birthday=birthday,
            phone_number=phone_number,
            oauth_provider=oauth_provider,
            image_url=image_url,
            kakao_id=kakao_id,
        )
