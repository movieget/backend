from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Query, Response
from fastapi.security import OAuth2PasswordBearer

from src.app.v1.user.entity.user import User
from src.app.v1.user.repository.user_repository import PointRepository
from src.app.v1.user.schemas.oauth import KakaoOauthResponse
from src.app.v1.user.schemas.user import UserErrorResponse, UserResponseSchema, UserUpdateSchema, \
    PointUseResponse, \
    PointStackResponse
from src.app.v1.user.service.login_kakao import login_kakao_route
from src.app.v1.user.service.user_service import delete_user_account, get_user_info, logout_user, \
    update_user_info
from src.core.security import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 카카오 로그인
@router.get("/login/kakao")
async def login_kakao(code: str, response: Response) -> KakaoOauthResponse | UserErrorResponse:
    return await login_kakao_route(code, response)


# 내 정보 조회
@router.get("/me", response_model=UserResponseSchema)
async def read_me(current_user: User = Depends(get_current_user)):
    return await get_user_info(current_user.id)


# 내 정보 수정
@router.patch("/me", response_model=UserResponseSchema)
async def update_user(
        user_update: UserUpdateSchema,
        current_user: User = Depends(get_current_user)
):
    return await update_user_info(current_user.id, user_update)


# 로그아웃
@router.get("/logout/me")
async def logout_me(
        request: Request,
        response: Response,
        access_token: str = Depends(oauth2_scheme),
) -> dict:
    refresh_token = request.cookies.get("refresh_token")
    return await logout_user(access_token, refresh_token, response)


# 회원 탈퇴
@router.delete("/me")
async def delete_user(current_user: User = Depends(get_current_user)) -> dict:
    return await delete_user_account(current_user.id)



# 포인트 적립 내역
@router.get("/point/stack/{user_id}", response_model=List[PointStackResponse])
async def get_user_point_stack(user_id: int, period: str = Query("today", regex="^(all|today|week)$")):
    try:
        point_stack = await PointRepository.get_user_point_stack(user_id, period)
        if not point_stack:
            raise HTTPException(status_code=404, detail="적립된 포인트 내역이 없습니다.")
        return point_stack
    except Exception as e:
        raise HTTPException(status_code=500, detail="내부 서버 오류")


# 포인트 이용내역
@router.get("/point/use/{user_id}", response_model=List[PointUseResponse])
async def get_user_point_use(user_id: int, period: str = Query("today", regex="^(all|today|week)$")):
    try:
        point_use = await PointRepository.get_user_point_use(user_id, period)
        if not point_use:
            raise HTTPException(status_code=404, detail="사용한 포인트 내역이 없습니다.")
        return point_use
    except Exception as e:
        raise HTTPException(status_code=500, detail="내부 서버 오류")

#
# # 프로필 이미지 업데이트 엔드포인트
# @router.post("/update-profile-image")
# async def update_profile_image(
#         user: User = Depends(get_current_user),
#         file: UploadFile = File(...),
# ):
#     image_url = await update_profile_image_url(user.id, file)
#
#     response_data = UserImageUpdateSchema(
#         message="프로필 이미지가 변경되었습니다.",
#         image_url=image_url
#     )
#
#     return response_data
