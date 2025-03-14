from dataclasses import dataclass
from uuid import UUID
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from delivery.core.Domain.SharedKernel.Location import Location


class OrderException(Exception):
    """Class for order validation exceptions"""


@dataclass
class Order:
    id: UUID
    location: Location
    status: str
    courierid: UUID | None = None

    @classmethod
    def CreateOrder(cls, id: UUID, location: Location) -> None:
        cls(id=id, location=location, status=OrderStatus.Created)

    def AssignOrder(self, courier: Courier) -> None:
        if courier.setBusy():
            self.courierid = courier.id
            self.status = OrderStatus.Assigned

    def CompleteOrder(self) -> None:
        if not self.courierid or self.status != OrderStatus.Assigned:
            raise OrderException("Cant complete not assigned order")
        self.status = OrderStatus.Completed
        # Courier[self.courierid].setFree()
