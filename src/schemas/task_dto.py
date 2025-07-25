from pydantic import BaseModel, field_validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from models.task import TaskPriority, TaskStatus

if TYPE_CHECKING:
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
    
    @field_validator("deadline", "completed_at", mode="before")
    @classmethod
    def remove_tzinfo(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @field_validator("deadline", "completed_at", mode="before")
    @classmethod
    def remove_tzinfo(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskWithTagsRead(TaskRead):
    tags: list["TagRead"]