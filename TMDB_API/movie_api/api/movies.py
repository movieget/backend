from fastapi import APIRouter, HTTPException, Query
from typing import List
from TMDB_API.movie_api.models.movie import Movie
from TMDB_API.movie_api.schemas.movie import MovieResponse
from TMDB_API.movie_api.config import settings
import httpx
from datetime import date, datetime

router = APIRouter()


async def fetch_movie_from_tmdb(movie_id: int) -> dict:
    """
    TMDB API에서 특정 영화 정보를 가져옵니다.

    Args:
        movie_id (int): TMDB 영화 ID

    Returns:
        dict: 영화 정보

    Raises:
        HTTPException: API 요청 실패 시
    """
    url = f"{settings.TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": settings.TMDB_API_KEY, "append_to_response": "videos,release_dates", "language": "ko-KR"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"TMDB API 요청 실패: {str(e)}")


@router.post("/fetch-from-tmdb/", response_model=List[MovieResponse], name="fetch_movies_from_tmdb")
async def fetch_and_save_movies(movie_ids: List[int] = Query(...)):
    """
    TMDB API에서 영화 정보를 가져와 저장합니다.

    Args:
        movie_ids (List[int]): TMDB 영화 ID 리스트

    Returns:
        List[MovieResponse]: 저장된 영화 정보 리스트

    Raises:
        HTTPException: 영화 정보 가져오기 또는 저장 실패 시
    """
    results = []
    for movie_id in movie_ids:
        existing_movie = await Movie.get_or_none(id=movie_id)
        if existing_movie:
            results.append(existing_movie)
            continue

        try:
            tmdb_movie_data = await fetch_movie_from_tmdb(movie_id)
            movie_data = process_tmdb_data(tmdb_movie_data)
            db_movie = await Movie.create(**movie_data)
            results.append(db_movie)
        except HTTPException as e:
            print(f"영화 ID {movie_id} 처리 중 오류: {e.detail}")
            continue

    if not results:
        raise HTTPException(status_code=404, detail="영화를 찾거나 저장하지 못했습니다.")

    return results


def process_tmdb_data(tmdb_movie_data: dict) -> dict:
    """
    TMDB API 응답 데이터를 처리하여 데이터베이스 모델에 맞게 변환합니다.

    Args:
        tmdb_movie_data (dict): TMDB API 응답 데이터

    Returns:
        dict: 처리된 영화 데이터
    """
    release_date = parse_release_date(tmdb_movie_data)
    trailer_url = find_trailer_url(tmdb_movie_data)
    age_rating = get_age_rating(tmdb_movie_data)

    return {
        "id": tmdb_movie_data["id"],
        "title": tmdb_movie_data["title"],
        "overview": tmdb_movie_data["overview"],
        "release_date": release_date,
        "poster_image_url": f"https://image.tmdb.org/t/p/original{tmdb_movie_data['poster_path']}",
        "image_url": f"https://image.tmdb.org/t/p/original{tmdb_movie_data['backdrop_path']}",
        "duration": tmdb_movie_data["runtime"],
        "genre": tmdb_movie_data["genres"][0]["name"] if tmdb_movie_data["genres"] else "Unknown",
        "rating": float(tmdb_movie_data["vote_average"]),
        "status": get_movie_status(release_date),
        "trailer_url": trailer_url,
        "age_rating": age_rating,
    }


def parse_release_date(tmdb_movie_data: dict) -> date:
    """영화 개봉일을 파싱합니다."""
    release_date_str = tmdb_movie_data.get("release_date")
    return datetime.strptime(release_date_str, "%Y-%m-%d").date() if release_date_str else None


def find_trailer_url(tmdb_movie_data: dict) -> str:
    """영화 예고편 URL을 찾습니다."""
    videos = tmdb_movie_data.get("videos", {}).get("results", [])
    for video in videos:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return ""


def get_age_rating(tmdb_movie_data: dict) -> str:
    """영화 연령 등급을 가져옵니다."""
    for release in tmdb_movie_data.get("release_dates", {}).get("results", []):
        if release["iso_3166_1"] == "KR":
            return release["release_dates"][0].get("certification", "all")
    return "all"


def get_movie_status(release_date: date) -> str:
    """영화 상영 상태를 결정합니다."""
    today = date.today()
    if release_date > today:
        return "개봉 예정"
    elif release_date <= today:
        return "상영 중"
    else:
        return "상영 종료"
