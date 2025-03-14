from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderStatus:
    Created: str = field(init=False, repr=False, default="created")
    Assigned: str = field(init=False, repr=False, default="assigned")
    Completed: str = field(init=False, repr=False, default="completed")
