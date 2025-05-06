from delivery.core.Application.DomainEventHandlers.OrderCompletedDomainEventHandler import (
    OrderCompletedDomainEventHandler,
)
from delivery.core.Domain.Model.CourierAggregate.Courier import CourierException
from delivery.core.Domain.Model.OrderAggregate.Order import OrderException
from delivery.infrastructure.Adapters.Postgres.Repositories.CourierRepository import (
    CourierRepository,
)
from delivery.infrastructure.Adapters.Postgres.Repositories.OrderRepository import (
    OrderRepository,
    OrderStatus,
)


class MoveCouriersHandler:
    @classmethod
    async def Handle(cls) -> bool:
        rep_ord = OrderRepository()
        rep_ord.session.begin()
        assigned_orders = await rep_ord.get_all_assigned()
        orders = list(assigned_orders) if assigned_orders else []
        for order in orders:
            if not order.courierid:
                raise OrderException("Order is not assigned to courier")
            rep_cour = CourierRepository(rep_ord.session)
            courier = await rep_cour.get(order.courierid)
            if not courier:
                raise CourierException("None available courier")
            courier.Move(order.location)
            if courier.location == order.location:
                order.CompleteOrder()
                courier.setFree()
            await rep_cour.update(courier)
            await rep_ord.update(order.id, order)
            await rep_ord.session.commit()

            if order.status == OrderStatus.Completed:
                await OrderCompletedDomainEventHandler.handle(order)
        return True
