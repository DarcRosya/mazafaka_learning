from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_async_session
from src.models.user import User
from src.queries.user_queries import select_user_by_email
from src.utils.auth_services import (
    login_user,
    register_user, 
    validate_user,
    get_current_user_for_refresh,
)
from src.utils.jwt_access import create_access_token, decode_jwt
from src.schemas.auth_dto import (
    TokenInfo, 
    RegisterForm
)
from src.schemas.user_dto import UserCreate



http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register")
async def register(
    background_tasks: BackgroundTasks,
    form_data: RegisterForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    user_in = UserCreate(
        username=form_data.username,
        email=form_data.email,
        password=form_data.password,
    )
    return await register_user(db=db, user_in=user_in, background_tasks=background_tasks)


@router.get("/verify")
async def verify_email(
    token: str, 
    db: AsyncSession = Depends(get_async_session)
):
    payload = decode_jwt(token)
    email = payload["sub"]
    user = await select_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    await db.commit()
    return {"msg": "Email verified successfully"}


@router.post("/login", response_model=TokenInfo)
async def login(
    user: User = Depends(validate_user)
):
    # user = await validate_user(username=user.username, password=user.password)
    return await login_user(user=user)


@router.post(
    "/refresh", 
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def refresh_token(
    current_user: User = Depends(get_current_user_for_refresh),
):
    new_access_token = create_access_token(current_user)
    return TokenInfo(
        access_token=new_access_token,
        refresh_token=None,  
    )


