import os
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

Tortoise_Models = [
    "app.v1.user.entity.user",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("MYSQL_HOST"),
                "port": int(os.getenv("MYSQL_PORT")),
                "user": os.getenv("MYSQL_USER"),
                "password": os.getenv("MYSQL_PASSWORD"),
                "database": os.getenv("MYSQL_DB"),
            },
        }
    },
    "apps": {
        "models": {
            "models": Tortoise_Models,
            "default_connection": "default",
        },
    },
    # "routers": ["app.configs.database_config.Router"],
    "timezone": "Asia/Seoul",
}


def database_initialize(app: FastAPI) -> None:
    Tortoise.init_models(Tortoise_Models, "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
