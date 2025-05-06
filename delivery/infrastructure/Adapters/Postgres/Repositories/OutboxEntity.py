import datetime
import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.infrastructure.Adapters.Postgres.db import get_db_session
from delivery.infrastructure.Adapters.Postgres.Models.Outbox.outbox import OutboxModel


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Location):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


@dataclass
class OutboxEntity:
    session: AsyncSession = get_db_session()

    async def add(self, order: Order) -> None:
        result = await self.session.execute(  # noqa: F841
            insert(OutboxModel).values(
                {
                    "id": order.id,
                    "type": type(order).__name__,
                    "content": str(json.dumps(order.__dict__, cls=UUIDEncoder)),
                    "occured_dttm": datetime.datetime.now(datetime.UTC),
                }
            ),
        )

    async def get(self) -> list[dict[str, Any] | None]:
        result = await self.session.execute(  # noqa: F841
            select(OutboxModel).filter_by(processed_dttm=None)
        )
        outbox_messages = []
        for message in result.scalars().all():
            outbox_messages.append(message.__dict__)
        return outbox_messages

    async def update(self, id: UUID) -> None:
        result = await self.session.execute(  # noqa: F841
            update(OutboxModel)
            .filter_by(id=id)
            .values(
                {
                    "processed_dttm": datetime.datetime.now(),
                }
            )
        )
