import pytest
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.core.Domain.Model.CourierAggregate.Transport import (
    Transport,
    TransportException,
)


def test_transport() -> None:
    a = Transport(name="on_foot", speed=1)
    b = Transport(name="auto", speed=3)
    c = Transport(name="on_foot", speed=1)

    assert a != c
    assert 3 == b.move()

    achieve_result = False
    max_step = (Location.max_x + Location.max_y) - 1
    loc_1 = Location.get_random_coordinate()
    print(str(loc_1))
    loc_2 = Location.get_random_coordinate()
    print(str(loc_2))
    for step in range(1, max_step):
        loc_1 = b.get_next_location(loc_1, loc_2)
        print(f"step={step}, {str(loc_1)}")
        if loc_1 == loc_2:
            achieve_result = True
            break
    assert achieve_result

    loc_1 = Location(Location.min_x, Location.min_y)
    loc_2 = Location(Location.max_x, Location.max_y)

    for step in range(max_step):
        loc_1 = a.get_next_location(loc_1, loc_2)
        if loc_1 == loc_2:
            break
    assert step == max_step - 2

    with pytest.raises(TransportException):
        a.name = ""

    with pytest.raises(TransportException):
        a.speed = 5
