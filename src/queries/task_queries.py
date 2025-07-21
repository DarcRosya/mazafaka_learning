import logging
from fastapi import HTTPException
from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.task_dto import TaskCreate, TaskUpdate
from models.task import Task
from utils.data_handle import strip_tzinfo

async def create_task_query(db: AsyncSession, task_in: TaskCreate, user_id: int) -> Task:
    data = task_in.model_dump()
    if 'deadline' in data:
        data['deadline'] = strip_tzinfo(data['deadline'])

    if 'completed_at' in data:
        data['completed_at'] = strip_tzinfo(data['completed_at'])

    task = Task(**data, user_id=user_id)
    try:
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
    except Exception as e:
        await db.rollback()
        logging.error(f"Update user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

async def get_tasks_by_user_id(db: AsyncSession, user_id: int) -> list[Task] | None:
    query = (
        select(Task)
        .filter(Task.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def update_task_query(db: AsyncSession, task_id: int, user_id: User, task_update: TaskUpdate) -> Task | None:
    data = task_update.model_dump(exclude_unset=True)  # берем только поля, которые пришли
    if 'deadline' in data:
        data['deadline'] = strip_tzinfo(data['deadline'])

    if 'completed_at' in data:
        data['completed_at'] = strip_tzinfo(data['completed_at'])

    query = (
        update(Task)
        .where(and_(Task.id == task_id, Task.user_id == user_id))
        .values(**data)
        # .execution_options(synchronize_session='fetch')
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    if result.rowcount == 0:
        return None
    
    updated_object = await db.execute(select(Task).where(Task.id == task_id))
    # Вернуть обновлённый объект
    return updated_object.scalars().first()


async def delete_task_query(db: AsyncSession, task_id: int, user_id: User) -> bool:
    query = (
        delete(Task)
        .where(and_(Task.id == task_id, Task.user_id == user_id))
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    return result.rowcount > 0