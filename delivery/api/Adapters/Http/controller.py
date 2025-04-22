from uuid import UUID

from fastapi import APIRouter

from delivery.core.Application.UseCases.Commands.AssignOrders.AssignOrdersHandler import (
    AssignOrdersHandler,
)
from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderCommand import (
    CreateOrderCommand,
)
from delivery.core.Application.UseCases.Commands.CreateOrder.CreateOrderHandler import (
    CreateOrderHandler,
)
from delivery.core.Application.UseCases.Commands.MoveCouriers.MoveCouriersHandler import (
    MoveCouriersHandler,
)
from delivery.core.Application.UseCases.Queries.GetAllCouriers.GetAllCouriersHandler import (
    Courier,
    GetAllCouriersHandler,
)
from delivery.core.Application.UseCases.Queries.GetNotCompletedOrders.GetNotCompletedOrdersHandler import (
    GetNotCompletedOrdersHandler,
    Order,
)

tags_metadata = [
    {
        "name": "API сервиса доставки",
        "description": "API сервиса доставки для обработки заказов",
    },
]

router: APIRouter = APIRouter(
    prefix="",
    tags=["Сервис доставки"],
    responses={404: {"description": "Not found"}},
)


@router.get("/assign_order", summary="Назначить заказ")
async def assign() -> dict:
    return dict(await AssignOrdersHandler.Handle())


@router.get("/create_order", summary="Создать заказ")
async def create(BasketId: UUID, Street: str) -> dict:
    return dict(await CreateOrderHandler.Handle(CreateOrderCommand(BasketId, Street)))


@router.get("/move_couriers", summary="Двинуть курьеров")
async def move_couriers() -> bool:
    return await MoveCouriersHandler.Handle()


@router.get("/get_all_couriers", summary="Получить список всех курьеров")
async def get_couriers() -> list[dict]:
    couriers_arr = await GetAllCouriersHandler.Handle()
    return [
        (courier.__dict__ if isinstance(courier, Courier) else {})
        for courier in couriers_arr
        if couriers_arr
    ]


@router.get(
    "/get_not_completed_orders", summary="Получить список всех незавершенных заказов"
)
async def get_orders() -> list[dict]:
    orders_arr = await GetNotCompletedOrdersHandler.Handle()
    return [
        (order.__dict__ if isinstance(order, Order) else {})
        for order in orders_arr
        if orders_arr
    ]
