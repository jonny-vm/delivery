import importlib.util as imp
import pytest


def test_location() -> None:
    spec = imp.spec_from_file_location(
        "Location", "Delivery.Core\\Domain\\SharedKernel\\Location.py"
    )
    loc_module = imp.module_from_spec(spec)
    spec.loader.exec_module(loc_module)
    a = loc_module.Location(5, 5)
    b = loc_module.Location(1, 10)
    c = loc_module.Location(5, 5)
    assert 1 == loc_module.Location.min_x
    assert 10 == loc_module.Location.max_y
    assert 5 == a.x
    assert 10 == b.y
    assert not a.is_eqiv(b)
    assert a.is_eqiv(c)
    with pytest.raises(loc_module.CoordinateException):
        loc_module.Location(0, 11)
