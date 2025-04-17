from dataclasses import dataclass
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from delivery.core.Domain.Model.CourierAggregate.CourierStatus import CourierStatus
from delivery.core.Ports.InterfaceCourierRepository import InterfaceCourierRepository
from delivery.infrastructure.Adapters.Postgres.db import get_db_session
from delivery.infrastructure.Adapters.Postgres.Models.CourierAggregate.courier import (
    CourierModel,
    TransportModel,
)


@dataclass
class CourierRepository(InterfaceCourierRepository):
    session: AsyncSession = get_db_session()

    async def get(self, id: UUID) -> Optional[Courier]:
        try:
            result_courier = await self.session.execute(
                select(CourierModel).filter_by(id=id)
            )
            model_courier = result_courier.scalar_one()
            result_transport = await self.session.execute(
                select(TransportModel).filter_by(id=model_courier.transport_id)
            )
            model_courier.transport = result_transport.scalar_one()
        except NoResultFound:
            return None
        return Courier.model_validate(model_courier)

    async def add(self, courier: Courier) -> Optional[Courier]:
        result_transport = await self.session.execute(  # noqa: F841
            insert(TransportModel)
            .values(
                {
                    "id": courier.transport.id,
                    "name": courier.transport.name,
                    "speed": courier.transport.speed,
                }
            )
            .returning(TransportModel),
        )

        result_courier = await self.session.execute(
            insert(CourierModel)
            .values(
                {
                    "id": courier.id,
                    "status": courier.status,
                    "name": courier.name,
                    "location_x": courier.location.x,
                    "location_y": courier.location.y,
                    "transport_id": courier.transport.id,
                }
            )
            .returning(CourierModel),
        )
        model_courier = result_courier.scalar_one()

        return Courier.model_validate(model_courier)

    async def update(self, courier: Courier) -> Optional[Courier]:
        try:
            result_courier = await self.session.execute(
                update(CourierModel)
                .filter_by(id=courier.id)
                .values(
                    {
                        "status": courier.status,
                        "name": courier.name,
                        "location_x": courier.location.x,
                        "location_y": courier.location.y,
                        "transport_id": courier.transport.id,
                    }
                )
                .returning(CourierModel)
            )
            model = result_courier.scalar_one()
            result_transport = await self.session.execute(  # noqa: F841
                update(TransportModel)
                .filter_by(id=model.transport_id)
                .values(
                    {
                        "name": courier.transport.name,
                        "speed": courier.transport.speed,
                    }
                )
                .returning(TransportModel)
            )
        except NoResultFound:
            return None

        return Courier.model_validate(model)

    async def get_all_free(self) -> Optional[Sequence[Courier]]:
        try:
            result_couriers = await self.session.execute(
                select(CourierModel).filter_by(status=CourierStatus.Free)
            )
            models_couriers = result_couriers.scalars().all()
            models_couriers_with_transport = []
            for model in models_couriers:
                result_transport = await self.session.execute(
                    select(TransportModel).filter_by(id=model.transport_id)
                )
                model.transport = result_transport.scalar_one()
                models_couriers_with_transport.append(model)
        except NoResultFound:
            return None

        return [
            Courier.model_validate(model) for model in models_couriers_with_transport
        ]
