from abc import abstractmethod

from delivery.core.Domain.Model.OrderAggregate.Order import Order


class InterfaceBusProducer:
    @abstractmethod
    @classmethod
    async def produce(cls, order: Order) -> None:
        pass
