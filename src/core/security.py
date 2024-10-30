from datetime import datetime, timedelta
import uuid

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from tortoise.exceptions import DoesNotExist

from src.app.v1.user.entity.user import User
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
        access_token: str = Depends(oauth2_scheme),     # 헤더의 엑세스토큰
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 액세스 토큰의 블랙리스트 여부 확인
    try:
        payload = decode_jwt_token(access_token)
        jti = payload.get("jti")
        if await is_token_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token blacklisted")

        id = payload.get("id")
    except JWTError:
        raise credentials_exception

    # 쿠키에서 리프레시 토큰 가져오기
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise credentials_exception

    # 리프레시 토큰 검증
    try:
        # 리프레시 토큰 검증
        refresh_payload = decode_jwt_token(refresh_token)
        refresh_jti = refresh_payload.get("jti")
        refresh_user_id = refresh_payload.get("id")

        if await verify_refresh_token(id=refresh_user_id, jti=refresh_jti) is not True:
            raise credentials_exception

        # 가져온 id로 사용자 조회
        user = await User.get(id=refresh_user_id)
    except (JWTError, DoesNotExist):
        raise credentials_exception
    # 액세스 토큰과 리프레시 토큰의 사용자 id 일치 확인
    if id != user.id:
        raise credentials_exception

    return user
