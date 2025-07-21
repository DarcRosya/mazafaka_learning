from pydantic import BaseModel
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from src.schemas.task_dto import TaskRead


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserRelationship(UserRead):
    tasks: list["TaskRead"]