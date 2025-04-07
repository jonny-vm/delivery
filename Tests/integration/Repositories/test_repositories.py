import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from delivery.infrastructure.Adapters.Postgres.Repositories.CourierRepository import (
    CourierRepository,
)
from delivery.core.Domain.SharedKernel.Location import Location
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from sqlalchemy.ext.asyncio import async_sessionmaker
from delivery.infrastructure.Adapters.Postgres.Repositories.OrderRepository import (
    OrderRepository,
)
from delivery.core.Domain.Model.OrderAggregate.OrderStatus import OrderStatus
from delivery.core.Domain.Model.OrderAggregate.Order import Order
import uuid
from typing import Sequence, Optional


@pytest.mark.usefixtures("db_init")
@pytest.mark.first
async def test_addorder(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(3, 7)
        rep = OrderRepository(session)
        ord = Order.CreateOrder(uuid.uuid4(), loc)
        result = await rep.add(ord)
        assert isinstance(result, Order)


async def test_getorder(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(7, 5)
        rep = OrderRepository(session)
        ord = Order.CreateOrder(uuid.uuid4(), loc)
        order_add_agr = await rep.add(ord)
        if isinstance(order_add_agr, Order):
            order_get_agr = await rep.get(order_add_agr.id)
            if order_get_agr:
                assert order_get_agr.__class__ == order_add_agr.__class__
                assert order_get_agr.courierid == order_add_agr.courierid
            else:
                assert False
        else:
            assert False


async def test_updateorder(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(6, 5)
        rep = OrderRepository(session)
        ord = Order.CreateOrder(uuid.uuid4(), loc)
        order_add_agr = await rep.add(ord)
        if isinstance(order_add_agr, Order):
            loc = Location(9, 9)
            ord = Order.CreateOrder(uuid.uuid4(), loc)
            order_upd_agr = await rep.update(order_add_agr.id, ord)
            if order_upd_agr:
                assert order_upd_agr.__class__ == order_add_agr.__class__
                assert order_upd_agr.courierid == order_add_agr.courierid
                assert order_upd_agr.location.x == loc.x
            else:
                assert False
        else:
            assert False


async def test_anyone_created_order(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(6, 5)
        rep = OrderRepository(session)
        ord = Order.CreateOrder(uuid.uuid4(), loc)
        await rep.add(ord)
        order = await rep.get_anyone_created()
        assert True if isinstance(order, Order) else False
        assert order.status == OrderStatus.Created if order else False


async def test_all_assigned_orders(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session, session.begin():
        loc_ord = Location(6, 5)
        rep = OrderRepository(session)
        ord = Order.CreateOrder(uuid.uuid4(), loc_ord)
        await rep.add(ord)
        loc_cour = Location(3, 9)
        cour = Courier.CreateCourier(
            name="cour1", transport_name="tr1", transport_speed=2, location=loc_cour
        )
        ord.AssignOrder(cour)
        await rep.update(ord.id, ord)
        all_assigned: Optional[Sequence] = await rep.get_all_assigned()
        assert all_assigned
        assert len(all_assigned) > 0


async def test_addcourier(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(2, 5)
        crep = CourierRepository(session)
        cour = Courier.CreateCourier(
            name="cour1", transport_name="tr1", transport_speed=2, location=loc
        )
        result = await crep.add(cour)
        assert isinstance(result, Courier)


async def test_getcourier(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(7, 5)
        rep = CourierRepository(session)
        cour = Courier.CreateCourier(
            name="cour2", transport_name="tr2", transport_speed=1, location=loc
        )
        courier_add_agr = await rep.add(cour)
        if isinstance(courier_add_agr, Courier):
            assert True
            courier_get_agr = await rep.get(courier_add_agr.id)
            if courier_get_agr:
                assert courier_get_agr.__class__ == courier_add_agr.__class__
                assert courier_get_agr.name == courier_add_agr.name
                assert (
                    courier_get_agr.transport.speed == courier_add_agr.transport.speed
                )
            else:
                assert False
        else:
            assert False


async def test_updatecourier(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(6, 5)
        crep = CourierRepository(session)
        cour = Courier.CreateCourier(
            name="cour1", transport_name="tr1", transport_speed=2, location=loc
        )
        courier_add_agr = await crep.add(cour)
        if isinstance(courier_add_agr, Courier):
            loc = Location(9, 9)
            cour = courier_add_agr
            cour.location = loc
            cour.transport.speed = 3
            courier_upd_agr = await crep.update(courier_add_agr.id, cour)
            if courier_upd_agr:
                assert courier_upd_agr.__class__ == courier_add_agr.__class__
                assert courier_upd_agr.transport.id == courier_add_agr.transport.id
                assert courier_upd_agr.transport.speed == cour.transport.speed
            else:
                assert False
        else:
            assert False


async def test_all_free_couriers(db_conn, exec_db_tests) -> None:
    if not exec_db_tests:
        pytest.skip("DB not connected")

    async with async_sessionmaker(db_conn.engine)() as session:
        loc = Location(6, 5)
        crep = CourierRepository(session)
        cour = Courier.CreateCourier(
            name="cour1", transport_name="tr1", transport_speed=2, location=loc
        )
        courier_add_agr = await crep.add(cour)
        all_free: Optional[Sequence] = await crep.get_all_free()
        assert all_free
        assert len(all_free) > 0


@pytest.mark.last
@pytest.mark.usefixtures("db_rollback")
async def test_rlbck(db_rollback) -> None:
    assert True
