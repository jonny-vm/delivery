import math
from dataclasses import dataclass
from typing import Self

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
        cls, name: str, transport_name: str, transport_speed: int, location: Location
    ) -> Self:
        return cls(
            name=name,
            transport=Transport(transport_name, transport_speed),
            location=location,
            status=CourierStatus.Free,
        )

    def setFree(self) -> None:
        self.status = CourierStatus.Free

    def setBusy(self) -> None:
        if self.status == CourierStatus.Busy:
            raise CourierException("Courier already is busy")
        self.status = CourierStatus.Busy

    def Move(self, target: Location) -> Location:
        self.location = self.transport.get_next_location(
            current_location=self.location, aim_location=target
        )
        return self.location

    def getCountMoves(self, target: Location) -> int:
        return math.ceil(self.location.get_distance(target) / self.transport.speed)
