# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import tienda_pb2 as tienda__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in tienda_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TiendaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AgregarTienda = channel.unary_unary(
                '/testgrpc.Tienda/AgregarTienda',
                request_serializer=tienda__pb2.AgregarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.AgregarTiendaResponse.FromString,
                _registered_method=True)
        self.ObtenerTienda = channel.unary_unary(
                '/testgrpc.Tienda/ObtenerTienda',
                request_serializer=tienda__pb2.ObtenerTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.ObtenerTiendaResponse.FromString,
                _registered_method=True)
        self.ModificarTienda = channel.unary_unary(
                '/testgrpc.Tienda/ModificarTienda',
                request_serializer=tienda__pb2.ModificarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.ModificarTiendaResponse.FromString,
                _registered_method=True)
        self.EliminarTienda = channel.unary_unary(
                '/testgrpc.Tienda/EliminarTienda',
                request_serializer=tienda__pb2.EliminarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.EliminarTiendaResponse.FromString,
                _registered_method=True)
        self.TraerTodasLasTiendas = channel.unary_unary(
                '/testgrpc.Tienda/TraerTodasLasTiendas',
                request_serializer=tienda__pb2.TraerTodasLasTiendasRequest.SerializeToString,
                response_deserializer=tienda__pb2.TraerTodasLasTiendasResponse.FromString,
                _registered_method=True)
        self.TraerTodasLasTiendasFiltradas = channel.unary_unary(
                '/testgrpc.Tienda/TraerTodasLasTiendasFiltradas',
                request_serializer=tienda__pb2.TraerTodasLasTiendasFiltradasRequest.SerializeToString,
                response_deserializer=tienda__pb2.TraerTodasLasTiendasFiltradasResponse.FromString,
                _registered_method=True)


class TiendaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AgregarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ObtenerTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModificarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EliminarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodasLasTiendas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodasLasTiendasFiltradas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TiendaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AgregarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.AgregarTienda,
                    request_deserializer=tienda__pb2.AgregarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.AgregarTiendaResponse.SerializeToString,
            ),
            'ObtenerTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.ObtenerTienda,
                    request_deserializer=tienda__pb2.ObtenerTiendaRequest.FromString,
                    response_serializer=tienda__pb2.ObtenerTiendaResponse.SerializeToString,
            ),
            'ModificarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.ModificarTienda,
                    request_deserializer=tienda__pb2.ModificarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.ModificarTiendaResponse.SerializeToString,
            ),
            'EliminarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.EliminarTienda,
                    request_deserializer=tienda__pb2.EliminarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.EliminarTiendaResponse.SerializeToString,
            ),
            'TraerTodasLasTiendas': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodasLasTiendas,
                    request_deserializer=tienda__pb2.TraerTodasLasTiendasRequest.FromString,
                    response_serializer=tienda__pb2.TraerTodasLasTiendasResponse.SerializeToString,
            ),
            'TraerTodasLasTiendasFiltradas': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodasLasTiendasFiltradas,
                    request_deserializer=tienda__pb2.TraerTodasLasTiendasFiltradasRequest.FromString,
                    response_serializer=tienda__pb2.TraerTodasLasTiendasFiltradasResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'testgrpc.Tienda', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('testgrpc.Tienda', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Tienda(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AgregarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/AgregarTienda',
            tienda__pb2.AgregarTiendaRequest.SerializeToString,
            tienda__pb2.AgregarTiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ObtenerTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/ObtenerTienda',
            tienda__pb2.ObtenerTiendaRequest.SerializeToString,
            tienda__pb2.ObtenerTiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ModificarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/ModificarTienda',
            tienda__pb2.ModificarTiendaRequest.SerializeToString,
            tienda__pb2.ModificarTiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EliminarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/EliminarTienda',
            tienda__pb2.EliminarTiendaRequest.SerializeToString,
            tienda__pb2.EliminarTiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TraerTodasLasTiendas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/TraerTodasLasTiendas',
            tienda__pb2.TraerTodasLasTiendasRequest.SerializeToString,
            tienda__pb2.TraerTodasLasTiendasResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TraerTodasLasTiendasFiltradas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/testgrpc.Tienda/TraerTodasLasTiendasFiltradas',
            tienda__pb2.TraerTodasLasTiendasFiltradasRequest.SerializeToString,
            tienda__pb2.TraerTodasLasTiendasFiltradasResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
