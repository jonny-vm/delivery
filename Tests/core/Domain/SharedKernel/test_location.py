import pytest
from delivery.core.Domain.SharedKernel.Location import Location, CoordinateException


def test_location() -> None:
    a = Location(5, 5)
    b = Location(1, 10)
    c = Location(5, 5)
    assert 1 == Location.min_x
    assert 10 == Location.max_y
    assert 5 == a.x
    assert 10 == b.y
    assert a == c
    assert a != b
    assert 9 == a.get_distance(b)
    with pytest.raises(CoordinateException):
        Location(0, 11)
