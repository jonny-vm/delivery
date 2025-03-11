import uuid
from dataclasses import dataclass, field
import importlib.util as imp


spec = imp.spec_from_file_location(
    "Location", "Delivery.Core\\Domain\\SharedKernel\\Location.py"
)
loc_module = imp.module_from_spec(spec)
spec.loader.exec_module(loc_module)


class TransportException(Exception):
    """Class for transport validation exceptions"""


class Location(loc_module.Location):
    """Location class from location module"""


def get_next_uuid() -> uuid.uuid4:
    """Generates new UUID"""
    return uuid.uuid4()


@dataclass
class Transport:
    id: uuid.UUID = field(default_factory=get_next_uuid, kw_only=True)
    name: str
    speed: int

    min_speed: int = field(init=False, repr=False, default=1)
    max_speed: int = field(init=False, repr=False, default=3)
    step: int = field(init=False, repr=False, default=1)

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

    def is_equiv(self, transp: "Transport") -> bool:
        return self.id == transp.id

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
