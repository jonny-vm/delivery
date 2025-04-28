import os
from dataclasses import dataclass, field
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from delivery.api.Adapters.Kafka.Basket import basket_contract_pb2
from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderHandler import (
    CreateOrderCommand,
    CreateOrderHandler,
)


class testError(Exception):
    pass


def init_basket_kafka() -> AIOKafkaConsumer:
    topic = os.getenv("BASKET_TOPIC_NAME")
    kservers = os.getenv("BASKET_BOOTSTRAP_SERVERS", "")
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=kservers.split(","),
        group_id="delivery",
    )


@dataclass
class GetBasket:
    consumer: AIOKafkaConsumer = field(default_factory=lambda: init_basket_kafka())

    async def start(self) -> None:
        basket = basket_contract_pb2.BasketConfirmedIntegrationEvent()
        await self.consumer.start()
        try:
            async for message in self.consumer:
                basket.ParseFromString(  # noqa: F841
                    message.value
                )
                basket_id = UUID(basket.basketId)
                street = basket.address.street
                cmd = CreateOrderCommand(basket_id, street)
                await CreateOrderHandler.Handle(cmd)
        finally:
            await self.consumer.stop()
