import os
from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["TMDB_API.movie_api.models.movie", "TMDB_API.movie_api.models.actor_image", "aerich.models"],
            "default_connection": "default",
        },
    },
}

class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URL = TORTOISE_ORM["connections"]["default"]
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    TMDB_BASE_URL = "https://api.themoviedb.org/3"

settings = Settings()


# print(f"Database URL: {settings.DATABASE_URL}")  # 디버깅을 위해 추가