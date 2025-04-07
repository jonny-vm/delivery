from delivery.core.Domain.SharedKernel.Location import Location
from pydantic import BaseModel, ConfigDict, Field

from delivery.core.Domain.SharedKernel.Entity import Entity
from uuid import UUID
from typing import Any


class TransportException(Exception):
    """Class for transport validation exceptions"""


class Transport(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(init=False, default_factory=lambda: Entity.get_next_uuid())
    name: str
    speed: int

    min_speed: int = Field(init=False, repr=False, default=1)
    max_speed: int = Field(init=False, repr=False, default=3)
    step: int = Field(init=False, repr=False, default=1)

    def __eq__(self, other_obj: Any) -> bool:
        if isinstance(other_obj, type(self)):
            return self.id == other_obj.id
        return False

    def __setattr__(self, name, value):
        if name == "name":
            if not value:
                raise TransportException(f"value of {name} can't be empty")
        elif name == "speed":
            if value < self.min_speed or value > self.max_speed:
                raise TransportException(
                    f"Transport {name} must be greater or equal than {self.min_speed} and less or equal than {self.max_speed}"
                )
        self.__dict__[name] = value

    def move(self) -> int:
        return self.step * self.speed

    def get_next_location(
        self, current_location: Location, aim_location: Location
    ) -> Location:
        def get_new_coordinate(
            cur_coordinate: int, aim_coordinate: int, movement: int
        ) -> int:
            if cur_coordinate >= aim_coordinate:
                return max(cur_coordinate - movement, aim_coordinate)
            else:
                return min(cur_coordinate + movement, aim_coordinate)

        current_move = self.move()
        current_x = get_new_coordinate(current_location.x, aim_location.x, current_move)

        current_move = max(current_move - abs(current_location.x - aim_location.x), 0)
        current_y = get_new_coordinate(current_location.y, aim_location.y, current_move)

        return Location(current_x, current_y)
