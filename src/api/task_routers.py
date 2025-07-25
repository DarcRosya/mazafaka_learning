from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.user import User
from models.task import Task
from schemas.task_dto import TaskCreate, TaskRead, TaskUpdate, TaskWithTagsRead
from schemas.tag_dto import TagBase
from utils.jwt_access import get_current_user
from src.utils.task_servives import get_task_and_tag_or_404

from queries.task_queries import (
    delete_task_query,
    select_tasks_by_user_id,
    create_task_query,
    update_task_query,
    select_tasks_by_tag,
)

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
    current_user: User = Depends(get_current_user),
):
    return await select_tasks_by_user_id(db=db, user_id=current_user.id)


@router.post(
    "",
    response_model=TaskWithTagsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="Created task"
)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await create_task_query(db=db, task_in=task_in, user_id=current_user.id)    


@router.get(
    "",
    response_model=list[Task],
    summary="Get all tasks of current user by tag",
    response_description="List of tasks"
)
async def get_tasks_by_tag(
    tag_name: TagBase = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await select_tasks_by_tag(db=db, tag_name=tag_name, user_id=current_user.id)


@router.put(
    "/{task_id}/tags/{tag_id}",
    response_model=TaskWithTagsRead,
    status_code=status.HTTP_200_OK,
    summary="Add a new tag to task",
    response_description="Added tag"
)
async def add_tag_to_task(
    task_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    task, tag = await get_task_and_tag_or_404(db, task_id, tag_id, current_user.id)

    if tag not in task.tags:
        task.tags.append(tag)
        await db.commit()
        await db.refresh(task)

    return task


@router.delete(
    "/{task_id}/tags/{tag_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove a tag from task",
    response_description="Tag removed",
    responses={
        404: {"description": "Task or tag not found"},
        409: {"description": "Tag is not attached to the task"},
        200: {"description": "Tag successfully removed from task"},
    }
)
async def remove_tag_from_task(
    task_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    task, tag = await get_task_and_tag_or_404(db, task_id, tag_id, current_user.id)

    if tag not in task.tags:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag is not attached to the task"
        )

    task.tags.remove(tag)
    await db.commit()
    await db.refresh(task)

    return task


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
    return TaskRead.model_validate(updated_task, from_attributes=True)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task by ID",
    response_description="Task deleted",
    responses={404: {"description": "Tag not found"},
               204: {"description": "Task deleted successfully"}
    }
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    await delete_task_query(db=db, task_id=task_id, user_id=current_user.id)