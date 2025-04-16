from dataclasses import dataclass
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Ports.InterfaceOrderRepository import InterfaceOrderRepository
from delivery.infrastructure.Adapters.Postgres.db import get_db_session
from delivery.infrastructure.Adapters.Postgres.Models.OrderAggregate.order import (
    OrderModel,
)


@dataclass
class OrderRepository(InterfaceOrderRepository):
    session: AsyncSession = get_db_session()

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
        result = await self.session.execute(
            select(OrderModel).filter_by(status=OrderStatus.Created)
        )
        model = result.scalars().first()
        return None if not model else Order.model_validate(model)

    async def get_all_assigned(self) -> Optional[Sequence[Order]]:
        try:
            result = await self.session.execute(
                select(OrderModel).filter_by(status=OrderStatus.Assigned)
            )
            models = result.scalars().all()
        except NoResultFound:
            return None

        return [Order.model_validate(model) for model in models]
