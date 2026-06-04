from app.routers.auth import authRouter
from app.routers.task import taskRoute

def register_routes(app):
    app.include_router(router=authRouter, tags=["Auth"], prefix="/auth")
    app.include_router(router=taskRoute,tags=["Todo CRUD"], prefix="/todo")
