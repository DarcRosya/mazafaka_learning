from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.queries.user_queries import update_user_query, delete_user_query 
from src.schemas.task_dto import TaskRead
from src.schemas.user_dto import UserRead, UserUpdate
from src.utils.jwt_access import get_current_user
from src.models.user import User

router = APIRouter(
    prefix="/users",      # это общий префикс
    tags=["Users"]        # это группа, удобно в Swagger
)

@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user info",
    response_description="Current user data"
)
async def get_user(
    current_user: User = Depends(get_current_user)
):
    return UserRead.model_validate(current_user, from_attributes=True)


@router.get(
    "/me/tasks",
    response_model=list[TaskRead],
    summary="Get tasks of current user",
    response_description="List of tasks belonging to the current user"
)
async def get_user_tasks(
    current_user: User = Depends(get_current_user)
):
    return current_user.tasks


@router.patch(
    "/me",
    response_model=UserRead,
    summary="Update current user",
    response_description="Updated user object",
    responses={404: {"description": "User not found"}}
)
async def update_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    updated_user = await update_user_query(db=db, user_id=current_user.id, user_update=user_update)
    return UserRead.model_validate(updated_user, from_attributes=True)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user",
    response_description="User deleted successfully",
    responses={404: {"description": "Tag not found"},
               204: {"description": "Task deleted successfully"}
    }
)
async def delete_user(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session)
):
    await delete_user_query(db=db, user_id=current_user.id)