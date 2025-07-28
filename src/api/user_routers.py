from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.queries.user_queries import (
    update_user_query, 
    delete_user_query 
)
from src.schemas.task_dto import TaskRead
from src.schemas.user_dto import UserRead, UserUpdate
from src.utils.auth_services import get_current_user
from src.models.user import User

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/users",      # это общий префикс
    tags=["Users"],        # это группа, удобно в Swagger
    dependencies=[Depends(http_bearer)],
)

@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user info",
    response_description="Current user data"
)
async def get_user(
    current_user: User = Depends(get_current_user)
):
    return UserRead.model_validate(current_user, from_attributes=True)


@router.get(
    "/me/tasks",
    response_model=list[TaskRead],
    summary="Get tasks of current user",
    response_description="List of tasks belonging to the current user"
)
async def get_user_tasks(
    current_user: User = Depends(get_current_user),
):
    return current_user.tasks


@router.patch(
    "/me",
    response_model=UserRead,
    summary="Update current user",
    response_description="Updated user object",
    responses={404: {"description": "User not found"}}
)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    updated_user = await update_user_query(db=db, user_id=current_user.id, user_update=user_update)
    return UserRead.model_validate(updated_user, from_attributes=True)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user",
    response_description="User deleted successfully",
    responses={404: {"description": "Tag not found"},
               204: {"description": "Task deleted successfully"}
    }
)
async def delete_user(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_session),
):
    await delete_user_query(db=db, user_id=current_user.id)








# @router.get("/users/me/")
# def auth_user_check_self_info(
#     payload: dict = Depends(get_current_token_payload),
#     user: UserSchema = Depends(get_current_active_auth_user),
# ):
#     iat = payload.get("iat")
#     return {
#         "username": user.username,
#         "email": user.email,
#         "logged_in_at": iat,
#     }


# def get_current_token_payload(
#     token: str = Depends(oauth2_scheme),
# ) -> dict:
#     try:
#         payload = auth_utils.decode_jwt(
#             token=token,
#         )
#     except InvalidTokenError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"invalid token error: {e}",
#         )
#     return payload



# def get_current_active_auth_user(
#     user: UserSchema = Depends(get_current_auth_user),
# ):
#     if user.active:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="inactive user",
#     )


# get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)



# def get_auth_user_from_token_of_type(token_type: str):
#     def get_auth_user_from_token(
#         payload: dict = Depends(get_current_token_payload),
#     ) -> UserSchema:
#         validate_token_type(payload, token_type)
#         return get_user_by_token_sub(payload)

#     return get_auth_user_from_token



# def get_current_token_payload(
#     token: str = Depends(oauth2_scheme),
# ) -> dict:
#     try:
#         payload = auth_utils.decode_jwt(
#             token=token,
#         )
#     except InvalidTokenError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"invalid token error: {e}",
#         )
#     return payload