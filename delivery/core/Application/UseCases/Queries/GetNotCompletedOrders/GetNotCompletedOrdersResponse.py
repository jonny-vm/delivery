from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Location:
    x: int
    y: int


@dataclass(frozen=True)
class Order:
    id: UUID
    location: Location
