from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from TMDB_API.movie_api.api.movies import router as movies_router
from TMDB_API.movie_api.api.actors import router as actors_router
from TMDB_API.movie_api.api.etl import router as etl_router
from TMDB_API.movie_api.config import TORTOISE_ORM
import uvicorn

app = FastAPI()

app.include_router(movies_router, prefix="/movies", tags=["movies"])
app.include_router(actors_router, prefix="/actors", tags=["actors"])
app.include_router(etl_router, prefix="/etl", tags=["etl"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Aerich가 스키마를 관리할 것이므로 False로 설정
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
