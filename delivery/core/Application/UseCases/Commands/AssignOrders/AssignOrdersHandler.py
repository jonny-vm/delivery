from delivery.core.Domain.Model.CourierAggregate.Courier import CourierException
from delivery.core.Domain.Model.OrderAggregate.Order import Order, OrderException
from delivery.core.Domain.Services.DispatchService import Dispatch
from delivery.infrastructure.Adapters.Postgres.Repositories.CourierRepository import (
    CourierRepository,
)
from delivery.infrastructure.Adapters.Postgres.Repositories.OrderRepository import (
    OrderRepository,
)


class AssignOrdersHandler:
    @classmethod
    async def Handle(cls) -> Order:
        rep_ord = OrderRepository()
        rep_ord.session.begin()
        order = await rep_ord.get_anyone_created()
        if not order:
            raise OrderException("None available order")
        rep_cour = CourierRepository(rep_ord.session)
        couriers = await rep_cour.get_all_free()
        if not couriers:
            raise CourierException("None available courier")
        courier = Dispatch(order, list(couriers))
        order.AssignOrder(courier)
        await rep_cour.update(courier)
        await rep_ord.update(order.id, order)
        await rep_ord.session.commit()
        return order
