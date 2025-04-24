from abc import abstractmethod

from delivery.core.Domain.SharedKernel.Location import Location


class InterfaceGeoService:
    @abstractmethod
    async def get_location(self, street: str) -> Location:
        pass
