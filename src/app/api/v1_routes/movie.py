from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from src.app.v1.favorite.entity.favorite import Favorite
from src.app.v1.movie.entity.movie import Movie
from src.app.v1.movie.schemas.movie_schema import MovieDetail, MovieListResponse, MovieListItem, ActorImage
from src.app.v1.user.entity.user import User
from src.common.models.consts import MovieStatusEnum

router = APIRouter()

# Temporary user data creation function
async def getCurrentUser():
    # Temporary user data creation (assuming user with ID 1)
    return await User.get_or_none(id=1)

@router.get("/{movieId}", response_model=MovieDetail)
async def getMovieDetail(movieId: int, currentUser: User = Depends(getCurrentUser)):
    movie = await Movie.get_or_none(id=movieId).prefetch_related('actor_images')
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actorImages = [ActorImage(name=actorImage.actor_name, imageUrl=actorImage.image_url)
                   for actorImage in movie.actor_images]
    isLiked = await Favorite.filter(user=currentUser, movie=movie).exists()
    totalLikes = await Favorite.filter(movie=movie).count()

    return MovieDetail(
        id=movie.id,
        backdropImage=movie.image_url,
        posterImage=movie.poster_image_url,
        title=movie.title,
        age=movie.age_rating,
        genre=movie.genre,
        duration=movie.duration,
        playing=movie.status == MovieStatusEnum.NOW_SHOWING,
        overview=movie.overview,
        trailer=movie.trailer_url,
        actorImages=actorImages,
        isLikes=isLiked,
        totalLikes=totalLikes,
        rating=movie.rating
    )

@router.post("/{movieId}", status_code=status.HTTP_200_OK)
async def toggleFavorite(movieId: int, currentUser: User = Depends(getCurrentUser)):
    """
    Toggle favorite API for movies

    - Functionality: Toggles the user's favorite status for a specific movie.
    - Parameters:
        - movieId: ID of the movie to toggle favorite status
    - Returns: Message indicating the result of the favorite status change
    """
    movie = await Movie.get_or_none(id=movieId)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    favorite = await Favorite.get_or_none(user=currentUser, movie=movie)

    if favorite:
        # If already liked, delete it
        await favorite.delete()
        return {"status": "Favorite removed"}
    else:
        # If not liked, add it
        await Favorite.create(user=currentUser, movie=movie)
        return {"status": "Favorite added"}

@router.get("/", response_model=MovieListResponse)
async def searchMovies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    currentUser: User = Depends(getCurrentUser)
):
    query = Movie.all()

    if search:
        query = query.filter(title__icontains=search)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related('actor_images')

    movieList = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=(movie.status == MovieStatusEnum.NOW_SHOWING.value),
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[ActorImage(name=actorImage.actor_name, imageUrl=actorImage.image_url)
                         for actorImage in movie.actor_images],
            rating=movie.rating,
            isLikes=await Favorite.filter(user=currentUser, movie=movie).exists(),
            totalLikes=await Favorite.filter(movie=movie).count()
        )
        for movie in movies
    ]

    nextPage = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movieList,
        total=len(movieList),
        nextPage=nextPage
    )

@router.get("/movies/now", response_model=MovieListResponse)
async def getNowShowingMovies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query = Movie.filter(status=MovieStatusEnum.NOW_SHOWING.value)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related('actor_images')

    movieList = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=True,
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[ActorImage(name=actorImage.actor_name, imageUrl=actorImage.image_url)
                         for actorImage in movie.actor_images],
            rating=movie.rating,
            isLikes=False,
            totalLikes=0
        )
        for movie in movies
    ]

    nextPage = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movieList,
        total=len(movieList),
        nextPage=nextPage
    )

@router.get("/movies/soon", response_model=MovieListResponse)
async def getComingSoonMovies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query = Movie.filter(status=MovieStatusEnum.COMING_SOON)

    total = await query.count()
    movies = await query.offset((page - 1) * limit).limit(limit).order_by('-created_at').prefetch_related('actor_images')

    movieList = [
        MovieListItem(
            id=movie.id,
            title=movie.title,
            posterImage=movie.poster_image_url,
            age=movie.age_rating,
            genre=movie.genre,
            playing=False,
            overview=movie.overview,
            trailerUrl=movie.trailer_url,
            duration=movie.duration,
            backdropImage=movie.image_url,
            actorImages=[ActorImage(name=actorImage.actor_name, imageUrl=actorImage.image_url)
                         for actorImage in movie.actor_images],
            rating=movie.rating,
            isLikes=False,
            totalLikes=0
        )
        for movie in movies
    ]

    nextPage = page + 1 if (page * limit) < total else None

    return MovieListResponse(
        movies=movieList,
        total=len(movieList),
        nextPage=nextPage
    )