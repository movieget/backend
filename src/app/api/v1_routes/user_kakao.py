from fastapi import APIRouter, HTTPException
from redis import RedisError
from starlette import status
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse, Response
from tortoise.exceptions import DBConnectionError

from src.app.v1.user.service.oauth_service import get_kakao_token, get_kakao_user_info
from src.app.v1.user.service.redis import save_kakao_access_token, save_kakao_refresh_token, save_refresh_token
from src.core.configs.database_config import settings
from src.core.security import create_jwt_token, decode_jwt_token
from src.app.v1.user.repository.user_repository import UserRepository

router = APIRouter()
user_repository = UserRepository()


# 카카오 로그인
@router.get("/login/kakao")
async def kakao_login(code: str, response: Response):
    # 카카오 액세스 토큰과 리프레시 토큰 요청
    token = await get_kakao_token(code)
    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="카카오 로그인 실패")

    # 카카오 액세스 토큰을 이용하여 카카오 유저 정보 가져오기
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

    user = await user_repository.get_kakao_user(kakao_id=kakao_id)

    # 프론트 페이지로 리다이렉트
    # response = RedirectResponse(url="http://localhost:5173/kakao/callback", status_code=302)

    if user:
        # 사용자가 DB에 있다면
        # JWT 토큰 발행 (액세스토큰)    15분
        jwt_access_token = create_jwt_token({"id": user.id, "type": "access"}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        # 리프레쉬 토큰 생성 필요함 (액세스토큰 발급을 위한 리프레쉬토큰) 1시간
        jwt_refresh_token = create_jwt_token({"id": user.id, "type": "refresh"}, expires_delta=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        jti = decode_jwt_token(jwt_refresh_token).get("jti")

        response = JSONResponse(content={"detail": "login success"}, status_code=status.HTTP_200_OK)

        # 쿠키에 JWT 리프레시 토큰 및 전달값 설정
        response.set_cookie(
            key="refresh_token",
            value=jwt_refresh_token,
            httponly=True,  # JavaScript로 접근 불가
            secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
            max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
            samesite="none",  # 동일 사이트 정책
        )
        response.set_cookie(
            key="access_token",
            value=jwt_access_token,
            httponly=True,  # JavaScript로 접근 불가
            secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
            max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
            samesite="none",  # 동일 사이트 정책
        )
        response.set_cookie(
            key="user_id",
            value=user.id,
            httponly=True,  # JavaScript로 접근 불가
            secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
            max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
            samesite="none",  # 동일 사이트 정책
        )
        response.set_cookie(
            key="profile_url",
            value=user.image_url,
            httponly=True,  # JavaScript로 접근 불가
            secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
            max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
            samesite="none",  # 동일 사이트 정책
        )

        # 레디스에 "자체 리프레시 토큰"과 "카카오액세스토큰(로그아웃시 필요함)" 저장
        try:
            await save_refresh_token(id=user.id, jti=jti)
            await save_kakao_access_token(id=user.id, access_token=access_token)
            await save_kakao_refresh_token(id=user.id, refresh_token=refresh_token)
        except RedisError:
            raise HTTPException(status_code=500, detail="Redis 저장 실패")

        return response

    else:
        try:
            # 사용자 정보가 없는 경우 유저 정보를 DB에 저장 (회원가입)
            user = await user_repository.create_user(
                username=username,
                email=email,
                nickname=nickname,
                birthday=birthday,
                phone_number=phone_number,
                oauth_provider=oauth_provider,
                image_url=image_url,
                kakao_id=kakao_id,
            )

            # JWT 토큰 발행 (액세스토큰)    15분
            jwt_access_token = create_jwt_token({"id": user.id, "type": "access"}, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

            # 리프레쉬 토큰 생성 필요함 (액세스토큰 발급을 위한 리프레쉬토큰) 1시간
            jwt_refresh_token = create_jwt_token({"id": user.id, "type": "refresh"}, expires_delta=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            jti = decode_jwt_token(jwt_refresh_token).get("jti")

            response = JSONResponse(content={"detail": "login Fail"}, status_code=status.HTTP_404_NOT_FOUND)

            # 쿠키에 JWT 리프레시 토큰 및 전달값 설정
            response.set_cookie(
                key="refresh_token",
                value=jwt_refresh_token,
                httponly=True,  # JavaScript로 접근 불가
                secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
                max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
                samesite="none",  # 동일 사이트 정책
            )
            response.set_cookie(
                key="access_token",
                value=jwt_access_token,
                httponly=True,  # JavaScript로 접근 불가
                secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
                max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
                samesite="none",  # 동일 사이트 정책
            )
            response.set_cookie(
                key="user_id",
                value=user.id,
                httponly=True,  # JavaScript로 접근 불가
                secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
                max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
                samesite="none",  # 동일 사이트 정책
            )
            response.set_cookie(
                key="profile_url",
                value=user.image_url,
                httponly=True,  # JavaScript로 접근 불가
                secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
                max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
                samesite="none",  # 동일 사이트 정책
            )

            # 레디스에 "자체 리프레시 토큰"과 "카카오액세스토큰(로그아웃시 필요함), 카카오리프레시토큰" 저장
            try:
                await save_refresh_token(id=user.id, jti=jti)
                await save_kakao_access_token(id=user.id, access_token=access_token)
                await save_kakao_refresh_token(id=user.id, refresh_token=refresh_token)
            except RedisError:
                raise HTTPException(status_code=500, detail="Redis 저장 실패")

            return response

        except DBConnectionError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="데이터베이스 연결 오류입니다.")
