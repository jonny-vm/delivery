from delivery.infrastructure.Adapters.Kafka.OrderStatusChanged.Producer import produce


class OrderCompletedDomainEventHandler:
    @classmethod
    async def handle(cls, order: dict) -> None:
        await produce(
            orderId=str(order.get("id")), orderStatus=str(order.get("status"))
        )
