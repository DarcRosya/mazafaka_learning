from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base
from .shared_types import intpk

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str]

    user: Mapped["User"] = relationship(
        back_populates="tags",
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="tags",
        secondary="task_tags"
    )


class TaskTags(Base):
    __tablename__ = "task_tags"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )