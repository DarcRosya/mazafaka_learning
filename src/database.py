from src.config import settings
from typing import Annotated, AsyncGenerator
from sqlalchemy import String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    url=settings.DATABASE_URL,
    # echo=True,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

str_256 = Annotated[str, String(256)]
str_100 = Annotated[str, String(100)]

class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session