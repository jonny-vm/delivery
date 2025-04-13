from typing import ClassVar
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship
from delivery.core.Domain.SharedKernel.Location import Location

from uuid import UUID
from sqlalchemy.types import Integer

from delivery.infrastructure.Adapters.Postgres.db import Base


class CourierModel(Base):
    __tablename__ = "courier"
    __table_args__: ClassVar[dict] = {"schema": "delivery"}
    id: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    transport_id: Mapped[int] = mapped_column(ForeignKey("delivery.transport.id"))
    transport: Mapped["TransportModel"] = relationship(
        back_populates="courier", single_parent=True
    )

    location: Mapped[Location] = composite(
        Location,
        Column("location_x", Integer, nullable=False),
        Column("location_y", Integer, nullable=False),
    )


class TransportModel(Base):
    __tablename__ = "transport"
    __table_args__: ClassVar[dict] = {"schema": "delivery"}

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    speed: Mapped[int] = mapped_column(nullable=False)
    courier: Mapped["CourierModel"] = relationship(
        back_populates="transport", single_parent=True
    )
