from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query, BackgroundTasks
from src.app.v1.favorite.entity.favorite import Favorite
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.movie.schemas.movie_schema import MovieDetail, MovieListResponse, MovieListItem, ActorImage
from src.app.v1.user.entity.user import User
from src.common.models.consts import MovieStatusEnum
from src.app.v1.movie.service.movie_service import get_total_likes, schedule_likes_update, cache_movie_detail, \
    get_cached_movie_detail
from src.common.utils.redis import get_redis


router = APIRouter()


async def get_current_user():
    """
    get_current_user 함수

    기능:
    - 임시 사용자 데이터를 생성합니다 (ID가 2인 사용자로 가정).
    - 실제 운영 환경에서는 적절한 인증 메커니즘으로 대해야함.

    반환값:
    - User 객체: 현재 사용자 정보
    """
    user = await User.get_or_none(id=2).only('id', 'username', 'email')
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{movie_id}", response_model=MovieDetail)
async def get_movie_detail(movie_id: int, current_user: User = Depends(get_current_user), redis=Depends(get_redis)):
    """
    get_movie_detail 함수

    기능:
    - 특정 영화의 상세 정보를 조회
    - Redis 캐시를 확인하고, 없으면 데이터베이스에서 정보를 가져와 캐시에 저장

    매개변수:
    - movie_id: 조회할 영화의 ID
    - current_user: 현재 로그인한 사용자 정보
    - redis: Redis 클라이언트

    반환값:
    - MovieDetail 객체: 영화 상세 정보
    """
    cached_detail = await get_cached_movie_detail(movie_id, redis)
    if cached_detail:
        return MovieDetail(**cached_detail)

    movie = await Movie.get_or_none(id=movie_id).prefetch_related('actor_images')
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")

    actor_images = [
        ActorImage(name=actor_image.actor_name, image_url=actor_image.image_url)
        for actor_image in movie.actor_images if actor_image.image_url
    ]

    is_liked = await Favorite.filter(user=current_user, movie=movie).exists()
    total_likes = await get_total_likes(movie.id, redis)

    movie_detail = MovieDetail(
        id=movie.id,
        backdrop_image=movie.image_url,
        poster_image=movie.poster_image_url,
        title=movie.title,
        age_rating=movie.age_rating,
        genre=movie.genre,
        duration=movie.duration,
        playing=movie.status == MovieStatusEnum.NOW_SHOWING,
        overview=movie.overview,
        trailer_url=movie.trailer_url,
        actor_images=actor_images,
        is_likes=is_liked,
        total_likes=total_likes,
        rating=movie.rating
    )

    await cache_movie_detail(movie_id, movie_detail.dict(), redis)
    return movie_detail


@router.post("/{movie_id}", status_code=status.HTTP_200_OK)
async def toggle_favorite(
        movie_id: int,
        current_user: User = Depends(get_current_user),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        redis=Depends(get_redis)
):
    """
    toggle_favorite 함수

    기능:
    - 특정 영화에 대한 사용자의 좋아요 상태를 토글
    - 좋아요 수 업데이트를 백그라운드 작업으로 예약
    - 영화 상세 정보 캐시를 삭제합니다.

    매개변수:
    - movie_id: 좋아요를 토글할 영화의 ID
    - current_user: 현재 로그인한 사용자 정보
    - background_tasks: 백그라운드 작업 객체
    - redis: Redis 클라이언트

    반환값:
    - dict: 좋아요 상태 변경 결과 메시지
    """
    movie = await Movie.get_or_none(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="영화를 찾을 수 없습니다.")

    favorite, created = await Favorite.get_or_create(user=current_user, movie=movie)

    if not created:
        favorite.is_liked = not favorite.is_liked
        await favorite.save()
    else:
        favorite.is_liked = True
        await favorite.save()

    schedule_likes_update(background_tasks, movie_id)

    await redis.delete(f"movie:{movie_id}:detail")

    return {"status": "좋아요가 취소되었습니다." if not favorite.is_liked else "좋아요가 추가되었습니다."}


