from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth_services import login_user, register_user
from src.database import get_async_session
from src.schemas.auth_dto import Token, UserLogin
from src.schemas.user_dto import UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class RegisterForm:
    def __init__(
        self,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
    ):
        self.username = username
        self.email = email
        self.password = password


@router.post("/register", response_model=Token)
async def register(
    form_data: RegisterForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    user_in = UserCreate(
        username=form_data.username,
        email=form_data.email,
        password=form_data.password,
    )
        
    return await register_user(db, user_in)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_async_session)
):
    username = form_data.username
    password = form_data.password

    user_in = UserLogin(username=username, password=password)
    return await login_user(db, user_in)