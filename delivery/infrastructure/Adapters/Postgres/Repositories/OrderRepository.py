from delivery.core.Ports.InterfaceOrderRepository import InterfaceOrderRepository

from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.infrastructure.Adapters.Postgres.Models.OrderAggregate.order import (
    OrderModel,
)
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from typing import Sequence, Optional
from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from uuid import UUID


class OrderRepository(InterfaceOrderRepository):
    async def get(self, id: UUID) -> Optional[Order]:
        try:
            result = await self.session.execute(select(OrderModel).filter_by(id=id))
            model = result.scalar_one()
        except NoResultFound:
            return None
        return Order.model_validate(model)

    async def add(self, order: Order) -> Optional[Order]:
        result = await self.session.execute(
            insert(OrderModel).values(**order.__dict__).returning(OrderModel),
        )
        model = result.scalar_one()

        return Order.model_validate(model)

    async def update(self, id: UUID, order: Order) -> Optional[Order]:
        try:
            result = await self.session.execute(
                update(OrderModel)
                .filter_by(id=id)
                .values(
                    {
                        "status": order.status,
                        "courierid": order.courierid,
                        "location_x": order.location.x,
                        "location_y": order.location.y,
                    }
                )
                .returning(OrderModel)
            )
            model = result.scalar_one()
        except NoResultFound:
            return None

        return Order.model_validate(model)

    async def get_anyone_created(self) -> Optional[Order]:
        try:
            result = await self.session.execute(
                select(OrderModel).filter_by(status=OrderStatus.Created)
            )
            model = result.scalars().first()
        except NoResultFound:
            return None
        return Order.model_validate(model)

    async def get_all_assigned(self) -> Optional[Sequence[Order]]:
        try:
            result = await self.session.execute(
                select(OrderModel).filter_by(status=OrderStatus.Assigned)
            )
            models = result.scalars().all()
        except NoResultFound:
            return None

        return [Order.model_validate(model) for model in models]
