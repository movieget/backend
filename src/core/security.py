from datetime import datetime, timedelta
import uuid

from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from tortoise.exceptions import DoesNotExist

from src.app.v1.user.entity.user import User
from src.app.v1.user.schemas.oauth import KakaoOauthResponse
from src.app.v1.user.service.redis import is_token_blacklisted, verify_refresh_token
from src.core.configs.database_config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# jti 를 포함한 JWT 발급
def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()

    jti = str(uuid.uuid4())  # 유니크한 jti 생성 (jti = JWT ID)
    expire = datetime.utcnow() + expires_delta  # 만료기간 설정
    payload.update({"jti": jti, "exp": expire})

    # 토큰 설정
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
        request: Request,   # 쿠키의 리프레시 토큰을 가져오기 위해
        response: Response,
        access_token: str = Depends(oauth2_scheme),     # 헤더의 엑세스토큰
) -> KakaoOauthResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 액세스 토큰의 유효성 검사
    try:
        payload = decode_jwt_token(access_token)
        access_jti = payload.get("jti")
        access_exp = payload.get("exp")    # 만료시간 추출
        access_id = payload.get("id")

        # 블랙리스트 확인
        if await is_token_blacklisted(access_jti):
            raise HTTPException(status_code=401, detail="Token blacklisted")

        # 액세스토큰 만료시간 확인 -> 유효하다면 해당 액세스토큰 반환
        if access_exp and datetime.utcnow().timestamp() <= access_exp:
            user = await User.get(id=access_id)
            return KakaoOauthResponse(access_token=access_token, id=user.id)

        # 액세스 토큰이 만료된 경우, 리프레시 토큰을 확인하여 새로운 액세스토큰 발급
        current_refresh_token = request.cookies.get("refresh_token")
        # 리프레시 토큰이 없다면
        if not current_refresh_token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refresh_Token not found")

        # 리프레시 토큰 유효성 검사
        refresh_payload = decode_jwt_token(current_refresh_token)
        refresh_jti = refresh_payload.get("jti")
        refresh_exp = refresh_payload.get("exp")
        refresh_user_id = payload.get("id")

        # 리프레시 토큰의 만료시간 확인
        if refresh_exp and datetime.utcnow().timestamp() > refresh_exp:
            raise HTTPException(status_code=401, detail="Refresh token expired, Please login again")

        # 리프레시 토큰이 유효하지 않다면
        if await verify_refresh_token(refresh_user_id, refresh_jti) is not True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")

        # 리프레시 토큰이 유효할 때 -> 액세스 토큰 재발급
        new_access_token = create_jwt_token(
            {"id": refresh_user_id, "type": "access"},
            expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        # 쿠키에 현재 리프레시토큰 설정
        response.set_cookie(
            key="refresh_token",
            value=current_refresh_token,
            httponly=True,  # JavaScript로 접근 불가
            secure=False,  # HTTPS에서만 동작 (로컬 테스트 시 False)
            max_age=3600,  # 쿠키 만료 시간 (초 단위) ** 5분~10분 설정 필요
            samesite="none",  # 동일 사이트 정책
        )

        # Response body에 새로운 액세스토큰과 user id 반환
        response_model = KakaoOauthResponse(access_token=new_access_token, id=refresh_user_id)

        return response_model

    except JWTError:
        raise credentials_exception
