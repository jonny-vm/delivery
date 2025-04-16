from abc import abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from delivery.core.Domain.Model.CourierAggregate.Courier import Courier


class InterfaceCourierRepository:
    @abstractmethod
    async def add(self, order: Courier) -> Optional[Courier]:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Courier]:
        pass

    @abstractmethod
    async def update(self, courier: Courier) -> Optional[Courier]:
        pass

    @abstractmethod
    async def get_all_free(self) -> Optional[Sequence[Courier]]:
        pass
