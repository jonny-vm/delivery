import os

from aiokafka import AIOKafkaProducer

from delivery.infrastructure.Adapters.Kafka.OrderStatusChanged.order_contract_pb2 import (
    OrderStatusChangedIntegrationEvent,
)


async def produce(orderId: str, orderStatus: str):
    try:
        msg = OrderStatusChangedIntegrationEvent(
            orderId=orderId, orderStatus=orderStatus
        )
        topic = os.getenv("PUBLISH_TOPIC_NAME")
        kservers = os.getenv("PUBLISH_BOOTSTRAP_SERVERS", "")
        producer = AIOKafkaProducer(bootstrap_servers=kservers.split(","))
        await producer.start()
        await producer.send_and_wait(topic, value=msg.SerializeToString())
    finally:
        await producer.stop()
