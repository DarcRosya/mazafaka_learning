from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.task import Task
from models.user import User
from queries.task_queries import (
    delete_task_query,
    get_tasks_by_user_id,
    create_task_query,
    update_task_query,
)
from schemas.task_dto import TaskCreate, TaskRead, TaskUpdate
from schemas.user_dto import UserRead
from utils.jwt_access import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get(
    "",
    response_model=list[TaskRead],
    summary="Get all tasks of current user",
    response_description="List of tasks"
)
async def get_tasks(
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(get_current_user),
):
    return await get_tasks_by_user_id(db=db, user_id=current_user.id)


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="Created task"
)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserRead = Depends(get_current_user)
):
    return await create_task_query(db=db, task_in=task_in, user_id=current_user.id)    


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task by ID",
    response_description="Updated task",
    responses={404: {"description": "Task not found"}}
)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    updated_task = await update_task_query(
        db=db, task_id=task_id, user_id=current_user.id, task_update=task_in
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    return TaskRead.model_validate(updated_task, from_attributes=True)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a task by ID",
    response_description="Task deleted",
    responses={404: {"description": "Task not found"}}
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    success = await delete_task_query(db=db, task_id=task_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    return {"detail": "Task deleted"}