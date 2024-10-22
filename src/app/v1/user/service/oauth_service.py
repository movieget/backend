import os

import aiohttp
import httpx

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"


async def get_kakao_access_token(code: str) -> str | None:
    url = "https://kauth.kakao.com/oauth/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("KAKAO_CLIENT_ID"),
        "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params)
        response_data = response.json()

        if response.status_code != 200:
            return None
        return response_data.get("access_token")


async def get_kakao_user_info(access_token: str):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None
