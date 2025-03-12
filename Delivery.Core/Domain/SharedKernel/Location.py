from dataclasses import dataclass, field
import random
from typing import Any


class CoordinateException(Exception):
    """Class for coordinate validation exceptions"""


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    min_x: int = field(init=False, repr=False, default=1)
    max_x: int = field(init=False, repr=False, default=10)
    min_y: int = field(init=False, repr=False, default=1)
    max_y: int = field(init=False, repr=False, default=10)

    def __post_init__(self) -> None:
        if self.x < self.min_x or self.x > self.max_x:
            raise CoordinateException(
                f"Coordinate X must be greater or equal than {self.min_x} and less or equal than {self.max_x}"
            )
        if self.y < self.min_y or self.y > self.max_y:
            raise CoordinateException(
                f"Coordinate Y must be greater or equal than {self.min_y} and less or equal than {self.max_y}"
            )

    def __eq__(self, other_obj: Any) -> bool:
        if isinstance(other_obj, type(self)):
            return self.x == other_obj.x and self.y == other_obj.y
        return False

    def get_distance(self, loc: "Location") -> int:
        return abs(loc.x - self.x) + abs(loc.y - self.y)

    @classmethod
    def get_random_coordinate(cls) -> "Location":
        return Location(
            random.randint(Location.min_x, Location.max_x),
            random.randint(Location.min_y, Location.max_y),
        )
