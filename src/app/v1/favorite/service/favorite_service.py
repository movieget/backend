from typing import List

from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.movie.repository.movie_repository import MovieRepository
from src.app.v1.favorite.repository.favorite_repository import FavoriteRepository
from src.app.v1.favorite.entity.favorite import Favorite
from src.common.handlers.exception_handler import BusinessException, ErrorCode
from src.app.v1.favorite.schemas.responseDto import FavoriteItemResponse, UserFavoritesResponse, FavoriteAddResponse, FavoriteMovieResponse
from src.app.v1.favorite.schemas.requestDto import FavoriteAddRequest
from src.app.v1.favorite.entity.favorite import Favorite


class FavoriteService:
    def __init__(self, user_repository: UserRepository, movie_repository: MovieRepository, favorite_repository: FavoriteRepository):
        self.user_repository = user_repository
        self.movie_repository = movie_repository
        self.favorite_repository = favorite_repository

    async def get_user_favorite(self, user_id: int, movie_id: int):
        try:
            user = await self.user_repository.get_user(user_id)
            movie = await self.movie_repository.get_movie(movie_id)

            if not user or not movie:
                raise BusinessException(ErrorCode.USER_NOT_FOUND, "사용자 또는 영화가 존재하지 않습니다.")

            # 찜 True/False 반환
            favorite = await self.favorite_repository.get_is_liked(user_id, movie_id)

            # is_liked 값 반환 로직을 Service에서 처리
            return {"is_liked": favorite.is_liked if favorite else False, "user_id": user_id, "movie_id": movie_id}
        except Exception as e:
            raise BusinessException(ErrorCode.INTERNAL_SERVER_ERROR, detail="찜 조회를 실패했습니다.")

    async def get_user_favorites(self, user_id: int) -> List[Favorite]:
        """사용자의 모든 찜 목록을 가져옵니다."""
        # 사용자 존재 여부 확인
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, f"사용자 {user_id}번 ID를 찾을 수 없습니다.")

        # 사용자의 찜 목록 조회
        favorites = await self.favorite_repository.get_user_favorites(user_id)

        # for i in favorites:
        #     print(FavoriteItemResponse.model_validate(i))
        # import pdb

        # pdb.set_trace()
        # 찜 목록을 DTO로 변환
        # favortie_items = [FavoriteItemResponse.model_validate(item) for item in favorites]
        favorite_items = [
            FavoriteMovieResponse(
                favorite_id=fav.id,
                movie_id=fav.movie.id,
                is_liked=fav.is_liked,
                title=fav.movie.title,
                poster_image=fav.movie.poster_image_url,
                age_rating=fav.movie.age_rating,
                genre=fav.movie.genre,
                overview=fav.movie.overview,
                trailer_url=fav.movie.trailer_url,
                duration=fav.movie.duration,
                actor_images=fav.movie.actor_images,
                rating=fav.movie.rating,
                total_likes=await Favorite.filter(movie=fav.movie, is_liked=True).count(),
            )
            for fav in favorites
        ]

        # UserFavoritesResponse DTO 생성 및 반환
        return UserFavoritesResponse(user_id=user_id, favorites=favorite_items)
        # return UserFavoritesResponse(user_id=user_id, favorites=favortie_items, total_count=len(favortie_items))

    async def favorite_create_toggle(self, user_id, favoriteaddrequest: FavoriteAddRequest) -> FavoriteAddResponse:
        """영화를 찜 목록에 추가합니다."""
        # 사용자와 영화 존재 여부 확인
        user = await self.user_repository.get_user(user_id)
        movie = await self.movie_repository.get_movie(favoriteaddrequest.movie_id)
        if not user or not movie:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, "사용자 또는 영화가 존재하지 않습니다.")

        # 찜 목록 확인 및 토글
        favorite = await self.favorite_repository.get_favorite(user_id, favoriteaddrequest.movie_id)

        # 이미 찜 목록에 추가되었는지 확인
        if favorite:
            # 이미 존재하는 경우, is_liked 상태를 토글
            favorite.is_liked = not favorite.is_liked
            await favorite.save()
        else:
            # 존재하지 않는 경우, 새로 생성하고 is_liked를 True로 설정
            favorite = await Favorite.create(user_id=user_id, movie_id=favoriteaddrequest.movie_id, is_liked=True)
        if not favorite:
            raise BusinessException(ErrorCode.INTERNAL_SERVER_ERROR, "찜 생성을 실패했습니다.")

        return FavoriteAddResponse.model_validate(favorite)
