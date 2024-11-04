import logging
from datetime import date, timedelta
from typing import List

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.app.v1.book.entity.book import Book
from src.app.v1.review.entity.review import Review
from src.app.v1.user.entity.point_history import PointHistory
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
            return await User.get(oauth_id=kakao_id)
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
            oauth_id=kakao_id,
        )

    async def update_profile_image(self, id: int, image_url: str):
        user = await User.get(id=id)
        user.image_url = image_url
        await user.save()


logging.basicConfig(level=logging.DEBUG)


class PointRepository:
    @staticmethod
    def get_filter_start_date(period: str) -> date:
        today = date.today()
        if period == "today":
            logging.debug("Filtering by today's date")
            return today
        elif period == "week":
            logging.debug("Filtering by last 7 days")
            return today - timedelta(days=7)
        logging.debug("No date filter applied")
        return None

    @staticmethod
    async def get_user_point_stack(user_id: int, period: str) -> List[PointStackResponse]:
        point_stack = []
        start_date = PointRepository.get_filter_start_date(period)

        try:
            user = await User.get(id=user_id)
            total_points = user.point
            logging.debug(f"User {user_id} total points from User model: {total_points}")

            point_histories = await PointHistory.filter(
                user_id=user_id, change_type__in=["리뷰 적립", "예매 적립"], **({"created_at__gte": start_date} if start_date else {})
            ).order_by("created_at")

            for history in point_histories:
                point_stack.append(
                    PointStackResponse(
                        type=history.change_type,
                        accumulation_date=history.created_at,
                        movie_title=history.description,
                        points_earned=history.points,
                        remaining_points=total_points,
                    )
                )

            point_stack.sort(key=lambda x: x.accumulation_date)
            logging.info(f"User {user_id} point stack: {point_stack}")
        except Exception as e:
            logging.error(f"Error fetching point stack for user {user_id}: {e}")

        return point_stack

    # 포인트 이용내역
    @staticmethod
    async def get_user_point_use(user_id: int, period: str) -> List[PointUseResponse]:
        logging.debug(f"Fetching point use for user {user_id} with period: {period}")
        point_use = []

        try:
            try:
                user = await User.get(id=user_id)
                remaining_points = user.point
                logging.debug(f"User {user_id} remaining points: {remaining_points}")
            except DoesNotExist:
                logging.error(f"User {user_id} does not exist.")
                raise HTTPException(status_code=404, detail="User not found")

            start_date = PointRepository.get_filter_start_date(period)
            logging.debug(f"Start date for filtering: {start_date}")

            point_histories = (
                await PointHistory.filter(user_id=user_id, change_type="이용 내역", **({"created_at__gte": start_date} if start_date else {}))
                .prefetch_related("payment")
                .order_by("created_at")
            )

            for history in point_histories:
                booking_code = history.payment.orderId if history.payment else history.id
                remaining_points -= history.points

                point_use.append(
                    PointUseResponse(
                        booking_code=booking_code,
                        movie_title=history.description,
                        usage_date=history.created_at,
                        used_points=history.points,
                        remaining_points=remaining_points,
                    )
                )

            logging.info(f"Point use details for user {user_id}: {point_use}")
        except Exception as e:
            logging.error(f"Error fetching point use for user {user_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return point_use

    # update_points 함수 만들기 -> book, review의 repository에서 호출
    @staticmethod
    async def update_points(user_id: int, points_to_add: int, change_type: str, description: str):
        if change_type == "이용 내역" and points_to_add > 0:
            points_to_add = -points_to_add

        user = await User.get(id=user_id)
        user.point += points_to_add
        await user.save()

        await PointHistory.create(user=user, change_type=change_type, points=abs(points_to_add), description=description)

        logging.info(f"User {user_id} updated with {points_to_add} points. Total: {user.point}")

    # 포이트 차감
    @staticmethod
    async def deduct_points(user_id: int, points: int) -> None:
        try:
            user = await User.get(id=user_id)
            if user.point < points:
                raise ValueError("사용 가능한 포인트가 부족합니다.")
            user.point -= points
            await user.save()

        except DoesNotExist:
            raise ValueError("해당 사용자를 찾을 수 없습니다.")

    # 남은 포인트
    @staticmethod
    async def get_remaining_points(user_id: int) -> int:
        try:
            user = await User.get(id=user_id)
            return user.point
        except DoesNotExist:
            raise ValueError("해당 사용자를 찾을 수 없습니다.")

    @staticmethod
    async def restore_points(user_id: int, points: int) -> None:
        try:
            user = await User.get(id=user_id)
            user.point += points
            await user.save()
        except DoesNotExist:
            raise ValueError("해당 사용자를 찾을 수 없습니다.")
