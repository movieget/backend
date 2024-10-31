from fastapi import APIRouter, Depends, Query
from src.app.v1.favorite.schemas.requestDto import FavoriteAddRequest
from src.app.v1.favorite.schemas.responseDto import FavoriteAddResponse, UserFavoritesResponse
from src.app.v1.favorite.service.favorite_service import FavoriteService
from src.core.factory import get_favorite_service

router = APIRouter()


@router.get("/favorites", response_model=UserFavoritesResponse)
async def get_user_favorites(user_id: int | None = Query(None), favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.get_user_favorites(user_id)


@router.post("/favorite/{user_id}", response_model=FavoriteAddResponse)
async def update_favorite(user_id: int, favoriteaddrequest: FavoriteAddRequest, favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.favorite_create_toggle(user_id, favoriteaddrequest)
