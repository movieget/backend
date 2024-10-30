import httpx


async def logout_kakao_service(provider: str, access_token: str) -> bool | None:
    if provider != "kakao":
        raise ValueError(f"지원하지 않는 소셜: {provider}")

    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()  # 상태 코드가 200이 아닐 경우 예외 발생
            return True  # 로그아웃 성공
        except httpx.HTTPStatusError as e:
            print(f"HTTP 오류: {e.response.status_code}, 응답 내용: {e.response.text}")
        except Exception as e:
            print(f"예기치 않은 오류: {str(e)}")

    return False  # 로그아웃 실패


# 추가되는 소셜의 로그아웃 기능 구현예정
# async def logout_naver_service(provider: str, access_token:str) -> bool | None:
#     pass
