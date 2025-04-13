from abc import ABC
import uuid


class Entity(ABC):
    @classmethod
    def get_next_uuid(cls) -> uuid.UUID:
        """Generates new UUID"""
        return uuid.uuid4()
