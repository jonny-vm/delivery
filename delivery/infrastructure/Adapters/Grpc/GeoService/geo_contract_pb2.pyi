from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGeolocationRequest(_message.Message):
    __slots__ = ("Street",)
    STREET_FIELD_NUMBER: _ClassVar[int]
    Street: str
    def __init__(self, Street: _Optional[str] = ...) -> None: ...

class GetGeolocationReply(_message.Message):
    __slots__ = ("Location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    Location: Location
    def __init__(self, Location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class ErrorResponse(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
