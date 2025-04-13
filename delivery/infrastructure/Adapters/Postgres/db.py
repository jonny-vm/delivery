from sqlalchemy.orm import DeclarativeBase
import os


class Base(DeclarativeBase):
    pass


def get_url():
    return os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql+asyncpg:///")
