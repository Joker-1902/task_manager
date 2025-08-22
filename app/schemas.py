from pydantic import BaseModel, ConfigDict
from typing import Optional
from .models import TaskStatus
import uuid


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskOut(TaskCreate):
    uuid: uuid.UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    model_config = ConfigDict(from_attributes=True)
