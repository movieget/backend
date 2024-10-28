import redis
from typing import Optional
from datetime import timedelta

# Redis 연결 설정
redis_client = redis.Redis(
    host="localhost",  # 또는 Docker 사용 시 Redis 컨테이너 이름 사용
    port=6379,
    decode_responses=True  # 문자열 응답 디코딩
)


# Redis 연결 테스트
def test_redis_connection():
    try:
        redis_client.ping()
        print("✅ Redis 서버에 연결되었습니다.")
    except redis.exceptions.ConnectionError as e:
        print(f"❌ Redis 연결 실패: {e}")
