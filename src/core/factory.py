from fastapi import Depends

# 서비스와 리포지토리 임포트
from src.app.v1.favorite.service.favorite_service import FavoriteService
from src.app.v1.favorite.repository.favorite_repository import FavoriteRepository
from src.app.v1.user.repository.user_repository import UserRepository, PointRepository
from src.app.v1.movie.repository.movie_repository import MovieRepository
from src.app.v1.review.service.review_service import ReviewService
from src.app.v1.review.repository.review_repository import ReviewRepository
from src.app.v1.book.service.book_service import BookService
from src.app.v1.book.repository.book_repository import BookRepository
from src.app.v1.screen.repository.screeninfo_repository import ScreenInfoRepository


# 의존성 주입을 위한 factory 함수
def get_favorite_service(
    user_repository: UserRepository = Depends(),
    movie_repository: MovieRepository = Depends(),
    favorite_repository: FavoriteRepository = Depends(),
) -> FavoriteService:
    return FavoriteService(user_repository, movie_repository, favorite_repository)


def get_review_service(
    review_repository: ReviewRepository = Depends(),
    movie_repository: MovieRepository = Depends(),
    user_repository: UserRepository = Depends(),
) -> ReviewService:
    return ReviewService(review_repository, movie_repository, user_repository)


def get_book_service(
    book_repository: BookRepository = Depends(),
    screeninfo_repository: ScreenInfoRepository = Depends(),
    point_repository: PointRepository = Depends(),
) -> BookService:
    return BookService(book_repository, screeninfo_repository, point_repository)
