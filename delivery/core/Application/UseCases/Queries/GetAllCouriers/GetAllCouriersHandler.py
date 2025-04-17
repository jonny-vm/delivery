from typing import Optional

from sqlalchemy import text

from delivery.infrastructure.Adapters.Postgres.db import get_db_session

from .GetAllCouriersResponse import Courier, Location


class GetAllCouriersHandler:
    @classmethod
    async def Handle(cls) -> Optional[list[Courier]]:
        result = []
        session = get_db_session()
        result_couriers = await session.execute(
            text(
                """SELECT id, name, location_x::int, location_y::int, status, transport_id
                FROM delivery.courier"""
            )
        )
        couriers = result_couriers.fetchall()
        for courier_row in couriers:
            result.append(await GetAllCouriersHandler.MapToCourier(courier_row))
        await session.close()
        return result

    @classmethod
    async def MapToCourier(cls, result_row) -> Courier:
        x = result_row.location_x
        y = result_row.location_y
        if isinstance(x, int) and isinstance(y, int):
            location = Location(x=x, y=y)
        courier = Courier(
            id=result_row.id,
            name=result_row.name,
            location=location,
            transportId=result_row.transport_id,
        )
        return courier
