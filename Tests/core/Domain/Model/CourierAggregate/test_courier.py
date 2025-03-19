import pytest
from delivery.core.Domain.Model.CourierAggregate.Courier import (
    Courier,
    CourierException,
)
from delivery.core.Domain.Model.CourierAggregate.CourierStatus import CourierStatus

from delivery.core.Domain.SharedKernel.Location import Location


def test_courier() -> None:
    loc_1 = Location(5, 5)
    loc_2 = Location(1, 10)
    courier_1 = Courier.CreateCourier("Ivan", "Moto", 2, loc_1)
    assert courier_1.status == CourierStatus.Free

    with pytest.raises(CourierException):
        for idx in range(2):
            courier_1.setBusy()

    for idx in range(2):
        courier_1.setFree()
    assert courier_1.status == CourierStatus.Free

    assert courier_1.getCountMoves(loc_2) == 5

    for idx in range(3):
        courier_1.Move(loc_2)
    assert courier_1.getCountMoves(loc_2) == 2

    for idx in range(10):
        courier_1.Move(loc_2)
    assert courier_1.getCountMoves(loc_2) == 0

    assert courier_1.location == loc_2
