from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class BasketConfirmedIntegrationEvent(_message.Message):
    __slots__ = ("basketId", "address", "items", "deliveryPeriod")
    BASKETID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DELIVERYPERIOD_FIELD_NUMBER: _ClassVar[int]
    basketId: str
    address: Address
    items: _containers.RepeatedCompositeFieldContainer[Item]
    deliveryPeriod: DeliveryPeriod
    def __init__(
        self,
        basketId: _Optional[str] = ...,
        address: _Optional[_Union[Address, _Mapping]] = ...,
        items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...,
        deliveryPeriod: _Optional[_Union[DeliveryPeriod, _Mapping]] = ...,
    ) -> None: ...

class Address(_message.Message):
    __slots__ = ("country", "city", "street", "house", "apartment")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    HOUSE_FIELD_NUMBER: _ClassVar[int]
    APARTMENT_FIELD_NUMBER: _ClassVar[int]
    country: str
    city: str
    street: str
    house: str
    apartment: str
    def __init__(
        self,
        country: _Optional[str] = ...,
        city: _Optional[str] = ...,
        street: _Optional[str] = ...,
        house: _Optional[str] = ...,
        apartment: _Optional[str] = ...,
    ) -> None: ...

class Item(_message.Message):
    __slots__ = ("id", "goodId", "title", "price", "quantity")
    ID_FIELD_NUMBER: _ClassVar[int]
    GOODID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    goodId: str
    title: str
    price: float
    quantity: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        goodId: _Optional[str] = ...,
        title: _Optional[str] = ...,
        price: _Optional[float] = ...,
        quantity: _Optional[int] = ...,
    ) -> None: ...

class DeliveryPeriod(_message.Message):
    __slots__ = ("to",)
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    to: int
    def __init__(self, to: _Optional[int] = ..., **kwargs) -> None: ...
