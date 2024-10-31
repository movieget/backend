from pydantic import BaseModel, Field
from typing import List, Optional

class ActorImage(BaseModel):
    name: str
    imageUrl: str

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
    actorImages: List[ActorImage]
    isLikes: bool
    totalLikes: int

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
    actorImages: Optional[List[ActorImage]] = None
    rating: Optional[int] = None
    isLikes: Optional[bool] = None
    totalLikes: Optional[int] = None

class MovieListResponse(BaseModel):
    movies: List[MovieListItem]
    total: int
    nextPage: Optional[int] = None
