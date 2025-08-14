from pydantic import BaseModel, EmailStr
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from src.schemas.task_dto import TaskRead


    


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserRead

class UserRelationshipTasks(UserRead):
    tasks: list["TaskRead"]