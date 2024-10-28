from fastapi import Depends

# 서비스와 리포지토리 임포트
from src.app.v1.favorite.service.favorite_service import FavoriteService
from src.app.v1.favorite.repository.favorite_repository import FavoriteRepository
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.movie.repository.movie_repository import MovieRepository


# 의존성 주입을 위한 factory 함수
def get_favorite_service(
    favorite_repository: FavoriteRepository = Depends(),
    user_repository: UserRepository = Depends(),
    movie_repository: MovieRepository = Depends(),
) -> FavoriteService:
    return FavoriteService(favorite_repository, user_repository, movie_repository)
