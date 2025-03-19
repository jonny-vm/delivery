from delivery.core.Domain.Model.OrderAggregate.Order import Order
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from delivery.core.Domain.Services.DispatchService import Dispatch as DispatchMeth


def Dispatch(order: Order, couriers: list[Courier]) -> Courier:
    return DispatchMeth(order, couriers)
