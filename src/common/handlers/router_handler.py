from app.v2.mobiles.router import router as mobile_router
from app.v2.questions.router import router as question_router
from app.v2.badges.router import router as badge_router


def attach_router_handlers(app):
    app.include_router(router=mobile_router, prefix="/api/v2")
    app.include_router(router=badge_router, prefix="/api/v2")
    app.include_router(router=question_router, prefix="/api/v2")
