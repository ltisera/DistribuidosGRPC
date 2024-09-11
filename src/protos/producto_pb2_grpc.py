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
        self.TraerTodosLosProductosPorNombre = channel.unary_unary(
                '/producto.Producto/TraerTodosLosProductosPorNombre',
                request_serializer=producto__pb2.TraerTodosLosProductosPorNombreRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerTodosLosProductosPorNombreResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosProductosPorTalle = channel.unary_unary(
                '/producto.Producto/TraerTodosLosProductosPorTalle',
                request_serializer=producto__pb2.TraerTodosLosProductosPorTalleRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerTodosLosProductosPorTalleResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosProductosPorColor = channel.unary_unary(
                '/producto.Producto/TraerTodosLosProductosPorColor',
                request_serializer=producto__pb2.TraerTodosLosProductosPorColorRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerTodosLosProductosPorColorResponse.FromString,
                _registered_method=True)
        self.TraerProductoPorCodigo = channel.unary_unary(
                '/producto.Producto/TraerProductoPorCodigo',
                request_serializer=producto__pb2.TraerProductoPorCodigoRequest.SerializeToString,
                response_deserializer=producto__pb2.TraerProductoPorCodigoResponse.FromString,
                _registered_method=True)


class ProductoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AgregarProducto(self, request, context):
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

    def TraerTodosLosProductosPorNombre(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosProductosPorTalle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosProductosPorColor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerProductoPorCodigo(self, request, context):
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
            'TraerTodosLosProductosPorNombre': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosProductosPorNombre,
                    request_deserializer=producto__pb2.TraerTodosLosProductosPorNombreRequest.FromString,
                    response_serializer=producto__pb2.TraerTodosLosProductosPorNombreResponse.SerializeToString,
            ),
            'TraerTodosLosProductosPorTalle': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosProductosPorTalle,
                    request_deserializer=producto__pb2.TraerTodosLosProductosPorTalleRequest.FromString,
                    response_serializer=producto__pb2.TraerTodosLosProductosPorTalleResponse.SerializeToString,
            ),
            'TraerTodosLosProductosPorColor': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosProductosPorColor,
                    request_deserializer=producto__pb2.TraerTodosLosProductosPorColorRequest.FromString,
                    response_serializer=producto__pb2.TraerTodosLosProductosPorColorResponse.SerializeToString,
            ),
            'TraerProductoPorCodigo': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerProductoPorCodigo,
                    request_deserializer=producto__pb2.TraerProductoPorCodigoRequest.FromString,
                    response_serializer=producto__pb2.TraerProductoPorCodigoResponse.SerializeToString,
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
    def TraerTodosLosProductosPorNombre(request,
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
            '/producto.Producto/TraerTodosLosProductosPorNombre',
            producto__pb2.TraerTodosLosProductosPorNombreRequest.SerializeToString,
            producto__pb2.TraerTodosLosProductosPorNombreResponse.FromString,
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
    def TraerTodosLosProductosPorTalle(request,
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
            '/producto.Producto/TraerTodosLosProductosPorTalle',
            producto__pb2.TraerTodosLosProductosPorTalleRequest.SerializeToString,
            producto__pb2.TraerTodosLosProductosPorTalleResponse.FromString,
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
    def TraerTodosLosProductosPorColor(request,
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
            '/producto.Producto/TraerTodosLosProductosPorColor',
            producto__pb2.TraerTodosLosProductosPorColorRequest.SerializeToString,
            producto__pb2.TraerTodosLosProductosPorColorResponse.FromString,
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
    def TraerProductoPorCodigo(request,
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
            '/producto.Producto/TraerProductoPorCodigo',
            producto__pb2.TraerProductoPorCodigoRequest.SerializeToString,
            producto__pb2.TraerProductoPorCodigoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
