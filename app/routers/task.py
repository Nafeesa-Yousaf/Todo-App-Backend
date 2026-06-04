from fastapi import APIRouter,Depends
from app.util.protect_route import get_current_user
from app.schema.task import TaskCreate,TaskResponse,TaskUpdate
from app.service.tasks_service import TaskService
from app.schema.auth import UserOutput

taskRoute=APIRouter()

@taskRoute.get("/get-tasks",status_code=200,response_model=list[TaskResponse])
def get_tasks(current_user:UserOutput=Depends(get_current_user)):
    return TaskService().get_tasks(user_id=current_user.id)

@taskRoute.post("/{task_id}/update-task",status_code=200,dependencies=[Depends(get_current_user)])
def update_task(updated_task:TaskUpdate,task_id:int):
    return TaskService().update_task(task=updated_task,task_id=task_id)

@taskRoute.post("/create-task",status_code=200)
def create_task(task:TaskCreate,current_user:UserOutput=Depends(get_current_user)):
    return TaskService().create_task(task=task,user_id=current_user.id)

@taskRoute.get("/{task_id}/delete-task",status_code=200,dependencies=[Depends(get_current_user)])
def delete_task(task_id:int):
    return TaskService().delete_task(task_id=task_id)

