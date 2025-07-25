from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.password_hashing import verify_password
from src.utils.jwt_access import create_access_token
from src.queries.user_queries import select_user_by_username
from src.schemas.auth_dto import Token, UserLogin
from src.schemas.user_dto import UserCreate
from src.queries.user_queries import create_user_query
    

# опционально сделать логику с выдачей токена лишь после потверждения email
async def register_user(db: AsyncSession, user_in: UserCreate) -> Token:
    existing_user = await select_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await create_user_query(db, user_in)

    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


async def login_user(db: AsyncSession, user_in: UserLogin) -> Token:
    user = await select_user_by_username(db, user_in.username)

    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # создаём токен
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
