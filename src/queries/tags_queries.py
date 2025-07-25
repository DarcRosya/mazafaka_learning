from fastapi import HTTPException
from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.models.tag import Tag
from src.schemas.tag_dto import TagCreate, TagUpdate


async def create_tag_query(db: AsyncSession, tag_in: TagCreate, user_id: int) -> Tag:
    data = tag_in.model_dump()
    tag = Tag(**data, user_id=user_id)
    try:
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return tag
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


async def select_tag(db: AsyncSession, tag_id: int, user_id: int) -> Tag | None:
    query = (
        select(Tag)
        .filter(and_(Tag.id == tag_id, Tag.user_id == user_id))
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def select_tags(db: AsyncSession, user_id: int) -> list[Tag]:
    query = (
        select(Tag)
        .filter(Tag.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def select_tags_on_task(db: AsyncSession, task_id: int, user_id: int) -> list[Tag]:
    query = (
        select(Tag)
        .join(Task, Tag.tasks) # указываем таблицу и путь
        .filter(Task.id == task_id, Tag.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def update_tag_query(db: AsyncSession, tag_id: int, tag_update: TagUpdate, user_id: int) -> Tag:
    data = tag_update.model_dump(exclude_unset=True)

    query = (
        update(Tag)
        .filter(and_(Tag.user_id == user_id, Tag.id == tag_id))
        .values(**data)
    )

    try: 
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    updated_object = await db.execute(select(Tag).where(Tag.id == tag_id))
    return updated_object.scalars().first()


async def delete_tag_query(db: AsyncSession, tag_id: int, user_id: int) -> None:
    query = (
        delete(Tag)
        .filter(and_(Tag.id == tag_id, Tag.user_id == user_id))
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found or access denied")