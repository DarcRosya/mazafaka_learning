from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, str_100, str_256 
from .shared_types import intpk, created_at, updated_at

if TYPE_CHECKING:
    from .task import Task  # импорт для аннотаций
    from .tag import Tag

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[intpk]
    username: Mapped[str_100] = mapped_column(unique=True, index=True)
    email: Mapped[str_256] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str_256]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    tasks: Mapped[List["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    tags: Mapped[list["Tag"]] = relationship(
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"