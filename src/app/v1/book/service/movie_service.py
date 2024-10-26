from fastapi import HTTPException

from src.app.v1.book.repository import book_repository


# 상영 날짜에 따른 영화 목록 조회
async def get_movies_by_date(screening_date: str):
    movies = await book_repository.get_movies_by_date(screening_date)
    if not movies:
        raise HTTPException(status_code=404, detail="선택한 날짜의 영화를 찾을 수 없습니다.")
    return movies


# 영화에 따른 지역 목록 조회
async def get_locations_by_movie(movie_id: int):
    locations = await book_repository.get_locations_by_movie(movie_id)
    if not locations:
        raise HTTPException(status_code=404, detail="선택된 영화를 상영하는 지역이 없습니다.")
    return locations

# 지역에 따른 영화관 목록 조회
async def get_cinemas_by_location(location_id: int):
    cinemas = await book_repository.get_cinemas_by_location(location_id)
    if not cinemas:
        raise HTTPException(status_code=404, detail="해당 지역에 영화관이 없습니다.")
    return cinemas


# 영화관과 영화에 따른 상영 시간 조회
async def get_screenings_by_cinema_and_movie(cinema_id: int, movie_id: int):
    screenings = await book_repository.get_screenings_by_cinema_and_movie(cinema_id, movie_id)
    if not screenings:
        raise HTTPException(status_code=404, detail="상영정보를 찾을 수 없습니다.")
    return screenings
