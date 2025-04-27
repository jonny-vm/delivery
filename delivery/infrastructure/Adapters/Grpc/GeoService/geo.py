import os

import grpc

from delivery.core.Ports.InterfaceGeoSevice import InterfaceGeoService, Location
from delivery.infrastructure.Adapters.Grpc.GeoService import (
    geo_contract_pb2 as geo,
)
from delivery.infrastructure.Adapters.Grpc.GeoService import (
    geo_contract_pb2_grpc as geo_grpc,
)


class gRPCError(Exception):
    pass


class GeoService(InterfaceGeoService):
    @classmethod
    async def grpc_geo_client(cls):
        channel = grpc.aio.insecure_channel(
            f"{os.getenv('GEO_HOST')}:{os.getenv('GEO_PORT')}"
        )
        client = geo_grpc.GeoStub(channel)
        return client

    @classmethod
    async def get_location(cls, street: str) -> Location:
        try:
            client = await GeoService.grpc_geo_client()
            reply = await client.GetGeolocation(
                geo.GetGeolocationRequest(Street=street)
            )
        except grpc.RpcError as e:
            raise gRPCError(e.details())

        return Location(reply.Location.x, reply.Location.y)
