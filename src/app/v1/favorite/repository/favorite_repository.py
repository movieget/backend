from src.app.v1.favorite.entity.favorite import Favorite
from tortoise.exceptions import DoesNotExist


class FavoriteRepository:
    @staticmethod
    async def get_favorite(user_id: int, movie_id: int) -> Favorite | None:
        return await Favorite.filter(user_id=user_id, movie_id=movie_id).first()

    @staticmethod
    async def get_user_favorites(user_id: int) -> list[Favorite]:
        return await Favorite.filter(user_id=user_id).all()

    @staticmethod
    async def add_favorite(user_id: int, movie_id: int) -> Favorite | None:
        return await Favorite.create(user_id=user_id, movie_id=movie_id)

    @staticmethod
    async def delete_favorite(user_id: int, movie_id: int) -> bool:
        try:
            favorite = await Favorite.filter(user_id=user_id, movie_id=movie_id).get()
            await favorite.delete()
            return True
        except DoesNotExist:
            return False
