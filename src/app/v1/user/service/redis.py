from datetime import timedelta
import json

from redis import RedisError
from fastapi import HTTPException
from starlette import status

from src.common.utils.redis import redis_client

REFRESH_TOKEN_TTL = timedelta(days=7)


# Redis에 리프레시 토큰 저장
async def store_refresh_token(id: int, jti: str) -> None:
    key = f"refresh_token:{id}"
    # jti 값만 저장
    token_data = {"jti": jti}

    # 리프레시 토큰을 JSON 문자열로 반환하여 Redis에 저장
    redis_client.set(key, json.dumps(token_data))

    # 만료 기간 설정
    redis_client.expire(key, REFRESH_TOKEN_TTL)


# 리프레시 토큰 검증
async def verify_refresh_token(id: int, jti: str) -> bool:
    key = f"refresh_token:{id}"

    # Redis 에서 저장된 리프레시 토큰 조회
    stored_token_data = redis_client.get(key)
    if stored_token_data is None:
        return False

    # Redis에 저장되어있는 해당 리프레시 토큰 가져오기
    token_data = json.loads(stored_token_data)

    # 리프레시 토큰의 jti가 Redis의 jti와 일치하는지 확인
    if token_data["jti"] == jti:
        return True


async def delete_user_token(id: int) -> None:
    key = f"refresh_token:{id}"
    redis_client.delete(key)

#
# async def add_token_to_blacklist(jti: str, expires_in: int):
#     try:
#         await redis_client.setex(f"blacklist:{jti}", expires_in, "true")
#     except RedisError as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e
#
#
# async def is_token_blacklisted(jti: str) -> bool:
#     try:
#         return await redis_client.exists(f"blacklist:{jti}") > 0
#     except RedisError as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e
