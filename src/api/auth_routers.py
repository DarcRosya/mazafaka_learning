from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.user import User
from src.utils.auth_services import (
    login_user,
    register_user, 
    validate_user,
    get_current_user_for_refresh,
)
from src.schemas.auth_dto import (
    TokenInfo, 
    RegisterForm
)
from src.schemas.user_dto import UserCreate
from src.utils.jwt_access import create_access_token

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/register", response_model=TokenInfo)
async def register(
    form_data: RegisterForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    user_in = UserCreate(
        username=form_data.username,
        email=form_data.email,
        password=form_data.password,
    )
    return await register_user(db=db, user_in=user_in)


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