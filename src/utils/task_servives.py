from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Task, Tag
from src.queries.task_queries import select_task_with_selection_relationship
from src.queries.tags_queries import select_tag

async def get_task_and_tag_or_404(
    db: AsyncSession,
    task_id: int,
    tag_id: int,
    user_id: int
) -> tuple[Task, Tag]:
    task = await select_task_with_selection_relationship(db=db, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tag = await select_tag(db=db, tag_id=tag_id, user_id=user_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return task, tag
