from fastapi import BackgroundTasks, Depends
from src.app.v1.favorite.entity.favorite import Favorite
from src.common.utils.redis import get_redis
import json

CACHE_EXPIRE_TIME = 5  # 5초


async def get_total_likes(movie_id: int, redis=Depends(get_redis)) -> int:
    """
    get_total_likes 함수

    기능:
    - 특정 영화의 총 좋아요 수를 조회합니다.
    - Redis 캐시에서 좋아요 수를 먼저 확인하고, 없으면 데이터베이스에서 계산하여 캐시에 저장

    매개변수:
    - movie_id (int): 조회할 영화의 ID
    - redis: Redis 클라이언트 (의존성 주입)

    반환값:
    - int: 총 좋아요 수
    """
    cache_key = f"movie:{movie_id}:likes"
    cached_likes = await redis.get(cache_key)
    if cached_likes is not None:
        return int(cached_likes)

    total_likes = await Favorite.filter(movie_id=movie_id, is_liked=True).count()
    await redis.set(cache_key, total_likes, ex=CACHE_EXPIRE_TIME)
    return total_likes


async def update_likes_count(movie_id: int):
    """
    update_likes_count 함수

    기능:
    - 특정 영화의 좋아요 수를 계산하고 Redis 캐시를 업데이트

    매개변수:
    - movie_id (int): 업데이트할 영화의 ID

    동작:
    1. Redis 클라이언트를 가져옵니다.
    2. 데이터베이스에서 해당 영화의 좋아요 수를 계산
    3. 계산된 좋아요 수를 Redis 캐시에 저장
    4. 업데이트 결과를 콘솔에 출력
    """
    redis = await get_redis()
    total_likes = await Favorite.filter(movie_id=movie_id, is_liked=True).count()
    cache_key = f"movie:{movie_id}:likes"
    await redis.set(cache_key, total_likes, ex=CACHE_EXPIRE_TIME)
    print(f"Updated likes count for movie {movie_id}: {total_likes}")


def schedule_likes_update(background_tasks: BackgroundTasks, movie_id: int):
    """
    schedule_likes_update 함수

    기능:
    - 좋아요 수 업데이트를 백그라운드 작업으로 예약

    매개변수:
    - background_tasks (BackgroundTasks): FastAPI의 BackgroundTasks 객체
    - movie_id (int): 업데이트할 영화의 ID

    동작:
    - update_likes_count 함수를 백그라운드 태스크로 추가
    """
    background_tasks.add_task(update_likes_count, movie_id)


async def cache_movie_detail(movie_id: int, movie_detail: dict, redis=Depends(get_redis)):
    """
    cache_movie_detail 함수

    기능:
    - 영화 상세 정보를 Redis 캐시에 저장

    매개변수:
    - movie_id (int): 캐시할 영화의 ID
    - movie_detail (dict): 캐시할 영화 상세 정보 딕셔너리
    - redis: Redis 클라이언트 (의존성 주입)

    동작:
    - 영화 상세 정보를 JSON 형태로 직렬화하여 Redis에 저장
    """
    cache_key = f"movie:{movie_id}:detail"
    await redis.set(cache_key, json.dumps(movie_detail), ex=CACHE_EXPIRE_TIME)


async def get_cached_movie_detail(movie_id: int, redis=Depends(get_redis)):
    """
    get_cached_movie_detail 함수

    기능:
    - Redis 캐시에서 영화 상세 정보를 조회

    매개변수:
    - movie_id (int): 조회할 영화의 ID
    - redis: Redis 클라이언트 (의존성 주입)

    반환값:
    - dict 또는 None: 캐시된 영화 상세 정보 (없으면 None)

    동작:
    - Redis 캐시에서 영화 상세 정보를 조회하고, JSON 형태로 역직렬화하여 반환
    """
    cache_key = f"movie:{movie_id}:detail"
    cached_detail = await redis.get(cache_key)
    if cached_detail:
        return json.loads(cached_detail)
    return None
