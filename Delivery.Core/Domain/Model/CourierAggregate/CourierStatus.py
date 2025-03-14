from dataclasses import dataclass, field


@dataclass(frozen=True)
class CourierStatus:
    Free: str = field(init=False, repr=False, default="free")
    Busy: str = field(init=False, repr=False, default="busy")
