from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderCommand import (
    CreateOrderCommand,
)
from delivery.core.Domain.Model.OrderAggregate.Order import Order, OrderException
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.infrastructure.Adapters.Postgres.Repositories.OrderRepository import (
    OrderRepository,
)


class CreateOrderHandler:
    @classmethod
    async def Handle(cls, message: CreateOrderCommand) -> Order:
        orderid = message.BasketId
        rep = OrderRepository()
        rep.session.begin()
        if await rep.get(orderid):
            raise OrderException(f"Order with id='{orderid}' already exists")

        order_loc = Location.get_random_coordinate()

        order = await rep.add(Order.CreateOrder(id=orderid, location=order_loc))

        if not (isinstance(order, Order) and order.status == OrderStatus.Created):
            raise OrderException(f"Order id='{orderid}' is not created")

        await rep.session.commit()

        return order
