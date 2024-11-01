from fastapi import APIRouter, Depends
from typing import List
from src.app.v1.review.schemas.responseDto import ReviewsResponse, ReviewImageResponse
from src.app.v1.review.schemas.resquestDto import ReviewCreateRequest, ReviewUpdateRequest, ReviewImageRequest
from src.app.v1.review.service.review_service import ReviewService

from src.core.factory import get_review_service

router = APIRouter()


@router.get("/reviews/{user_id}", response_model=List[ReviewsResponse])
async def get_user_reviews(user_id: int, review_service: ReviewService = Depends(get_review_service)):
    return await review_service.get_user_reviews_with_user_info(user_id)


@router.post("/review/{user_id}", response_model=ReviewsResponse)
async def create_review(review_request: ReviewCreateRequest, review_service: ReviewService = Depends(get_review_service)):
    return await review_service.create_review(review_request)


@router.post("/review/image", response_model=ReviewImageResponse)
async def create_review_image(review_request: ReviewImageRequest, review_service: ReviewService = Depends(get_review_service)):
    return await review_service.upload_review_image(review_request)


@router.patch("/review/{review_id}", response_model=ReviewsResponse)
async def update_review(review_id: int, review_request: ReviewUpdateRequest, review_service: ReviewService = Depends(get_review_service)):
    return await review_service.update_review(review_id, review_request)


@router.delete("/review/{review_id}", response_model=dict)
async def delete_review(review_id: int, review_service: ReviewService = Depends(get_review_service)):
    await review_service.delete_review(review_id)
    return {"message": "리뷰가 성공적으로 삭제되었습니다."}


@router.delete("/review/{user_id}", response_model=dict)
async def delete_all_user_reviews(user_id: int, review_service: ReviewService = Depends(get_review_service)):
    await review_service.delete_all_reviews_by_user(user_id)
    return {"message": "사용자의 모든 리뷰가 성공적으로 삭제되었습니다."}
