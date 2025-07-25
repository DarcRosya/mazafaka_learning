from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.user import User
from src.schemas.tag_dto import TagRead, TagUpdate
from src.utils.jwt_access import get_current_user

from src.queries.tags_queries import (
    select_tags, 
    select_tags_on_task,
    create_tag_query,
    update_tag_query,
    delete_tag_query,
)


router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.post(
    "",
    response_model=TagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tag",
    response_description="Created tag"
)
async def create_tag(
    tag_name: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await create_tag_query(db=db, tag_in=tag_name, user_id=current_user.id)


@router.get(
    "",
    response_model=list[TagRead],
    summary="Get all tags",
    response_description="List of tags"
)
async def get_tags(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await select_tags(db=db, user_id=current_user.id)


@router.get(
    "/{task_id}/tags",
    response_model=list[TagRead],
    status_code=status.HTTP_200_OK,
    summary="Get all tags linked to the task",
    response_description="List of tags"
)
async def get_tags_that_linked_to_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await select_tags_on_task(db=db, task_id=task_id, user_id=current_user.id)


@router.patch(
    "/{tag_id}",
    response_model=TagRead,
    summary="Update a tag by ID",
    response_description="Updated tag",
    responses={404: {"description": "Tag not found"}}
)
async def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    updated_tag = await update_tag_query(db=db, tag_id=tag_id, tag_update=tag_in, user_id=current_user.id)
    TagRead.model_validate(updated_tag, from_attributes=True)


@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a tag by ID",
    response_description="Tag deleted",
    responses={404: {"description": "Tag not found"},
               204: {"description": "Task deleted successfully"}
    }
)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    await delete_tag_query(db=db, tag_id=tag_id, user_id=current_user.id)