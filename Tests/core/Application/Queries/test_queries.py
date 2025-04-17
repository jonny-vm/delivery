import pytest

import delivery.core.Application.UseCases.Queries.GetAllCouriers.GetAllCouriersHandler as hdl_allcouriers
import delivery.core.Application.UseCases.Queries.GetNotCompletedOrders.GetNotCompletedOrdersHandler as hdl_orders


async def test_getAllCouriers(exec_db_tests):
    if not exec_db_tests:
        pytest.skip("DB not connected")
    couriers = await hdl_allcouriers.GetAllCouriersHandler.Handle()
    for courier in couriers:
        assert isinstance(courier, hdl_allcouriers.Courier)
    assert True


async def test_getNotCompletedOrders(exec_db_tests):
    if not exec_db_tests:
        pytest.skip("DB not connected")
    orders = await hdl_orders.GetNotCompletedOrdersHandler.Handle()
    for order in orders:
        assert isinstance(order, hdl_orders.Order)
    assert True
