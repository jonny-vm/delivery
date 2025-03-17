from delivery.core.Domain.Model.OrderAggregate.Order import Order, OrderException
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
import uuid
import pytest


def test_order() -> None:
    loc_1 = Location(5, 5)
    ord_1 = Order.CreateOrder(uuid.uuid4(), loc_1)
    loc_1 = Location(5, 5)
    courier_1 = Courier.CreateCourier("Ivan", "Moto", 2, loc_1)

    assert ord_1.status == OrderStatus.Created
    assert not ord_1.courierid

    with pytest.raises(OrderException):
        ord_1.CompleteOrder()

    ord_1.AssignOrder(courier_1)
    assert ord_1.courierid
    assert ord_1.status == OrderStatus.Assigned

    ord_1.CompleteOrder()
    assert ord_1.status == OrderStatus.Completed
