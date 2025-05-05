from datetime import datetime
from typing import ClassVar
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, registry

from delivery.infrastructure.Adapters.Postgres.db import Base

mapper_registry = registry()


class OutboxModel(Base):
    __tablename__ = "outbox"
    __table_args__: ClassVar[dict] = {"schema": "delivery"}
    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    occured_dttm: Mapped[datetime] = mapped_column(nullable=False)
    processed_dttm: Mapped[datetime] = mapped_column(nullable=True)
