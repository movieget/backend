from typing import List
from src.app.v1.review.entity.review import Review
from src.common.handlers.exception_handler import BusinessException, ErrorCode
from src.app.v1.review.repository.review_repository import ReviewRepository
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.review.schemas.resquestDto import ReviewCreateRequest, ReviewUpdateRequest


class ReviewService:

    def __init__(self, review_repository: ReviewRepository, user_repository: UserRepository):
        self.review_repository = review_repository
        self.user_repository = user_repository

    async def get_user_reviews_with_user_info(self, user_id: int) -> List[Review]:
        """특정 사용자의 모든 리뷰를 가져옵니다."""
        # 사용자 조회
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, f"사용자 {user_id}번 ID를 찾을 수 없습니다.")

        # 사용자의 리뷰 조회
        reviews = await self.review_repository.get_reviews_by_user_id(user_id)

        # 리뷰가 없는 경우 처리
        if not reviews:
            raise BusinessException(ErrorCode.REVIEW_NOT_FOUND, f"사용자 {user_id}번 ID에 대한 리뷰가 없습니다.")

        return [
            {
                "id": review.id,
                "title": review.title,
                "contents": review.contents,
                "review_image_url": review.review_image_url,
                "rating": review.rating,
                "registration_date": review.registration_date,
                "username": review.user.username,
                "user_image_url": review.user.image_url,
            }
            for review in reviews
        ]

    async def create_review(self, review_request: ReviewCreateRequest) -> Review:
        """새로운 리뷰를 생성합니다."""
        # 사용자 조회
        user = await self.user_repository.get_user(ReviewCreateRequest.user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, f"사용자 {ReviewCreateRequest.user_id}번 ID를 찾을 수 없습니다.")
        return await self.review_repository.create_review(
            user_id=review_request.user_id,
            title=review_request.title,
            contents=review_request.contents,
            review_image_url=review_request.review_image_url,
            rating=review_request.rating,
        )

    # TODO: review_image_url은 다른 upload_handler를 불러 처리해야 됨.
    async def upload_image_review(self, )
    
    async def update_review(self, review_id: int, review_request: ReviewUpdateRequest):
        """특정 ID의 리뷰를 수정합니다."""
        # 리뷰 조회
        review = await self.review_repository.get_review_by_id(review_id)

        if not review:
            raise BusinessException(ErrorCode.REVIEW_NOT_FOUND, f"리뷰를 찾을 수 없습니다.")

        # 리뷰 필드 업데이트
        review.title = review_request.title
        review.contents = review_request.contents
        review.review_image_url = review_request.review_image_url
        review.rating = review_request.rating

        await self.review_repository.update_review(review)

    async def delete_review(self, review_id: int):
        """특정 ID의 리뷰를 삭제합니다."""

        # 유효한 리뷰 ID인지 확인
        if review_id <= 0:
            raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, "유효하지 않은 리뷰 ID입니다.")

        # 리뷰 조회
        review = await self.review_repository.get_review_by_id(review_id)

        # 리뷰가 존재하지 않는 경우 예외 발생
        if not review:
            raise BusinessException(ErrorCode.REVIEW_NOT_FOUND, f"리뷰 {review_id}번을 찾을 수 없습니다.")

        # 리뷰 삭제
        await self.review_repository.delete_review(review)

    async def delete_all_reviews_by_user(self, user_id: int):
        """특정 사용자의 모든 리뷰를 삭제합니다."""
        if user_id <= 0:
            raise BusinessException(ErrorCode.INVALID_INPUT_VALUE, "유효하지 않은 사용자 ID입니다.")

        # 사용자의 모든 리뷰 삭제
        deleted_count = await self.review_repository.delete_all_reviews_by_user(user_id)

        # 삭제된 리뷰가 없는 경우 예외 발생
        if deleted_count == 0:
            raise BusinessException(ErrorCode.REVIEW_NOT_FOUND, f"사용자 {user_id}번 ID에 대한 리뷰가 없습니다.")
