import asyncio
from datetime import datetime, timezone

from fastapi import HTTPException, status, Response
from jose import JWTError, jwt
from src.app.v1.user.entity.user import User
from src.app.v1.user.schemas.user import UserResponseSchema, UserUpdateSchema  # 필요한 경우 추가
from src.app.v1.user.service.delete_user import schedule_account_deletion
from src.app.v1.user.service.redis import add_token_to_blacklist
from src.core.configs.database_config import settings


async def get_user_info(user_id: int) -> UserResponseSchema:
    user = await User.get(id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponseSchema(
        id=user.id,
        kakao_id=user.kakao_id,
        nickname=user.nickname,
        email=user.email,
        username=user.username,
        birthday=user.birthday or "",
        phone_number=user.phone_number or "",
        oauth_provider=user.oauth_provider or "",
        image_url=user.image_url or "",
    )


async def update_user_info(user_id: int, user_update: UserUpdateSchema) -> UserResponseSchema:
    user = await User.get(id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 수정할 항목이 None이 아닐 경우에만 업데이트
    if user_update.nickname is not None:
        user.nickname = user_update.nickname
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.phone_number is not None:
        user.phone_number = user_update.phone_number
    if user_update.birthday is not None:
        user.birthday = user_update.birthday
    if user_update.image_url is not None:
        user.image_url = user_update.image_url

    await user.save()  # 변경 사항 저장

    return UserResponseSchema(
        id=user.id,
        kakao_id=user.kakao_id,
        nickname=user.nickname,
        email=user.email,
        username=user.username,
        birthday=user.birthday or "",
        phone_number=user.phone_number or "",
        oauth_provider=user.oauth_provider or "",
        image_url=user.image_url or "",
    )


async def logout_user(access_token: str, refresh_token: str, response: Response) -> dict:
    try:
        # JWT 디코딩 및 jti와 만료 시간 추출
        access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        access_jti = access_payload.get("jti")
        access_exp = access_payload.get("exp")

        if not access_jti or access_exp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 토큰입니다.")

        # 액세스토큰 -> 블랙리스트
        access_expires_in = access_exp - int(datetime.now(timezone.utc).timestamp())
        if access_expires_in > 0:
            await add_token_to_blacklist(access_jti, access_expires_in)

        # 쿠키에서 가져온 리프레시토큰 삭제
        if refresh_token:
            refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            refresh_jti = refresh_payload.get("jti")
            refresh_exp = refresh_payload.get("exp")

            if not refresh_jti or refresh_exp is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 토큰입니다.")

            # 리프레시 토큰 블랙리스트 추가
            refresh_expires_in = refresh_exp - int(datetime.now(timezone.utc).timestamp())
            if refresh_expires_in > 0:
                await add_token_to_blacklist(refresh_jti, refresh_expires_in)

            # 리프레시토큰을 쿠키에서 삭제
            response.delete_cookie("refresh_token")

        return {"message": "로그아웃 완료"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")


async def delete_user_account(user_id: int) -> dict:
    user = await User.get(id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_deleted = True
    await user.save()

    # 비동기 작업 생성 (7일 후에 사용자 정보를 DB에서 삭제)
    asyncio.create_task(schedule_account_deletion(user_id))

    return {"message": "회원 탈퇴 요청이 완료되었습니다. 7일 후에 계정이 삭제됩니다."}
