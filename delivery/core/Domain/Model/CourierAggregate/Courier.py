from dataclasses import dataclass
from typing import Any
from uuid import UUID
from delivery.core.Domain.Model.CourierAggregate.CourierStatus import CourierStatus
from delivery.core.Domain.Model.CourierAggregate.Transport import Transport
from delivery.core.Domain.SharedKernel.Entity import Aggregate
from delivery.core.Domain.SharedKernel.Location import Location


class CourierException(Exception):
    """Class for courier validation exceptions"""


@dataclass
class Courier(Aggregate):
    name: str
    transport: Transport
    location: Location
    status: str

    @classmethod
    def CreateCourier(
        cls, name: str, transport_name: Any, transport_speed: Any, location: Location
    ) -> UUID:
        return cls(
            name=name,
            transport=Transport(transport_name, transport_speed),
            location=location,
            status=CourierStatus.Free,
        ).id

    def setFree(self) -> None:
        self.status = CourierStatus.Free if CourierStatus.Busy else self.status

    def setBusy(self) -> bool:
        if CourierStatus.Free:
            self.status = CourierStatus.Busy
            return True
        return False
