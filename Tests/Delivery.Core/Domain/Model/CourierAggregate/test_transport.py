import importlib.util as imp
import pytest


def test_transport(capsys) -> None:
    spec = imp.spec_from_file_location(
        "Transport", "Delivery.Core\\Domain\\Model\\CourierAggregate\\Transport.py"
    )
    trnsp_module = imp.module_from_spec(spec)
    spec.loader.exec_module(trnsp_module)

    a = trnsp_module.Transport(name="walk", speed=1)
    b = trnsp_module.Transport(name="auto", speed=3)
    c = trnsp_module.Transport(name="walk", speed=1)

    assert a != c
    assert 3 == b.move()

    achieve_result = False
    max_step = (trnsp_module.Location.max_x + trnsp_module.Location.max_y) - 1
    loc_1 = trnsp_module.Location.get_random_coordinate()
    print(str(loc_1))
    loc_2 = trnsp_module.Location.get_random_coordinate()
    print(str(loc_2))
    for step in range(1, max_step):
        loc_1 = b.get_next_location(loc_1, loc_2)
        print(f"step={step}, {str(loc_1)}")
        if loc_1 == loc_2:
            achieve_result = True
            break
    assert achieve_result

    loc_1 = trnsp_module.Location(
        trnsp_module.Location.min_x, trnsp_module.Location.min_y
    )
    loc_2 = trnsp_module.Location(
        trnsp_module.Location.max_x, trnsp_module.Location.max_y
    )

    for step in range(1, max_step):
        loc_1 = a.get_next_location(loc_1, loc_2)
        if loc_1 == loc_2:
            break
    assert step == max_step - 1

    with pytest.raises(trnsp_module.TransportException):
        a.name = ""

    with pytest.raises(trnsp_module.TransportException):
        a.speed = 5
