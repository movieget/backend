from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist

from src.app.v1.user.entity.user import User
from src.app.v1.user.schemas.user import UserResponseSchema, UserUpdateSchema
from src.app.v1.user.service.oauth_service import get_kakao_access_token, get_kakao_user_info
from src.core.security import create_access_token, get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/login/kakao")
async def kakao_login(code: str):
    # 카카오 액세스 토큰 요청
    access_token = await get_kakao_access_token(code)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="카카오 인증 실패")

    # 카카오 유저 정보 가져오기
    kakao_user = await get_kakao_user_info(access_token)
    if not kakao_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="카카오 유저 정보 조회 실패")

    # 아래에 birthday 입력을 위한 변수 할당
    birthyear = kakao_user.get("kakao_account", {}).get("birthyear")
    birthdate = kakao_user.get("kakao_account", {}).get("birthday")

    # 유저 정보를 항목별로 할당하기
    username = kakao_user.get("kakao_account", {}).get("name")
    email = kakao_user.get("kakao_account", {}).get("email")
    nickname = kakao_user.get("properties", {}).get("nickname")
    birthday = birthyear + birthdate
    phone_number = kakao_user.get("kakao_account", {}).get("phone_number")
    oauth_provider = "kakao"
    image_url = kakao_user.get("properties", {}).get("thumbnail_image")
    kakao_id = kakao_user.get("id")

    # 사용자 조회 또는 생성
    try:
        user = await User.get(kakao_id=kakao_id)
    except DoesNotExist:
        pass
    #     # 사용자 생성
    #     user = await User.create(
    #         username=username,
    #         email=email,
    #         nickname=nickname,
    #         birthday=birthday,
    #         phone_number=phone_number,
    #         oauth_provider=oauth_provider,
    #         image_url=image_url,
    #         kakao_id=kakao_id,
    #
    #     )
    #
    # # JWT 토큰 발행
    # token = create_access_token({"id": user.id})
    # return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponseSchema)
async def read_me(token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
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


@router.patch("/me", response_model=UserResponseSchema)
async def update_user(user_update: UserUpdateSchema, current_user: User = Depends(get_current_user)):
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
