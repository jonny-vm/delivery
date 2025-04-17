import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_url():
    return os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql+asyncpg:///")


def get_db_session():
    db_url = get_url()
    engine = create_async_engine(
        url=db_url,
        pool_pre_ping=True,
        connect_args={},
    )
    return AsyncSession(engine)
