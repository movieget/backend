from fastapi import APIRouter, HTTPException, Query
from asyncio import gather
from datetime import date

from src.app.v1.book.repository.book_repository import create_new_booking
from src.app.v1.book.service.movie_service import (
    get_movies_by_date,
    get_locations_by_movie,
    get_cinemas_by_location,
    get_screenings_by_cinema_and_movie
)
from src.app.v1.book.schemas.book import (
    BookOptionsResponse, MovieOption, LocationOption, CinemaOption, ScreeningOption,
)

router = APIRouter()

@router.get("/options", response_model=BookOptionsResponse)
async def book_options(screening_date: date, user_id: int = Query(None)):
    try:
        # 영화, 지역, 영화관, 상영시간 조회를 비동기 호출
        movies = await get_movies_by_date(screening_date)
        if not movies:
            raise HTTPException(status_code=404, detail="해당 날짜에 상영하는 영화를 찾을 수 없습니다.")

        # 회원일 경우 예약(book_id) 생성
        book_id = None
        if user_id is not None:
            new_booking = await create_new_booking(user_id=user_id, screen_info_id=screen_info_id)
            book_id = new_booking.id

        # MovieOption 생성
        movie_options = [
            MovieOption(
                id=movie["id"], title=movie["title"], genre=movie["genre"],
                duration=movie["duration"], age_rating=movie["age_rating"],
                poster_image_url=movie["poster_image_url"]
            ) for movie in movies
        ]

        # 비동기 호출을 동시에 수행
        location_tasks = [get_locations_by_movie(movie.id) for movie in movie_options]
        location_results = await gather(*location_tasks)

        all_locations, all_cinemas, all_screenings = [], [], []
        for movie, locations in zip(movie_options, location_results):
            location_options = [LocationOption(id=location["id"], spot=location["spot"]) for location in locations]
            all_locations.extend(location_options)

            # 각 지역에 대한 영화관 및 상영 시간 조회를 비동기로 처리
            cinema_tasks = [get_cinemas_by_location(location.id) for location in location_options]
            cinema_results = await gather(*cinema_tasks)
            for cinemas in cinema_results:
                cinema_options = [CinemaOption(id=cinema["id"], cinema_name=cinema["cinema_name"]) for cinema in cinemas]
                all_cinemas.extend(cinema_options)

                screening_tasks = [get_screenings_by_cinema_and_movie(cinema.id, movie.id) for cinema in cinema_options]
                screening_results = await gather(*screening_tasks)
                for screenings in screening_results:
                    screening_options = [
                        ScreeningOption(
                            id=screening["id"],
                            screen_number=screening["screen__screen_number"],
                            screening_date=screening["screening_date"],
                            start_time=screening["start_time"],
                            end_time=screening["end_time"]
                        )
                        for screening in screenings
                    ]
                    all_screenings.extend(screening_options)

        return BookOptionsResponse(
            book_id=book_id,  # 회원일 경우에만 book_id 반환
            movies=movie_options,
            locations=all_locations,
            cinemas=all_cinemas,
            screenings=all_screenings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
