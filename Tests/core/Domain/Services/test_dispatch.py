import pytest
import uuid
from delivery.core.Domain.Services.IDispatchService import Dispatch
from delivery.core.Domain.Services.DispatchService import DispatchException
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier


def test_dispatch() -> None:
    loc_1 = Location(5, 5)
    courier_1 = Courier.CreateCourier("Ivan", "Moto", 2, loc_1)
    loc_2 = Location(1, 5)
    courier_2 = Courier.CreateCourier("Alex", "On_foot", 1, loc_2)
    loc_3 = Location(7, 3)
    courier_3 = Courier.CreateCourier("John", "Auto", 3, loc_3)

    loc_ord = Location(1, 3)
    ord = Order.CreateOrder(uuid.uuid4(), loc_ord)
    assert Dispatch(ord, [courier_1, courier_2, courier_3]).name == "Alex"

    loc_ord = Location(6, 5)
    ord.location = loc_ord
    assert Dispatch(ord, [courier_1, courier_2, courier_3]).name == "Ivan"

    loc_ord = Location(9, 4)
    ord.location = loc_ord
    assert Dispatch(ord, [courier_1, courier_2, courier_3]).name == "John"

    courier_1.setBusy()
    courier_2.setBusy()
    with pytest.raises(DispatchException):
        Dispatch(ord, [courier_1, courier_2])
