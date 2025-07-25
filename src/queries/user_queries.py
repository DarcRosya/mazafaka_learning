import logging
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_dto import UserCreate, UserUpdate
from src.utils.password_hashing import hash_password
from src.models.user import User


async def create_user_query(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password)
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


async def select_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    query = (
        select(User)
        .filter(User.id == user_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def select_user_by_username(db: AsyncSession, username: str) -> User | None:
    query = (
        select(User)
        .filter(User.username == username)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_user_query(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    query = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logging.error(f"Update user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tag not found")  
    # Можно обрабатывать на уровне роутера и возвращать 404
    # Вернуть актуальный объект
    return await select_user_by_id(db, user_id)


async def delete_user_query(db: AsyncSession, user_id: int) -> None:
    # Проверка прав: только сам или админ (логика роутера) !!!!!
    query = (
        delete(User)
        .where(User.id == user_id)
    )

    try:
        result = await db.execute(query)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

