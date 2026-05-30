from app.routers.auth import authRouter
from app.routers.todo_crud import todoRouter

def register_routes(app):
    app.include_router(router=authRouter, tags=["Auth"], prefix="/auth")
    app.include_router(router=todoRouter,tags=["Todo CRUD"], prefix="/todo")
