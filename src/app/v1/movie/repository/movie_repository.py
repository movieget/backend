from tortoise.exceptions import DoesNotExist
from src.app.v1.movie.entity.movie import Movie


class MovieRepository:
    async def get_movie(self, movie_id: int) -> Movie | None:
        try:
            return await Movie.get(id=movie_id)
        except DoesNotExist:
            return None
