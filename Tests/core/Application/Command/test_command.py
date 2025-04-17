import uuid

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from delivery.core.Application.UseCases.Commands.AssignOrders.AssignOrdersHandler import (
    AssignOrdersHandler,
)
from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderCommand import (
    CreateOrderCommand,
)
from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderHandler import (
    CreateOrderHandler,
)
from delivery.core.Domain.Model.CourierAggregate.Courier import (
    Courier,
    CourierException,
)
from delivery.core.Domain.Model.OrderAggregate.Order import OrderException
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.infrastructure.Adapters.Postgres.Repositories.CourierRepository import (
    CourierRepository,
)


async def test_CreateOrder(exec_db_tests):
    if not exec_db_tests:
        pytest.skip("DB not connected")
    cmd = CreateOrderCommand(uuid.uuid4(), "street 1")
    order = await CreateOrderHandler.Handle(cmd)
    assert order.status == OrderStatus.Created
    with pytest.raises(OrderException):
        await CreateOrderHandler.Handle(cmd)


async def test_AssignOrder(db_conn, exec_db_tests):
    if not exec_db_tests:
        pytest.skip("DB not connected")
    cmd = CreateOrderCommand(uuid.uuid4(), "street 1")
    order = await CreateOrderHandler.Handle(cmd)
    with pytest.raises(CourierException):
        assert await AssignOrdersHandler.Handle()

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(2, 5)
        crep = CourierRepository(session)
        cour = Courier.CreateCourier(
            name="cour1", transport_name="tr1", transport_speed=2, location=loc
        )
        await crep.add(cour)
        await session.commit()

    order = await AssignOrdersHandler.Handle()
    assert order.status == OrderStatus.Assigned
    assert order.courierid == cour.id
