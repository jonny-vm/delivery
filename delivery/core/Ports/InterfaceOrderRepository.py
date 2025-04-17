from abc import abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from delivery.core.Domain.Model.OrderAggregate.Order import Order


class InterfaceOrderRepository:
    @abstractmethod
    async def add(self, order: Order) -> Optional[Order]:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def update(self, id: UUID, order: Order) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_anyone_created(self) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_all_assigned(self) -> Optional[Sequence[Order]]:
        pass
