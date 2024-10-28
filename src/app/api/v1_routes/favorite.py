from fastapi import APIRouter, Depends
from src.app.v1.favorite.schemas.requestDto import FavoriteAddRequest
from src.app.v1.favorite.schemas.responseDto import FavoriteAddResponse, UserFavoritesResponse
from src.app.v1.favorite.service.favorite_service import FavoriteService
from src.core.factory import get_favorite_service

router = APIRouter()


@router.get("/{user_id}", response_model=UserFavoritesResponse)
async def get_user_favorites(user_id: int, favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.get_user_favorites(user_id)


@router.post("/", response_model=FavoriteAddResponse)
async def favorite_create(favorite: FavoriteAddRequest, favorite_service: FavoriteService = Depends(get_favorite_service)):
    return await favorite_service.add_favorite(favorite)


@router.delete("/{user_id}/{movie_id}")
async def favorite_delete(user_id: int, movie_id: int, favorite_service: FavoriteService = Depends(get_favorite_service)):
    await favorite_service.delete_favorite(user_id, movie_id)
    return {"message": "Favorite successfully deleted"}
