# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import producto_pb2 as producto__pb2

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
        + f' but the generated code in producto_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ProductoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AgregarProducto = channel.unary_unary(
                '/producto.Producto/AgregarProducto',
                request_serializer=producto__pb2.AgregarProductoRequest.SerializeToString,
                response_deserializer=producto__pb2.AgregarProductoResponse.FromString,
                _registered_method=True)
        self.AgregarTalle = channel.unary_unary(
                '/producto.Producto/AgregarTalle',
                request_serializer=producto__pb2.AgregarTalleRequest.SerializeToString,
                response_deserializer=producto__pb2.AgregarTalleResponse.FromString,
                _registered_method=True)
        self.ObtenerProducto = channel.unary_unary(
                '/producto.Producto/ObtenerProducto',
                request_serializer=producto__pb2.ObtenerProductoRequest.SerializeToString,
                response_deserializer=producto__pb2.ObtenerProductoResponse.FromString,
                _registered_method=True)
        self.ModificarProducto = channel.unary_unary(
                '/producto.Producto/ModificarProducto',
                request_serializer=producto__pb2.ModificarProductoRequest.SerializeToString,
                response_deserializer=producto__pb2.ModificarProductoResponse.FromString,
                _registered_method=True)
        self.EliminarProducto = channel.unary_unary(
                '/producto.Producto/EliminarProducto',
                request_serializer=producto__pb2.EliminarProductoRequest.SerializeToString,
                response_deserializer=producto__pb2.ModificarProductoResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosProductos = channel.unary_unary(
                '/producto.Producto/TraerTodosLosProductos',
                request_serializer=producto__pb2.TraerTodosLosProductosRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerTodosLosProductosResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosProductosFiltrados = channel.unary_unary(
                '/producto.Producto/TraerTodosLosProductosFiltrados',
                request_serializer=producto__pb2.TraerTodosLosProductosFiltradosRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerTodosLosProductosFiltradosResponse.FromString,
                _registered_method=True)


class ProductoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AgregarProducto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AgregarTalle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ObtenerProducto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModificarProducto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EliminarProducto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosProductos(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosProductosFiltrados(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AgregarProducto': grpc.unary_unary_rpc_method_handler(
                    servicer.AgregarProducto,
                    request_deserializer=producto__pb2.AgregarProductoRequest.FromString,
                    response_serializer=producto__pb2.AgregarProductoResponse.SerializeToString,
            ),
            'AgregarTalle': grpc.unary_unary_rpc_method_handler(
                    servicer.AgregarTalle,
                    request_deserializer=producto__pb2.AgregarTalleRequest.FromString,
                    response_serializer=producto__pb2.AgregarTalleResponse.SerializeToString,
            ),
            'ObtenerProducto': grpc.unary_unary_rpc_method_handler(
                    servicer.ObtenerProducto,
                    request_deserializer=producto__pb2.ObtenerProductoRequest.FromString,
                    response_serializer=producto__pb2.ObtenerProductoResponse.SerializeToString,
            ),
            'ModificarProducto': grpc.unary_unary_rpc_method_handler(
                    servicer.ModificarProducto,
                    request_deserializer=producto__pb2.ModificarProductoRequest.FromString,
                    response_serializer=producto__pb2.ModificarProductoResponse.SerializeToString,
            ),
            'EliminarProducto': grpc.unary_unary_rpc_method_handler(
                    servicer.EliminarProducto,
                    request_deserializer=producto__pb2.EliminarProductoRequest.FromString,
                    response_serializer=producto__pb2.ModificarProductoResponse.SerializeToString,
            ),
            'TraerTodosLosProductos': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosProductos,
                    request_deserializer=producto__pb2.TraerTodosLosProductosRequest.FromString,
                    response_serializer=producto__pb2.TraerTodosLosProductosResponse.SerializeToString,
            ),
            'TraerTodosLosProductosFiltrados': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosProductosFiltrados,
                    request_deserializer=producto__pb2.TraerTodosLosProductosFiltradosRequest.FromString,
                    response_serializer=producto__pb2.TraerTodosLosProductosFiltradosResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'producto.Producto', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('producto.Producto', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Producto(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AgregarProducto(request,
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
            '/producto.Producto/AgregarProducto',
            producto__pb2.AgregarProductoRequest.SerializeToString,
            producto__pb2.AgregarProductoResponse.FromString,
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
    def AgregarTalle(request,
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
            '/producto.Producto/AgregarTalle',
            producto__pb2.AgregarTalleRequest.SerializeToString,
            producto__pb2.AgregarTalleResponse.FromString,
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
    def ObtenerProducto(request,
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
            '/producto.Producto/ObtenerProducto',
            producto__pb2.ObtenerProductoRequest.SerializeToString,
            producto__pb2.ObtenerProductoResponse.FromString,
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
    def ModificarProducto(request,
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
            '/producto.Producto/ModificarProducto',
            producto__pb2.ModificarProductoRequest.SerializeToString,
            producto__pb2.ModificarProductoResponse.FromString,
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
    def EliminarProducto(request,
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
            '/producto.Producto/EliminarProducto',
            producto__pb2.EliminarProductoRequest.SerializeToString,
            producto__pb2.ModificarProductoResponse.FromString,
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
    def TraerTodosLosProductos(request,
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
            '/producto.Producto/TraerTodosLosProductos',
            producto__pb2.TraerTodosLosProductosRequest.SerializeToString,
            producto__pb2.TraerTodosLosProductosResponse.FromString,
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
    def TraerTodosLosProductosFiltrados(request,
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
            '/producto.Producto/TraerTodosLosProductosFiltrados',
            producto__pb2.TraerTodosLosProductosFiltradosRequest.SerializeToString,
            producto__pb2.TraerTodosLosProductosFiltradosResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
