from pydantic import BaseModel

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    priority: str

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str = "Low"

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    priority: str | None = None
