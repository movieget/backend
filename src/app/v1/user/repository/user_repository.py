import logging
from datetime import date, timedelta
from typing import List

from tortoise.exceptions import DoesNotExist

from src.app.v1.book.entity.book import Book
from src.app.v1.review.entity.review import Review
from src.app.v1.user.entity.user import User
from src.app.v1.user.schemas.user import PointUseResponse, PointStackResponse


class UserRepository:
    async def get_user(self, user_id: int) -> User | None:
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None

    async def get_kakao_user(self, kakao_id: int) -> User | None:
        try:
            return await User.get(kakao_id=kakao_id)
        except DoesNotExist:
            return None

    async def create_user(
        self, username: str, email: str, nickname: str, birthday: str, phone_number: str, oauth_provider: str, image_url: str, kakao_id: int
    ) -> User:
        # 새 유저 생성
        return await User.create(
            username=username,
            email=email,
            nickname=nickname,
            birthday=birthday,
            phone_number=phone_number,
            oauth_provider=oauth_provider,
            image_url=image_url,
            kakao_id=kakao_id,
        )

# 포인트 이용 내역		GET	/user/point/use/{user_id}
# 포인트 적립 내역		GET	/user/point/stack/{user_id}
# 포인트 이용/적립내역 필터		GET	/user/point/filter/{user_id}
# 마이페이지(초기화면)-> 포인트 이용/적립 내역 -> 포인트 이용내역 (예매코드, 영화제목, 이용날짜(포인트 결제일), 이용내역(사용한 포인트 수), 남은 포인트) / 전체, 당일, 최근 1주간
#                                    -> 포인트 적립내역 (구분(리뷰40p/예매별100p), 적립 날짜(리뷰 작성일/예매일과 동일), 영화(관련타이틀), 적립금액, 남은 포인트) / 전체, 당일, 최근 1주간

# 포인트 적립 내역
class PointRepository:
    @staticmethod
    def get_filter_start_date(period: str) -> date:
        today = date.today()
        if period == "today":
            return today
        elif period == "week":
            return today - timedelta(days=7)
        return None

    @staticmethod
    async def get_user_point_stack(user_id: int, period: str) -> List[PointStackResponse]:
        point_stack = []
        total_points = await PointRepository.calculate_total_points(user_id)
        start_date = PointRepository.get_filter_start_date(period)

        type_bookings = await Book.filter(user_id=user_id).prefetch_related("screen_info__movie").all()
        for booking in type_bookings:
            if start_date and booking.book_time.date() < start_date:
                continue
            movie_title = booking.screen_info.movie.title if booking.screen_info and booking.screen_info.movie else "Unknown"
            points_earned = booking.adult_count * 100 + booking.child_count * 100
            total_points += points_earned
            point_stack.append(PointStackResponse(
                type="예매 적립",
                accumulation_date=booking.book_time,
                movie_title=movie_title,
                points_earned=points_earned,
                remaining_points=total_points
            ))

        reviewed_movies = set()
        type_reviews = await Review.filter(user_id=user_id).prefetch_related("movie").all()
        for review in type_reviews:
            if start_date and review.registration_date.date() < start_date:
                continue
            movie_title = review.movie.title if review.movie else "Unknown"
            movie_id = review.movie_id
            if movie_id not in reviewed_movies:
                reviewed_movies.add(movie_id)
                points_earned = 40
                total_points += points_earned
                point_stack.append(PointStackResponse(
                    type="리뷰 적립",
                    accumulation_date=review.created_at,
                    movie_title=movie_title,
                    points_earned=points_earned,
                    remaining_points=total_points
                ))

        # 적립 내역을 -> 날짜순으로 정렬
        # for i in range(len(point_stack)):
        #     min_index = i
        #     for j in range(i + 1, len(point_stack)):
        #         if point_stack[j].accumulation_date < point_stack[min_index].accumulation_date:
        #             min_index = j
        #     point_stack[i], point_stack[min_index] = point_stack[min_index], point_stack[i]

        point_stack.sort(key=lambda x: x.accumulation_date)
        logging.info(f"User {user_id} point stack: {point_stack}")
        return point_stack

    @staticmethod
    async def get_user_point_use(user_id:int, period: str) -> List[PointUseResponse]:
        point_use = []
        remaining_points = await PointRepository.calculate_total_points(user_id)
        start_date = PointRepository.get_filter_start_date(period)

        bookings = await Book.filter(user_id=user_id, status="COMPLETED").prefetch_related("screen_info_movie").all()
        for booking in bookings:
            if start_date and booking.book_time.date() < start_date:
                continue
            movie_title = booking.screen_info.movie.title if booking.screen_info and booking.screen_info.movie else "Unknown"
            used_points = (booking.adult_count + booking.child_count) * 100
            remaining_points -= used_points
            point_use.append(PointUseResponse(
                booking_code=booking.id,
                movie_title=movie_title,
                usage_date=booking.book_time,
                used_points=used_points,
                remaining_points=remaining_points
            ))
        point_use.sort(key=lambda x: x.usage_date)
        return point_use

    @staticmethod
    async def calculate_total_points(user_id: int) -> int:
        total_points = 0

        bookings = await Book.filter(user_id=user_id).all()
        for booking in bookings:
            points_earned = (booking.adult_count + booking.child_count) * 100
            total_points += points_earned

        reviewed_movies = set()
        reviews = await Review.filter(user_id=user_id).all()
        for review in reviews:
            movie_id = review.movie.id
            if movie_id not in reviewed_movies:
                reviewed_movies.add(movie_id)
                total_points += 40

        used_points = (total_points // 100) * 100 if total_points >= 100 else 0
        # if total_points >= 100:
        #     total_points // 100) * 100
        # else:
        #     used_points = 0
        remaining_points = total_points - used_points

        return remaining_points

# update_points 함수 만들기 -> book, review의 repository에서 호출
    @staticmethod
    async def update_points(user_id: int, points_to_add: int):
        user = await User.get(id=user_id)
        user.point += points_to_add
        await user.save()
        logging.info(f"User {user_id} updated with {points_to_add} points. Total: {user.point}")

