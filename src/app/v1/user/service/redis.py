from datetime import timedelta
import json

from redis import RedisError
from fastapi import HTTPException
from starlette import status

from src.common.utils.redis import redis_client

REFRESH_TOKEN_TTL = timedelta(days=7)


# Redis에 카카오 액세스 토큰 저장
async def save_kakao_access_token(id: int, access_token: str):
    key = f"kakao_access_token:{id}"
    await redis_client.setex(key, timedelta(hours=6), access_token)


# Redis에 카카오 리프레시 토큰 저장
async def save_kakao_refresh_token(id: int, refresh_token: str):
    key = f"kakao_refresh_token:{id}"
    await redis_client.setex(key, timedelta(days=1), refresh_token)


# Redis로부터 카카오 액세스 토큰 가져오기
async def get_kakao_access_token(id: int):
    key = f"kakao_access_token:{id}"
    return await redis_client.get(key)


# Redis로부터 카카오 리프레시 토큰 가져오기
async def get_kakao_refresh_token(id: int):
    key = f"kakao_refresh_token:{id}"
    return await redis_client.get(key)


# Redis에 자체 리프레시 토큰 저장
async def save_refresh_token(id: int, jti: str) -> None:
    key = f"refresh_token:{id}"
    # jti 값만 저장
    token_data = {"jti": jti}

    try:
        # JSON 문자열로 변환 후 저장, 만료 기간 설정
        await redis_client.setex(key, REFRESH_TOKEN_TTL, json.dumps(token_data))
    except RedisError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e


# 자체 리프레시 토큰 검증
async def verify_refresh_token(id: int, jti: str) -> bool:
    key = f"refresh_token:{id}"

    # Redis 에서 저장된 리프레시 토큰 조회
    try:
        stored_token_data = await redis_client.get(key)
        if not stored_token_data:
            return False

        # Redis에 저장되어있는 해당 리프레시 토큰 가져와서 비교
        token_data = json.loads(stored_token_data)
        return token_data.get("jti") == jti
    except RedisError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e


async def delete_user_token(id: int) -> None:
    key = f"refresh_token:{id}"
    await redis_client.delete(key)


async def add_token_to_blacklist(jti: str, expires_in: int) -> None:
    try:
        await redis_client.setex(f"blacklist:{jti}", expires_in, "true")
    except RedisError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e


async def is_token_blacklisted(jti: str) -> bool:
    try:
        return await redis_client.exists(f"blacklist:{jti}") > 0
    except RedisError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis 서버 오류입니다.") from e
