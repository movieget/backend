import os

import aiohttp
from fastapi import HTTPException
import httpx

from src.app.v1.user.service.redis import get_kakao_refresh_token, save_kakao_access_token, save_kakao_refresh_token


async def get_kakao_token(code: str) -> str | None:
    url = "https://kauth.kakao.com/oauth/token"
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    params = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("KAKAO_CLIENT_ID"),
        "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params)

        response_data = response.json()

        if response.status_code != 200:
            raise HTTPException(detail=response_data.get("error_description"), status_code=500)

        access_token = response_data.get("access_token")

        return access_token


async def get_kakao_user_info(access_token: str):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}", "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve user info")


async def refresh_kakao_access_token(id: int) -> str | None:
    refresh_token = await get_kakao_refresh_token(id)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="리프레시 토큰이 없습니다.")

    url = "https://kapi.kakao.com/oauth/token"
    data = {"grant_type": "refresh_token", "client_id": os.getenv("KAKAO_CLIENT_ID"), "refresh_token": refresh_token}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"카카오 토큰 갱신 실패: {response.text}")

        tokens = response.json()
        new_access_token = tokens.get("access_token")
        new_refresh_token = tokens.get("refresh_token")  # 갱신된 리프레시 토큰이 있다면 받아옴

        # 새로운 토큰을 Redis에 저장
        await save_kakao_access_token(id, new_access_token)
        if new_refresh_token:
            await save_kakao_refresh_token(id, new_refresh_token)

        return new_access_token
