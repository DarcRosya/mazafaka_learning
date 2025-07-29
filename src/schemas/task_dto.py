from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.models.task import TaskPriority, TaskStatus
from src.schemas.tag_dto import TagRead


# user_id убрал потому что пользователь не должен передавать свой id при создании задачи
# Его ID ты получаешь из JWT-токена (в Depends(current_user) в роутере)
# Это защищает от подмены данных (например: отправить user_id=2 и создать задачу на чужого)
class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    deadline: Optional[datetime]
    completed_at: Optional[datetime]


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskWithTagsRead(TaskBase):
    tags: list["TagRead"]