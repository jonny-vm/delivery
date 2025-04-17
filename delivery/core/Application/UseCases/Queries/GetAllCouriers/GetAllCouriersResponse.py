from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Location:
    x: int
    y: int


@dataclass(frozen=True)
class Courier:
    id: UUID
    name: str
    location: Location
    transportId: UUID
