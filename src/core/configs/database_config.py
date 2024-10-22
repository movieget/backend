import os

from dotenv import load_dotenv


# 환경에 따른 .env 파일 로드
load_dotenv()

Tortoise_Models = [
    "src.app.v1.user.entity.user",
    "src.app.v1.alert.entity.alert",
    "src.app.v1.book.entity.book",
    "src.app.v1.cinema.entity.cinema",
    "src.app.v1.favorite.entity.favorite",
    "src.app.v1.location.entity.location",
    "src.app.v1.movie.entity.movie",
    "src.app.v1.payment.entity.payment",
    "src.app.v1.payment.entity.payment_history",
    "src.app.v1.refund.entity.refund",
    "src.app.v1.review.entity.review",
    "src.app.v1.screen.entity.screen",
    "src.app.v1.screen.entity.screen_info",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": int(os.getenv("MYSQL_PORT", "3306")),
                "user": os.environ["MYSQL_USER"],  # 필수 값
                "password": os.environ["MYSQL_PASSWORD"],  # 필수 값
                "database": os.environ["MYSQL_DB"],  # 필수 값
                "charset": "utf8mb4",
                "use_unicode": True,
                # "timezone": "+09:00",
            },
        }
    },
    "apps": {
        "models": {
            "models": Tortoise_Models,
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Seoul",
}


class Settings:
    KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
    KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
