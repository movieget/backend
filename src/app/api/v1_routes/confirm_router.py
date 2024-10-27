from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Query
from src.app.v1.book.service.book_service import get_completed_bookings_by_user_id
from src.app.v1.book.schemas.book import BookResponse
from typing import List


router = APIRouter()

@router.get("/completed", response_model=List[BookResponse])

async def get_completed_bookings(user_id: int=Query(...)):
# async def get_completed_bookings(user: User = Depends(get_current_user)):
    try:
        # 유저가 예약한 모든 'COMPLETED' 상태의 예약 정보를 가져옴
        bookings = await get_completed_bookings_by_user_id(user_id)

        # 예약 정보가 없을 경우 404 처리
        if not bookings:
            raise HTTPException(status_code=404, detail="예약된 정보가 없습니다.")

        # 예약 정보를 반환, 순서를 맞춤
        return [
            BookResponse(
                poster_url=booking.movie.poster_url,  # 영화 포스터 URL
                movie_info=f"{booking.movie.title}, {booking.movie.age_limit}세 이상",  # 영화 제목과 연령 제한
                booking_date=booking.booking_date,  # 예매일
                screening_date=booking.screening_date,  # 상영일
                seats=booking.seats,  # 좌석 목록
                total_price=booking.total_price,  # 총 가격
                person_count=f"성인{booking.adult_count} / 청소년{booking.child_count}",  # 성인 / 청소년 인원수
                screening_time=booking.screening_time,  # 상영 시간
                location=booking.location.name,  # 지점 정보
                cinema=booking.cinema.name  # 상영관 정보
            )
            for booking in bookings
        ]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="검색을 실패했습니다.")
