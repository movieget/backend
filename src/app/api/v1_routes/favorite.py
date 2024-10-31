from fastapi import APIRouter, Depends, Query
from typing import Annotated
from src.app.v1.favorite.schemas.requestDto import FavoriteAddRequest, FavoriteCheckRequest
from src.app.v1.favorite.schemas.responseDto import FavoriteAddResponse, UserFavoritesResponse, FavortieCheckResponse
from src.app.v1.favorite.service.favorite_service import FavoriteService
from src.core.factory import get_favorite_service

router = APIRouter()


@router.get("/favorite", response_model=FavortieCheckResponse)
async def get_user_favorite(
    user_id: Annotated[int, Query(..., gt=0, description="User ID must be positive")],
    movie_id: Annotated[int, Query(..., gt=0, description="Movie ID must be positive")],
    favorite_service: FavoriteService = Depends(get_favorite_service),
):
    return await favorite_service.get_user_favorite(user_id, movie_id)


@router.get("/favorites", response_model=UserFavoritesResponse)
async def get_user_favorites(user_id: int | None = Query(None), favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.get_user_favorites(user_id)


@router.post("/favorite/{user_id}", response_model=FavoriteAddResponse)
async def update_favorite(user_id: int, favoriteaddrequest: FavoriteAddRequest, favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.favorite_create_toggle(user_id, favoriteaddrequest)
