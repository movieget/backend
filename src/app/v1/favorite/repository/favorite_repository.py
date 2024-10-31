from src.app.v1.favorite.entity.favorite import Favorite
from typing import List


class FavoriteRepository:
    @staticmethod
    async def get_favorite(user_id: int, movie_id: int) -> Favorite | None:
        return await Favorite.filter(user_id=user_id, movie_id=movie_id).first()

    @staticmethod
    async def get_user_favorites(user_id: int) -> List[Favorite]:
        return await Favorite.filter(user_id=user_id).all()

    @staticmethod
    async def add_favorite(user_id: int, movie_id: int) -> Favorite | None:
        return await Favorite.create(user_id=user_id, movie_id=movie_id)
