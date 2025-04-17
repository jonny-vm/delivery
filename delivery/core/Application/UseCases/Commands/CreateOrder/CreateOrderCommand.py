from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrderCommand:
    BasketId: UUID
    Street: str
