from fastapi import APIRouter,Depends
from app.util.protect_route import get_current_user
from app.schema.auth import UserOutput

todoRouter=APIRouter(
    dependencies=[Depends(get_current_user)]
)
@todoRouter.get("/get_task")
def get_task():
    return "task"