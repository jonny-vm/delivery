import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    id: uuid.UUID = field(
        default_factory=lambda: globals()["Entity"].get_next_uuid(),
        kw_only=True,
    )

    @classmethod
    def get_next_uuid(cls) -> uuid.UUID:
        """Generates new UUID"""
        return uuid.uuid4()

    def __eq__(self, other_obj: Any) -> bool:
        if isinstance(other_obj, type(self)):
            return self.id == other_obj.id
        return False


class Aggregate(Entity):
    """
    An entry point of aggregate.
    """

    pass
