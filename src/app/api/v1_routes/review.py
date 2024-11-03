from fastapi import APIRouter, Depends, UploadFile, File, Query
from src.app.v1.review.schemas.responseDto import ReviewsResponse, ReviewImageResponse, ReviewCreateResponse, ReviewListResponse
from src.app.v1.review.schemas.resquestDto import ReviewCreateRequest, ReviewUpdateRequest
from src.app.v1.review.service.review_service import ReviewService

from src.core.factory import get_review_service

router = APIRouter()


@router.get("/reviews", response_model=ReviewListResponse)
async def get_all_reviews(
    movie_id: int = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    review_service: ReviewService = Depends(get_review_service),
):
    return await review_service.get_movie_reviews_pagination(movie_id, page, limit)


@router.post("/review/{movie_id}", response_model=ReviewCreateResponse)
async def create_review(
    movie_id: int,
    review_request: ReviewCreateRequest,
    review_service: ReviewService = Depends(get_review_service),
):
    return await review_service.create_review(movie_id, review_request)


@router.post("/review/image/{user_id}", response_model=ReviewImageResponse)
async def create_review_image(
    user_id: int,
    image_file: UploadFile = File(...),
    review_service: ReviewService = Depends(get_review_service),
):
    return await review_service.upload_review_image(user_id, image_file)


@router.patch("/review/{review_id}", response_model=ReviewsResponse)
async def update_review(
    review_id: int,
    review_request: ReviewUpdateRequest,
    review_service: ReviewService = Depends(get_review_service),
):
    return await review_service.update_review(review_id, review_request)


@router.delete("/review/{review_id}", response_model=dict)
async def delete_review(review_id: int, review_service: ReviewService = Depends(get_review_service)):
    await review_service.delete_review(review_id)
    return {"message": "리뷰가 성공적으로 삭제되었습니다."}


@router.delete("/review/{user_id}", response_model=dict)
async def delete_all_user_reviews(user_id: int, review_service: ReviewService = Depends(get_review_service)):
    await review_service.delete_all_reviews_by_user(user_id)
    return {"message": "사용자의 모든 리뷰가 성공적으로 삭제되었습니다."}
