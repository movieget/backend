from fastapi import APIRouter, HTTPException, Depends, status, Query
from src.app.v1.favorite.entity.favorite import Favorite
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.movie.schemas.movie_schema import MovieDetail, MovieListResponse, MovieListItem
from src.app.v1.user.entity.user import User
from src.common.models.consts import MovieStatusEnum
from src.core.security import get_current_user
from typing import Optional

router = APIRouter()


# 임시 사용자 데이터 생성 함수
async def get_current_user():
    # 임시 사용자 데이터 생성 (ID가 1인 사용자로 가정)
    return await User.get_or_none(id=1)


@router.get("/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: int, current_user: User = Depends(get_current_user)):
    """
    영화 상세 정보 조회 API

    - 기능: 특정 영화의 상세 정보를 조회합니다.
    - 파라미터:
        - movie_id: 조회할 영화의 ID
    - 반환: MovieDetail 객체 (영화 상세 정보)
    """
    movie = await Movie.get_or_none(id=movie_id).prefetch_related("actor_images")
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor_images = [actor_image.image_url for actor_image in movie.actor_images]
    is_liked = await Favorite.filter(user=current_user, movie=movie).exists()
    total_likes = await Favorite.filter(movie=movie).count()

    return MovieDetail(
        id=movie.id,
        backdropImage=movie.image_url,
        posterImage=movie.poster_image_url,
        title=movie.title,
        age=movie.age_rating,
        genre=movie.genre,
        duration=movie.duration,
        playing=movie.status == MovieStatusEnum.NOW_SHOWING,
        overview=movie.overview,
        trailer=movie.trailer_url,
        actorImages=actor_images,
        isLikes=is_liked,
        totalLikes=total_likes,
        rating=movie.rating,
    )


@router.post("/{movie_id}", status_code=status.HTTP_200_OK)
async def toggle_favorite(movie_id: int, current_user: User = Depends(get_current_user)):
    """
    영화 좋아요 토글 API

    - 기능: 특정 영화에 대한 사용자의 좋아요 상태를 토글합니다.
    - 파라미터:
        - movie_id: 좋아요를 토글할 영화의 ID
    - 반환: 좋아요 상태 변경 결과 메시지
    """
    movie = await Movie.get_or_none(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    favorite = await Favorite.get_or_none(user=current_user, movie=movie)

    if favorite:
        # 이미 좋아요가 있다면 삭제
        await favorite.delete()
        return {"status": "Favorite removed"}
    else:
        # 좋아요가 없다면 추가
        await Favorite.create(user=current_user, movie=movie)
        return {"status": "Favorite added"}


@router.get("/", response_model=MovieListResponse)
async def search_movies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),  # 현재 사용자 정보 추가
):
    """
    영화 검색 API

    - 기능: 제목으로 영화 목록을 페이지네이션하여 조회합니다.
    - 파라미터:
        - page: 페이지 번호 (기본값: 1)
        - limit: 한 페이지당 영화 수 (기본값: 10, 최대: 100)
        - search: 검색어 (선택적)
    - 반환: MovieListResponse 객체
    """
    query = Movie.all()

    if search:
        query = query.filter(title__icontains=search)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by("-created_at").prefetch_related("actor_images")  # actor_images 미리 로드

    movie_list = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=(movie.status == MovieStatusEnum.NOW_SHOWING.value),
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[actor_image.image_url for actor_image in movie.actor_images],
            rating=movie.rating,
            isLikes=await Favorite.filter(user=current_user, movie=movie).exists(),
            totalLikes=await Favorite.filter(movie=movie).count(),
        )
        for movie in movies
    ]

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(movies=movie_list, total=total, next_page=next_page)


@router.get("/movies/now", response_model=MovieListResponse)
async def get_now_showing_movies(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """
    상영 중 영화 조회 API

    - 기능: 현재 상영 중인 영화 목록을 페이지네이션하여 조회합니다.
    - 파라미터:
        - page: 페이지 번호 (기본값: 1)
        - limit: 한 페이지당 영화 수 (기본값: 10, 최대: 100)
    - 반환: MovieListResponse 객체
    """
    query = Movie.filter(status=MovieStatusEnum.NOW_SHOWING.value)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by("-created_at").prefetch_related("actor_images")

    movie_list = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=True,
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[actor_image.image_url for actor_image in movie.actor_images],
            rating=movie.rating,
            isLikes=False,
            totalLikes=0,
        )
        for movie in movies
    ]

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(movies=movie_list, total=total, next_page=next_page)


@router.get("/movies/soon", response_model=MovieListResponse)
async def get_coming_soon_movies(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """
    개봉 예정 영화 조회 API

    - 기능: 개봉 예정인 영화 목록을 페이지네이션하여 조회합니다.
    - 파라미터:
        - page: 페이지 번호 (기본값: 1)
        - limit: 한 페이지당 영화 수 (기본값: 10, 최대: 100)
    - 반환: MovieListResponse 객체
    """
    query = Movie.filter(status=MovieStatusEnum.COMING_SOON)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by("-created_at").prefetch_related("actor_images")

    movie_list = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=False,  # 개봉 예정이므로 False
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[actor_image.image_url for actor_image in movie.actor_images],
            rating=movie.rating,
            isLikes=False,
            totalLikes=0,
        )
        for movie in movies
    ]

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(movies=movie_list, total=total, next_page=next_page)
