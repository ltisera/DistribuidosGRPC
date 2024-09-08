# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import usuario_pb2 as usuario__pb2

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
        + f' but the generated code in usuario_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class UsuarioStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.IniciarSesion = channel.unary_unary(
                '/usuario.Usuario/IniciarSesion',
                request_serializer=usuario__pb2.IniciarSesionRequest.SerializeToString,
                response_deserializer=usuario__pb2.IniciarSesionResponse.FromString,
                _registered_method=True)
        self.AgregarUsuario = channel.unary_unary(
                '/usuario.Usuario/AgregarUsuario',
                request_serializer=usuario__pb2.AgregarUsuarioRequest.SerializeToString,
                response_deserializer=usuario__pb2.AgregarUsuarioResponse.FromString,
                _registered_method=True)
        self.ObtenerUsuario = channel.unary_unary(
                '/usuario.Usuario/ObtenerUsuario',
                request_serializer=usuario__pb2.ObtenerUsuarioRequest.SerializeToString,
                response_deserializer=usuario__pb2.ObtenerUsuarioResponse.FromString,
                _registered_method=True)
        self.ModificarUsuario = channel.unary_unary(
                '/usuario.Usuario/ModificarUsuario',
                request_serializer=usuario__pb2.ModificarUsuarioRequest.SerializeToString,
                response_deserializer=usuario__pb2.ModificarUsuarioResponse.FromString,
                _registered_method=True)
        self.EliminarUsuario = channel.unary_unary(
                '/usuario.Usuario/EliminarUsuario',
                request_serializer=usuario__pb2.EliminarUsuarioRequest.SerializeToString,
                response_deserializer=usuario__pb2.EliminarUsuarioResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosUsuarios = channel.unary_unary(
                '/usuario.Usuario/TraerTodosLosUsuarios',
                request_serializer=usuario__pb2.TraerTodosLosUsuariosRequest.SerializeToString,
                response_deserializer=usuario__pb2.TraerTodosLosUsuariosResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosUsuariosFiltrados = channel.unary_unary(
                '/usuario.Usuario/TraerTodosLosUsuariosFiltrados',
                request_serializer=usuario__pb2.TraerTodosLosUsuariosFiltradosRequest.SerializeToString,
                response_deserializer=usuario__pb2.TraerTodosLosUsuariosFiltradosResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosUsuariosPorNombre = channel.unary_unary(
                '/usuario.Usuario/TraerTodosLosUsuariosPorNombre',
                request_serializer=usuario__pb2.TraerTodosLosUsuariosPorNombreRequest.SerializeToString,
                response_deserializer=usuario__pb2.TraerTodosLosUsuariosPorNombreResponse.FromString,
                _registered_method=True)
        self.TraerTodosLosUsuariosPorTienda = channel.unary_unary(
                '/usuario.Usuario/TraerTodosLosUsuariosPorTienda',
                request_serializer=usuario__pb2.TraerTodosLosUsuariosPorTiendaRequest.SerializeToString,
                response_deserializer=usuario__pb2.TraerTodosLosUsuariosPorTiendaResponse.FromString,
                _registered_method=True)


class UsuarioServicer(object):
    """Missing associated documentation comment in .proto file."""

    def IniciarSesion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AgregarUsuario(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ObtenerUsuario(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModificarUsuario(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EliminarUsuario(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosUsuarios(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosUsuariosFiltrados(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosUsuariosPorNombre(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TraerTodosLosUsuariosPorTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UsuarioServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'IniciarSesion': grpc.unary_unary_rpc_method_handler(
                    servicer.IniciarSesion,
                    request_deserializer=usuario__pb2.IniciarSesionRequest.FromString,
                    response_serializer=usuario__pb2.IniciarSesionResponse.SerializeToString,
            ),
            'AgregarUsuario': grpc.unary_unary_rpc_method_handler(
                    servicer.AgregarUsuario,
                    request_deserializer=usuario__pb2.AgregarUsuarioRequest.FromString,
                    response_serializer=usuario__pb2.AgregarUsuarioResponse.SerializeToString,
            ),
            'ObtenerUsuario': grpc.unary_unary_rpc_method_handler(
                    servicer.ObtenerUsuario,
                    request_deserializer=usuario__pb2.ObtenerUsuarioRequest.FromString,
                    response_serializer=usuario__pb2.ObtenerUsuarioResponse.SerializeToString,
            ),
            'ModificarUsuario': grpc.unary_unary_rpc_method_handler(
                    servicer.ModificarUsuario,
                    request_deserializer=usuario__pb2.ModificarUsuarioRequest.FromString,
                    response_serializer=usuario__pb2.ModificarUsuarioResponse.SerializeToString,
            ),
            'EliminarUsuario': grpc.unary_unary_rpc_method_handler(
                    servicer.EliminarUsuario,
                    request_deserializer=usuario__pb2.EliminarUsuarioRequest.FromString,
                    response_serializer=usuario__pb2.EliminarUsuarioResponse.SerializeToString,
            ),
            'TraerTodosLosUsuarios': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosUsuarios,
                    request_deserializer=usuario__pb2.TraerTodosLosUsuariosRequest.FromString,
                    response_serializer=usuario__pb2.TraerTodosLosUsuariosResponse.SerializeToString,
            ),
            'TraerTodosLosUsuariosFiltrados': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosUsuariosFiltrados,
                    request_deserializer=usuario__pb2.TraerTodosLosUsuariosFiltradosRequest.FromString,
                    response_serializer=usuario__pb2.TraerTodosLosUsuariosFiltradosResponse.SerializeToString,
            ),
            'TraerTodosLosUsuariosPorNombre': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosUsuariosPorNombre,
                    request_deserializer=usuario__pb2.TraerTodosLosUsuariosPorNombreRequest.FromString,
                    response_serializer=usuario__pb2.TraerTodosLosUsuariosPorNombreResponse.SerializeToString,
            ),
            'TraerTodosLosUsuariosPorTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.TraerTodosLosUsuariosPorTienda,
                    request_deserializer=usuario__pb2.TraerTodosLosUsuariosPorTiendaRequest.FromString,
                    response_serializer=usuario__pb2.TraerTodosLosUsuariosPorTiendaResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'usuario.Usuario', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('usuario.Usuario', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Usuario(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def IniciarSesion(request,
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
            '/usuario.Usuario/IniciarSesion',
            usuario__pb2.IniciarSesionRequest.SerializeToString,
            usuario__pb2.IniciarSesionResponse.FromString,
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
    def AgregarUsuario(request,
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
            '/usuario.Usuario/AgregarUsuario',
            usuario__pb2.AgregarUsuarioRequest.SerializeToString,
            usuario__pb2.AgregarUsuarioResponse.FromString,
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
    def ObtenerUsuario(request,
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
            '/usuario.Usuario/ObtenerUsuario',
            usuario__pb2.ObtenerUsuarioRequest.SerializeToString,
            usuario__pb2.ObtenerUsuarioResponse.FromString,
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
    def ModificarUsuario(request,
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
            '/usuario.Usuario/ModificarUsuario',
            usuario__pb2.ModificarUsuarioRequest.SerializeToString,
            usuario__pb2.ModificarUsuarioResponse.FromString,
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
    def EliminarUsuario(request,
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
            '/usuario.Usuario/EliminarUsuario',
            usuario__pb2.EliminarUsuarioRequest.SerializeToString,
            usuario__pb2.EliminarUsuarioResponse.FromString,
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
    def TraerTodosLosUsuarios(request,
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
            '/usuario.Usuario/TraerTodosLosUsuarios',
            usuario__pb2.TraerTodosLosUsuariosRequest.SerializeToString,
            usuario__pb2.TraerTodosLosUsuariosResponse.FromString,
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
    def TraerTodosLosUsuariosFiltrados(request,
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
            '/usuario.Usuario/TraerTodosLosUsuariosFiltrados',
            usuario__pb2.TraerTodosLosUsuariosFiltradosRequest.SerializeToString,
            usuario__pb2.TraerTodosLosUsuariosFiltradosResponse.FromString,
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
    def TraerTodosLosUsuariosPorNombre(request,
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
            '/usuario.Usuario/TraerTodosLosUsuariosPorNombre',
            usuario__pb2.TraerTodosLosUsuariosPorNombreRequest.SerializeToString,
            usuario__pb2.TraerTodosLosUsuariosPorNombreResponse.FromString,
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
    def TraerTodosLosUsuariosPorTienda(request,
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
            '/usuario.Usuario/TraerTodosLosUsuariosPorTienda',
            usuario__pb2.TraerTodosLosUsuariosPorTiendaRequest.SerializeToString,
            usuario__pb2.TraerTodosLosUsuariosPorTiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
