from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.infrastructure.Adapters.Kafka.OrderStatusChanged.Producer import produce


class OrderCompletedDomainEventHandler:
    @classmethod
    async def handle(cls, order: Order) -> None:
        await produce(orderId=str(order.id), orderStatus=order.status)
