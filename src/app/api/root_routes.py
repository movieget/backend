from fastapi import APIRouter


from app.api.v1_routes import user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
