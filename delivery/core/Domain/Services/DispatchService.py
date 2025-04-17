from delivery.core.Domain.Model.CourierAggregate.Courier import Courier, CourierStatus
from delivery.core.Domain.Model.OrderAggregate.Order import Order


class DispatchException(Exception):
    """Class for dispatch validation exceptions"""


def Dispatch(order: Order, couriers: list[Courier]) -> Courier:
    courier = None
    for courier_candidate in filter(lambda c: c.status == CourierStatus.Free, couriers):
        if not courier:
            courier = courier_candidate
            courier_moves = courier.getCountMoves(order.location)
        else:
            candidate_moves = courier_candidate.getCountMoves(order.location)
            if courier_moves > candidate_moves:
                courier = courier_candidate
                courier_moves = candidate_moves

    if not courier:
        raise DispatchException("There is not a single free courier")

    courier.setBusy()
    return courier
