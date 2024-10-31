import redis
from redis.asyncio import from_url

from src.core.configs.database_config import settings

# Redis 연결 설정
redis_client = from_url(settings.REDIS_URL, decode_responses=True)


# Redis 연결 테스트
def test_redis_connection():
    try:
        redis_client.ping()
        print("✅ Redis 서버에 연결되었습니다.")
    except redis.exceptions.ConnectionError as e:
        print(f"❌ Redis 연결 실패: {e}")
