from typing import Optional

from sqlalchemy import text

from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.infrastructure.Adapters.Postgres.db import get_db_session

from .GetNotCompletedOrdersResponse import Location, Order


class GetNotCompletedOrdersHandler:
    @classmethod
    async def Handle(cls) -> Optional[list[Order]]:
        result = []
        session = get_db_session()
        result_orders = await session.execute(
            text(
                f"""SELECT id, courierid, location_x::int, location_y::int, status
                FROM delivery.order
                where status != '{OrderStatus.Completed}'"""
            )
        )
        orders = result_orders.fetchall()
        for order_row in orders:
            result.append(await GetNotCompletedOrdersHandler.MapToOrder(order_row))
        await session.close()
        return result

    @classmethod
    async def MapToOrder(cls, result_row):
        x = result_row.location_x
        y = result_row.location_y
        if isinstance(x, int) and isinstance(y, int):
            location = Location(x=x, y=y)
        courier = Order(
            id=result_row.id,
            location=location,
        )
        return courier
