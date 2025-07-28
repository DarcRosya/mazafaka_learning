from fastapi import Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.user import User
from src.schemas.auth_dto import TokenInfo
from src.schemas.user_dto import UserCreate
from src.utils.password_hashing import verify_password
from src.utils.jwt_access import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    get_current_token_payload,
    get_user_by_token_sub,
    validate_token_type,
)
from src.queries.user_queries import (
    create_user_query, 
    select_user_by_username,
)
    

async def register_user(db: AsyncSession, user_in: UserCreate) -> TokenInfo:
    existing_user = await select_user_by_username(db=db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    user = await create_user_query(db=db, user_in=user_in)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def login_user(user: User) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def validate_user(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    user = await select_user_by_username(db=db, username=username)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(get_async_session),
    ):
        await validate_token_type(payload=payload, token_type=self.token_type)
        return await get_user_by_token_sub(payload=payload, db=db)
    

get_current_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)