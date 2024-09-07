# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: usuario.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'usuario.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rusuario.proto\x12\x07usuario\"\x90\x01\n\x0eUsuarioGrpcDTO\x12\x0f\n\x07usuario\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x0e\n\x06nombre\x18\x03 \x01(\t\x12\x10\n\x08\x61pellido\x18\x04 \x01(\t\x12\x12\n\nhabilitado\x18\x05 \x01(\x08\x12\x13\n\x0b\x63\x61saCentral\x18\x06 \x01(\x08\x12\x10\n\x08idTienda\x18\x07 \x01(\x03\"H\n\x15\x41gregarUsuarioRequest\x12/\n\x0eusuarioGrpcDTO\x18\x01 \x01(\x0b\x32\x17.usuario.UsuarioGrpcDTO\"+\n\x16\x41gregarUsuarioResponse\x12\x11\n\tidUsuario\x18\x01 \x01(\x03\"8\n\x0bUsuarioList\x12)\n\x08usuarios\x18\x01 \x03(\x0b\x32\x17.usuario.UsuarioGrpcDTO\"\x1e\n\x1cTraerTodosLosUsuariosRequest\"J\n\x1dTraerTodosLosUsuariosResponse\x12)\n\x0busuarioList\x18\x01 \x01(\x0b\x32\x14.usuario.UsuarioList\"7\n%TraerTodosLosUsuariosPorNombreRequest\x12\x0e\n\x06nombre\x18\x01 \x01(\t\"S\n&TraerTodosLosUsuariosPorNombreResponse\x12)\n\x0busuarioList\x18\x01 \x01(\x0b\x32\x14.usuario.UsuarioList\"0\n\x1cTraerUsuarioPorTiendaRequest\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\"P\n\x1dTraerUsuarioPorTiendaResponse\x12/\n\x0eusuarioGrpcDTO\x18\x01 \x01(\x0b\x32\x17.usuario.UsuarioGrpcDTO2\xb8\x03\n\x07Usuario\x12S\n\x0e\x41gregarUsuario\x12\x1e.usuario.AgregarUsuarioRequest\x1a\x1f.usuario.AgregarUsuarioResponse\"\x00\x12h\n\x15TraerTodosLosUsuarios\x12%.usuario.TraerTodosLosUsuariosRequest\x1a&.usuario.TraerTodosLosUsuariosResponse\"\x00\x12\x83\x01\n\x1eTraerTodosLosUsuariosPorNombre\x12..usuario.TraerTodosLosUsuariosPorNombreRequest\x1a/.usuario.TraerTodosLosUsuariosPorNombreResponse\"\x00\x12h\n\x15TraerUsuarioPorTienda\x12%.usuario.TraerUsuarioPorTiendaRequest\x1a&.usuario.TraerUsuarioPorTiendaResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'usuario_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USUARIOGRPCDTO']._serialized_start=27
  _globals['_USUARIOGRPCDTO']._serialized_end=171
  _globals['_AGREGARUSUARIOREQUEST']._serialized_start=173
  _globals['_AGREGARUSUARIOREQUEST']._serialized_end=245
  _globals['_AGREGARUSUARIORESPONSE']._serialized_start=247
  _globals['_AGREGARUSUARIORESPONSE']._serialized_end=290
  _globals['_USUARIOLIST']._serialized_start=292
  _globals['_USUARIOLIST']._serialized_end=348
  _globals['_TRAERTODOSLOSUSUARIOSREQUEST']._serialized_start=350
  _globals['_TRAERTODOSLOSUSUARIOSREQUEST']._serialized_end=380
  _globals['_TRAERTODOSLOSUSUARIOSRESPONSE']._serialized_start=382
  _globals['_TRAERTODOSLOSUSUARIOSRESPONSE']._serialized_end=456
  _globals['_TRAERTODOSLOSUSUARIOSPORNOMBREREQUEST']._serialized_start=458
  _globals['_TRAERTODOSLOSUSUARIOSPORNOMBREREQUEST']._serialized_end=513
  _globals['_TRAERTODOSLOSUSUARIOSPORNOMBRERESPONSE']._serialized_start=515
  _globals['_TRAERTODOSLOSUSUARIOSPORNOMBRERESPONSE']._serialized_end=598
  _globals['_TRAERUSUARIOPORTIENDAREQUEST']._serialized_start=600
  _globals['_TRAERUSUARIOPORTIENDAREQUEST']._serialized_end=648
  _globals['_TRAERUSUARIOPORTIENDARESPONSE']._serialized_start=650
  _globals['_TRAERUSUARIOPORTIENDARESPONSE']._serialized_end=730
  _globals['_USUARIO']._serialized_start=733
  _globals['_USUARIO']._serialized_end=1173
# @@protoc_insertion_point(module_scope)