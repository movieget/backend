from pydantic import BaseModel
from typing import List, Optional

class ActorImage(BaseModel):
    name: str
    image_url: str

class MovieDetail(BaseModel):
    id: int
    backdrop_image: str
    poster_image: str
    title: str
    age_rating: str
    genre: str
    duration: int
    playing: bool
    overview: str
    trailer_url: str
    actor_images: List[ActorImage]
    is_likes: bool
    total_likes: int
    rating: Optional[int] = None

class MovieListItem(BaseModel):
    id: int
    title: str
    poster_image: str
    age_rating: str
    genre: str
    playing: bool
    overview: Optional[str] = None
    trailer_url: Optional[str] = None
    duration: Optional[int] = None
    backdrop_image: Optional[str] = None
    actor_images: Optional[List[ActorImage]] = None
    rating: Optional[int] = None
    is_likes: Optional[bool] = None
    total_likes: Optional[int] = None

class MovieListResponse(BaseModel):
    movies: List[MovieListItem]
    total: int
    next_page: Optional[int] = None