@router.get("/", response_model=MovieListResponse)
async def search_movies(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        search: Optional[str] = None,
        current_user: User = Depends(get_current_user),
        redis=Depends(get_redis)
):
    """
    search_movies 함수

    기능:
    - 영화 목록을 검색하고 페이지네이션하여 조회
    - 검색어가 있으면 제목으로 필터링

    매개변수:
    - page: 페이지 번호
    - limit: 한 페이지당 영화 수
    - search: 검색어 (선택적)
    - current_user: 현재 로그인한 사용자 정보
    - redis: Redis 클라이언트

    반환값:
    - MovieListResponse 객체: 영화 목록 및 메타데이터
    """
    query = Movie.all()
    if search:
        query = query.filter(title__icontains=search)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related(
        'actor_images')

    movie_list = []
    for movie in movies:
        actor_images = [
            ActorImage(name=actor_image.actor_name, image_url=actor_image.image_url)
            for actor_image in movie.actor_images if actor_image.image_url
        ]

        movie_list.append(MovieListItem(
            id=movie.id,
            title=movie.title,
            poster_image=movie.poster_image_url,
            age_rating=movie.age_rating,
            genre=movie.genre,
            playing=(movie.status == MovieStatusEnum.NOW_SHOWING.value),
            overview=movie.overview,
            trailer_url=movie.trailer_url,
            duration=movie.duration,
            backdrop_image=movie.image_url,
            actor_images=actor_images,
            rating=movie.rating,
            is_likes=await Favorite.filter(user=current_user, movie=movie).exists(),
            total_likes=await get_total_likes(movie.id, redis)
        ))

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movie_list,
        total=len(movie_list),
        next_page=next_page
    )


@router.get("/movies/now", response_model=MovieListResponse)
async def get_now_showing_movies(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        redis=Depends(get_redis)
):
    """
    get_now_showing_movies 함수

    기능:
    - 현재 상영 중인 영화 목록을 페이지네이션하여 조회

    매개변수:
    - page: 페이지 번호
    - limit: 한 페이지당 영화 수
    - current_user: 현재 로그인한 사용자 정보
    - redis: Redis 클라이언트

    반환값:
    - MovieListResponse 객체: 상영 중인 영화 목록 및 메타데이터
    """
    query = Movie.filter(status=MovieStatusEnum.NOW_SHOWING.value)
    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related(
        'actor_images')

    movie_list = []
    for movie in movies:
        actor_images = [
            ActorImage(name=a.actor_name, image_url=a.image_url)
            for a in movie.actor_images if a.image_url
        ]
        movie_list.append(MovieListItem(
            id=movie.id,
            title=movie.title,
            poster_image=movie.poster_image_url,
            age_rating=movie.age_rating,
            genre=movie.genre,
            playing=True,
            overview=movie.overview,
            trailer_url=movie.trailer_url,
            duration=movie.duration,
            backdrop_image=movie.image_url,
            actor_images=actor_images,
            rating=movie.rating,
            is_likes=await Favorite.filter(user=current_user, movie=movie).exists(),
            total_likes=await get_total_likes(movie.id, redis)
        ))

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movie_list,
        total=len(movie_list),
        next_page=next_page
    )


@router.get("/movies/soon", response_model=MovieListResponse)
async def get_coming_soon_movies(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        redis=Depends(get_redis)
):
    """
    get_coming_soon_movies 함수

    기능:
    - 개봉 예정인 영화 목록을 페이지네이션하여 조회

    매개변수:
    - page: 페이지 번호
    - limit: 한 페이지당 영화 수
    - current_user: 현재 로그인한 사용자 정보
    - redis: Redis 클라이언트

    반환값:
    - MovieListResponse 객체: 개봉 예정인 영화 목록 및 메타데이터
    """
    query = Movie.filter(status=MovieStatusEnum.COMING_SOON.value)
    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related(
        'actor_images')

    movie_list = []
    for movie in movies:
        actor_images = [
            ActorImage(name=a.actor_name, image_url=a.image_url)
            for a in movie.actor_images if a.image_url
        ]
        movie_list.append(MovieListItem(
            id=movie.id,
            title=movie.title,
            poster_image=movie.poster_image_url,
            age_rating=movie.age_rating,
            genre=movie.genre,
            playing=False,
            overview=movie.overview,
            trailer_url=movie.trailer_url,
            duration=movie.duration,
            backdrop_image=movie.image_url,
            actor_images=actor_images,
            rating=movie.rating,
            is_likes=await Favorite.filter(user=current_user, movie=movie).exists(),
            total_likes=await get_total_likes(movie.id, redis)
        ))

    next_page = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movie_list,
        total=len(movie_list),
        next_page=next_page
    )