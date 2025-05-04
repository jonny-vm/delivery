from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    _None: _ClassVar[OrderStatus]
    Created: _ClassVar[OrderStatus]
    Assigned: _ClassVar[OrderStatus]
    Completed: _ClassVar[OrderStatus]
_None: OrderStatus
Created: OrderStatus
Assigned: OrderStatus
Completed: OrderStatus

class OrderStatusChangedIntegrationEvent(_message.Message):
    __slots__ = ("orderId", "orderStatus")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    ORDERSTATUS_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    orderStatus: OrderStatus
    def __init__(self, orderId: _Optional[str] = ..., orderStatus: _Optional[_Union[OrderStatus, str]] = ...) -> None: ...
