from delivery.core.Application.DomainEventHandlers.OrderCompletedDomainEventHandler import (
    OrderCompletedDomainEventHandler,
)
from delivery.core.Ports.IMessageBusProducer import InterfaceBusProducer, Order


class OrderCompletedDomainEvent(InterfaceBusProducer):
    @classmethod
    async def produce(cls, order: Order) -> None:
        await OrderCompletedDomainEventHandler.handle(order)
