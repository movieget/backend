# # src/app/v1/user/dependencies.py
# from fastapi import Depends, HTTPException, Security
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from src.core.configs.database_config import settings
# from src.app.v1.user.entity.user import User
#
# # JWT 토큰을 인증하는 OAuth2 스키마 설정
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     try:
#         # JWT 디코딩
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id = payload.get("sub") # JWT payload 에서 'sub' 값 (사용자 ID) 추출
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="유효한 인증정보를 찾을 수 없습니다.")
#         # 디코딩한 user_id를 통해 사용자 검색
#         user = await User.get(id=user_id)
#         if user is None:
#             raise HTTPException(status_code=401, detail="User를 찾을 수 없습니다.")
#         return user
#     # JWT가 유효하지 않거나 인증 오류가 발생하면 401 에러 반환
#     except JWTError:
#         raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
