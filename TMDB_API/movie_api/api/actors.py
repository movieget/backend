from fastapi import APIRouter, HTTPException, Query
from typing import List
from TMDB_API.movie_api.models.actor_image import ActorImage
from TMDB_API.movie_api.schemas.actor_image import ActorImageResponse
from TMDB_API.movie_api.config import settings
import httpx

router = APIRouter()


async def fetch_movie_credits_from_tmdb(movie_id: int) -> dict:
    """
    TMDB API에서 특정 영화의 출연진 정보를 가져옵니다.

    Args:
        movie_id (int): TMDB 영화 ID

    Returns:
        dict: 영화 출연진 정보

    Raises:
        HTTPException: API 요청 실패 시
    """
    url = f"{settings.TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": settings.TMDB_API_KEY, "append_to_response": "credits", "language": "ko-KR"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"TMDB API 요청 실패: {str(e)}")


@router.post("/fetch-actor-images/", response_model=List[ActorImageResponse], name="fetch_actor_images")
async def fetch_and_save_actor_images(movie_id: int = Query(...)):
    """
    TMDB API에서 영화 ID를 사용하여 주요 출연진의 이미지 정보를 가져와 저장합니다.

    Args:
        movie_id (int): TMDB 영화 ID

    Returns:
        List[ActorImageResponse]: 저장된 배우 이미지 정보 리스트

    Raises:
        HTTPException: 배우 이미지 정보 가져오기 또는 저장 실패 시
    """
    actor_data = await fetch_movie_credits_from_tmdb(movie_id)
    cast = actor_data.get("credits", {}).get("cast", [])[:10]  # 상위 10명의 출연진으로 제한
    results = []

    if not cast:
        return results  # 출연진이 없는 경우 빈 리스트 반환

    for actor in cast:
        actor_id = actor["id"]
        profile_path = actor.get("profile_path")

        if profile_path:
            image_url = f"https://image.tmdb.org/t/p/original{profile_path}"
            actor_image = await save_or_get_actor_image(image_url, movie_id)
            results.append(actor_image)

    return results


async def save_or_get_actor_image(image_url: str, movie_id: int) -> ActorImage:
    """
    배우 이미지를 저장하거나 이미 존재하는 경우 가져옵니다.

    Args:
        image_url (str): 배우 이미지 URL
        movie_id (int): 관련 영화 ID

    Returns:
        ActorImage: 저장되거나 조회된 ActorImage 인스턴스
    """
    existing_image = await ActorImage.get_or_none(image_url=image_url)
    if existing_image:
        return existing_image

    return await ActorImage.create(image_url=image_url, movie_id=movie_id)
