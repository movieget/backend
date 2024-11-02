from src.app.v1.review.entity.review import Review
from typing import List


class ReviewRepository:
    # prefetch_related
    # N+1 쿼리 문제를 방지하는 데 유용합니다(예: 리뷰를 가져온 후 각 사용자의 세부 정보를 별도로 가져오는 경우).
    # 리뷰와 연결된 사용자 정보를 불러오기
    @staticmethod
    async def get_reviews_by_movie_id(movie_id: int) -> List[Review]:
        return await Review.filter(movie=movie_id).prefetch_related("user").all()

    @staticmethod
    async def create_review(review: Review):
        """리뷰 생성"""
        await review.save()
        
    @staticmethod
    async def update_review(review: Review):
        """리뷰를 업데이트합니다."""
        await review.save()

    @staticmethod
    async def delete_review(review: Review):
        """리뷰를 삭제합니다."""
        await review.delete()

    @staticmethod
    async def delete_all_reviews_by_user(user_id: int):
        """특정 사용자의 모든 리뷰를 삭제합니다."""
        await Review.filter(user_id=user_id).delete()
