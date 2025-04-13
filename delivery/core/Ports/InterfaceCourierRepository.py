from abc import abstractmethod
from uuid import UUID
from delivery.core.Ports.repositories import SQLAbstractRepository
from delivery.core.Domain.Model.CourierAggregate.Courier import Courier
from typing import Optional, Sequence


class InterfaceCourierRepository(SQLAbstractRepository):
    @abstractmethod
    async def add(self, order: Courier) -> Optional[Courier]:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Courier]:
        pass

    @abstractmethod
    async def update(self, id: UUID, courier: Courier) -> Optional[Courier]:
        pass

    @abstractmethod
    async def get_all_free(self) -> Optional[Sequence[Courier]]:
        pass
