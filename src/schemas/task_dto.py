from pydantic import BaseModel, field_validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from models.task import TaskPriority, TaskStatus

if TYPE_CHECKING:
    from src.schemas.user_dto import UserRead



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

class TaskUpdate(TaskBase):
    pass

class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskRelationship(TaskRead):
    user: "UserRead"