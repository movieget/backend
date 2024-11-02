import uuid, urllib.parse
from botocore.exceptions import BotoCoreError, ClientError
import os
from dotenv import load_dotenv
from typing import List, Dict
from src.common.utils.aws_s3 import s3_client
from src.common.handlers.exception_handler import BusinessException, ErrorCode
from src.app.v1.review.entity.review import Review
from src.app.v1.review.repository.review_repository import ReviewRepository
from src.app.v1.movie.repository.movie_repository import MovieRepository
from src.app.v1.user.repository.user_repository import UserRepository
from src.app.v1.review.schemas.resquestDto import ReviewCreateRequest, ReviewUpdateRequest
from src.app.v1.review.schemas.responseDto import ReviewImageResponse, ReviewsResponse, ReviewCreateResponse

load_dotenv()


class ReviewService:

    def __init__(self, review_repository: ReviewRepository, movie_repository: MovieRepository, user_repository: UserRepository):
        self.review_repository = review_repository
        self.movie_repository = movie_repository
        self.user_repository = user_repository

    async def get_movie_reviews(self, movie_id: int) -> List[ReviewsResponse]:
        # Movie가 존재하는 지 조회
        reviews = await self.review_repository.get_reviews_by_movie_id(movie_id)
        if not reviews:
            raise BusinessException(ErrorCode.MOVIE_NOT_FOUND, f"조회한 {movie_id}가 존재하지 않습니다.")

        # ReviewsResponse로 변환하여 반환
        return [
            ReviewsResponse(
                id=review.id,
                image_url=review.user.image_url,
                username=review.user.username,
                rating=review.rating.value,  # Assuming rating is an Enum
                title=review.title,
                contents=review.contents,
                review_image_url=review.review_image_url,
                registration_date=review.registration_date,
            )
            for review in reviews
        ]

    async def create_review(self, movie_id: int, review_request: ReviewCreateRequest) -> ReviewCreateResponse:
        """새로운 리뷰를 생성합니다."""
        # 영화 조회
        movie = await self.movie_repository.get_movie(movie_id)
        if not movie:
            raise BusinessException(ErrorCode.MOVIE_NOT_FOUND, f"영화 {movie_id}번 ID를 찾을 수 없습니다.")
        # 사용자 조회
        user = await self.user_repository.get_user(review_request.user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, f"사용자 {review_request.user_id}번 ID를 찾을 수 없습니다.")

        review = Review(
            title=review_request.title,
            contents=review_request.contents,
            review_image_url=review_request.review_image_url,
            rating=review_request.rating,
            user_id=user.id,
            movie_id=movie_id,
        )
        print("======================================\n")
        print(review)
        print("======================================\n")

        after_review = await self.review_repository.create_review(review)

        print("등록 날짜:", after_review.registration_date)

        print("======================================\n")
        print(after_review)
        print("======================================\n")

        # ReviewCreateResponse로 변환하여 반환
        return ReviewCreateResponse(
            id=after_review.id,
            rating=after_review.rating.value,  # 평점 (Enum에서 값 가져오기)
            title=after_review.title,
            contents=after_review.contents,
            review_image_url=after_review.review_image_url,
            registration_date=after_review.registration_date,
            user_id=user.id,  # 사용자 이름
        )

    async def upload_review_image(self, user_id, image_file) -> Dict:
        # 사용자 확인
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise BusinessException(ErrorCode.USER_NOT_FOUND, f"사용자 {user_id}번 ID를 찾을 수 없습니다.")

        filename = f"{str(uuid.uuid4())}.jpg"
        s3_key = f"{user_id}/{filename}"

        try:
            s3_client.upload_fileobj(image_file.file, os.getenv("AWS_BUCKET_NAME"), s3_key)
        except (BotoCoreError, ClientError) as e:
            raise BusinessException(ErrorCode.INTERNAL_SERVER_ERROR, detail=f"S3 upload fails: {str(e)}")

        url = f"https://s3-ap-northeast-2.amazonaws.com/{os.getenv("AWS_BUCKET_NAME")}/{urllib.parse.quote(s3_key, safe='~()*!.')}"

        return ReviewImageResponse(review_image_url=url)

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
