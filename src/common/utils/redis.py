import redis
from redis.asyncio import from_url

from src.core.configs.database_config import settings

# Redis 연결 설정
redis_client = from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis():
    """
    Redis 클라이언트 반환 함수

    기능:
    - 설정된 Redis 클라이언트를 비동기적으로 반환

    반환값:
    - Redis 클라이언트 객체
    """
    return redis_client


def test_redis_connection():
    """
    Redis 연결 테스트 함수

    기능:
    - Redis 서버와의 연결을 테스트합니다.
    - 연결 성공 시 성공 메시지를 출력
    - 연결 실패 시 오류 메시지를 출력

    예외:
    - redis.exceptions.ConnectionError: Redis 연결 실패 시 발생
    """
    try:
        redis_client.ping()
        print(":white_check_mark: Redis 서버에 연결되었습니다.")
    except redis.exceptions.ConnectionError as e:
        print(f":x: Redis 연결 실패: {e}")