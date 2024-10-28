from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.app.v1.user.entity.user import User
from src.app.v1.user.schemas.user import UserResponseSchema, UserUpdateSchema
# from src.app.v1.user.service.redis import add_token_to_blacklist
from src.app.v1.user.service.social_logout import logout_kakao_service
from src.core.configs.database_config import settings
from src.core.security import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 내 정보 조회
@router.get("/me", response_model=UserResponseSchema)
async def read_me(
        request: Request,
):
    user = await get_current_user(request)

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


# 내 정보 수정
@router.patch("/me", response_model=UserResponseSchema)
async def update_user(
        user_update: UserUpdateSchema,
        current_user: User = Depends(get_current_user)
):
    user = await User.get(id=current_user.id)

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

    # UserResponseSchema에 맞게 반환
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

#
# # 로그아웃
# @router.get("/logout/me")
# async def logout_me(
#         access_token: str = Depends(oauth2_scheme),
#         current_user=Depends(get_current_user),
# ) -> dict:
#     # JWT 토큰을 Redis 블랙리스트 추가
#     try:
#         # jti 추출
#         payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         jti = payload.get("jti")
#
#         if not jti:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 토큰입니다.")
#
#         # 토큰 만료 시간 계산 및 검증
#         exp = payload.get("exp")
#         if exp is None:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 토큰입니다.")
#         expires_in = exp - int(datetime.utcnow().timestamp())
#         if expires_in <= 0:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="만료된 토큰입니다.")
#
#         # 블랙리스트 추가
#         await add_token_to_blacklist(jti, expires_in)
#
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")
#
#     # 소셜 로그아웃 요청
#     if current_user.oauth_provider == "kakao":
#         success = await logout_kakao_service(
#             provider=current_user.oauth_provider,
#             access_token=current_user.oauth_token,
#         )
#         if not success:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=f"{current_user.oauth_provider} 로그아웃 실패",
#             )
#
#     """다른 소셜 로그아웃 추가 가능"""
#
#     return {"message": "로그아웃 완료"}
