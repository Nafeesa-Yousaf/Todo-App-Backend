from app.schema.task import TaskCreate, TaskResponse, TaskUpdate
from app.repository.tasks_repo import TaskRepository 
from fastapi import HTTPException,status

class TaskService():
    def __init__(self):
        self._taskRepo=TaskRepository()

    def create_task(self,task:TaskCreate,user_id:int):
        try:
            priority=task.priority.lower()
            task.priority=priority
            if(task.priority != "high" and task.priority != "medium" and task.priority != "low" ):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":"Invalid Priority. Priority must be High, Medium or Low"})
            task=self._taskRepo.create_task(task,user_id)
            return {"details": "Task Created Successfully","task":TaskResponse(**task)}
        except Exception as error:
            raise error

    def get_tasks(self,user_id:int):
        try:
            tasks=self._taskRepo.get_tasks_by_uid(user_id)
            return [TaskResponse(**task) for task in tasks]
        except Exception as error:
            raise error
    
    def delete_task(self,task_id:int):
        try:
            self._taskRepo.delete_task(task_id)
            return {"details": "Task Deeleted Successfully"}
        except Exception as error:
            raise error
        
    def update_task(self,task:TaskUpdate,task_id:int):
        try:
            if(task.priority is not None and task.priority != "High" and task.priority != "Medium" and task.priority != "Low" ):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":"Invalid Priority. Priority must be High, Medium or Low"})
            task=self._taskRepo.update_task(task,task_id)
            return {"details": "Task Updated Successfully", "updated_task": TaskResponse(**task)}
        except Exception as error:
            raise error