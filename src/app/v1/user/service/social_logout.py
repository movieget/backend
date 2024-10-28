import httpx


async def logout_kakao_service(provider: str, access_token: str) -> bool | None:
    if provider == "kakao":
        url = "https://kapi.kakao.com/v1/user/logout"
    else:
        raise ValueError(f"지원하지 않는 소셜: {provider}")

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        if provider == "kakao":
            response = await client.post(url, headers=headers)

        if response.status_code != 200:
            return None

        return response.json()

# 추가되는 소셜의 로그아웃 기능 구현예정
# async def logout_naver_service(provider: str, access_token:str) -> bool | None:
#     pass
