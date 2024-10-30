from pydantic import BaseModel
from typing import List, Optional


#### 상세 페이지 스키마 ####
class MovieDetail(BaseModel):
    id: int
    backdropImage: str
    posterImage: str
    title: str
    age: str
    genre: str
    duration: int
    playing: bool
    overview: str
    trailer: str
    actorImages: List[str]
    isLikes: bool
    totalLikes: int
    rating: int


#### 영화 검색 & 무한 스크롤 스키마 ####
class MovieListItem(BaseModel):
    id: int
    title: str
    posterImage: str
    age: str
    genre: str
    playing: bool
    overview: Optional[str] = None
    trailerUrl: Optional[str] = None
    duration: Optional[int] = None
    backdropImage: Optional[str] = None
    actorImages: Optional[List[str]] = None
    rating: Optional[int] = None
    isLikes: Optional[bool] = None
    totalLikes: Optional[int] = None


class MovieListResponse(BaseModel):
    movies: List[MovieListItem]
    total: int
    next_page: Optional[int]