import asyncio
import json

from delivery.core.Application.DomainEventHandlers.OrderCompletedDomainEventHandler import (
    OrderCompletedDomainEventHandler,
)
from delivery.infrastructure.Adapters.Postgres.Repositories.OutboxEntity import (
    OutboxEntity,
)


class ProcessOutboxMessages:
    @classmethod
    async def process(cls) -> None:
        try:
            outbox = OutboxEntity()
            while True:
                outbox_messages = await outbox.get()
                for message in outbox_messages:
                    if message:
                        order = json.loads(message.get("content", {}))
                        await OrderCompletedDomainEventHandler.handle(order)
                        await outbox.update(message.get("id"))
                        await outbox.session.commit()
                await asyncio.sleep(5.0)
        finally:
            await outbox.session.close()
