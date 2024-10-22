from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from src.core.configs.database_config import TORTOISE_ORM


async def database_initialize(app: FastAPI) -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
    await Tortoise.generate_schemas()
