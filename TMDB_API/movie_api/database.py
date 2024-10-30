from tortoise import Tortoise
from TMDB_API.movie_api.config import TORTOISE_ORM

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

async def close_db():
    await Tortoise.close_connections()