from uuid import UUID
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from delivery.core.Domain.SharedKernel.Location import Location
from typing import Self
from pydantic import BaseModel, ConfigDict


class OrderException(Exception):
    """Class for order validation exceptions"""


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    location: Location
    status: str
    courierid: UUID | None

    @classmethod
    def CreateOrder(cls, id: UUID, location: Location) -> Self:
        return cls(id=id, location=location, status=OrderStatus.Created, courierid=None)

    def AssignOrder(self, courier: Courier) -> None:
        self.courierid = courier.id
        self.status = OrderStatus.Assigned

    def CompleteOrder(self) -> None:
        if self.status != OrderStatus.Assigned:
            raise OrderException("Cant complete not assigned order")
        self.status = OrderStatus.Completed
