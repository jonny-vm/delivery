from typing import ClassVar
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column, registry, composite
from delivery.core.Domain.SharedKernel.Location import Location
from uuid import UUID
from sqlalchemy.types import Integer

from delivery.infrastructure.Adapters.Postgres.db import Base


mapper_registry = registry()


class OrderModel(Base):
    __tablename__ = "order"
    __table_args__: ClassVar[dict] = {"schema": "delivery"}
    id: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False)
    courierid: Mapped[UUID] = mapped_column(nullable=True)

    location: Mapped[Location] = composite(
        Location,
        Column("location_x", Integer, nullable=False),
        Column("location_y", Integer, nullable=False),
    )
