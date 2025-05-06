from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderStatus:
    Created: str = field(init=False, repr=False, default="Created")
    Assigned: str = field(init=False, repr=False, default="Assigned")
    Completed: str = field(init=False, repr=False, default="Completed")
