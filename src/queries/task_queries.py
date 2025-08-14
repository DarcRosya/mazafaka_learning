import logging
from fastapi import HTTPException
from sqlalchemy import and_, select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.task_dto import TaskCreate, TaskUpdate
from src.models.task import Task
from src.models.tag import Tag
from src.utils.data_handle import make_aware


async def create_task_query(db: AsyncSession, task_in: TaskCreate, user_id: int) -> Task:
    data = task_in.model_dump()
    if 'deadline' in data:
        data['deadline'] = make_aware(data['deadline'])

    if 'completed_at' in data:
        data['completed_at'] = make_aware(data['completed_at'])

    task = Task(**data, user_id=user_id)
    try:
        db.add(task)
        await db.commit()
        result = await db.execute(
            select(Task)
            .options(selectinload(Task.tags))
            .filter(Task.id == task.id)
        )
        task_with_tags = result.scalar_one()
        return task_with_tags
    except Exception as e:
        await db.rollback()
        logging.error(f"Update user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

async def select_tasks_by_user_id(db: AsyncSession, user_id: int) -> list[Task]:
    query = (
        select(Task)
        .filter(Task.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def select_tasks_by_tag(db: AsyncSession, tag_name: str, user_id: int) -> list[Task]:
    query = (
        select(Task)
        .join(Task.tags) 
        .filter(and_(Tag.name == tag_name, Task.user_id == user_id))
    )
    result = await db.execute(query)
    return result.scalars().all()


async def select_task_with_selection_relationship(db: AsyncSession, task_id: int, user_id: int) -> Task | None:
    query = (
        select(Task)
        .options(selectinload(Task.tags))
        .filter(Task.id == task_id, Task.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_task_query(db: AsyncSession, task_id: int, user_id: int, task_update: TaskUpdate) -> Task:
    data = task_update.model_dump(exclude_unset=True)  # берем только поля, которые пришли
    if 'deadline' in data:
        data['deadline'] = make_aware(data['deadline'])
    if 'completed_at' in data:
        data['completed_at'] = make_aware(data['completed_at'])

    query = (
        update(Task)
        .filter(and_(Task.id == task_id, Task.user_id == user_id))
        .values(**data)
        .returning(Task)
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    updated_task = result.scalar_one_or_none()
    if not updated_task:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    return updated_task


async def delete_task_query(db: AsyncSession, task_id: int, user_id: int) -> None:
    query = (
        delete(Task)
        .filter(and_(Task.id == task_id, Task.user_id == user_id))
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found or access denied")