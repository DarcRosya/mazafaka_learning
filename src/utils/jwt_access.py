from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.password_hashing import oauth2_scheme
from src.config.settings import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
EMAIL_TOKEN_TYPE = "email"


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> dict:
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def encode_jwt(
    payload: dict,
    private_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    elif expire_minutes:
        expire = now + timedelta(minutes=expire_minutes)
    else:
        expire = now + timedelta(minutes=15)

    to_encode.update(
        exp=expire,
        iat=now,
        # jti=str(uuid.uuid4()),
    )
    return jwt.encode(to_encode, private_key, algorithm)


def create_jwt(
        token_type: str, 
        token_data: dict,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None, 
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def create_access_token(user: User) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": str(user.id), 
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE, 
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

def create_email_token(user: User) -> str:
    jwt_payload = {
        "sub": user.email
    }
    return create_jwt(
        token_type=EMAIL_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=10, 
    )


async def get_current_token_payload(
        token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def validate_token_type(payload: dict, token_type: str) -> None:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type!r} expected {token_type!r}"
        )
    
    
async def get_user_by_token_sub(payload: dict, db: AsyncSession) -> User:
    try:
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    result = await db.execute(
        select(User).options(selectinload(User.tasks)).filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user



