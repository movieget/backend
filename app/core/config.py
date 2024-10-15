import os

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

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
            "models": [
                "app.entity.user",
                "app.entity.event",
                "app.entity.movie",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
