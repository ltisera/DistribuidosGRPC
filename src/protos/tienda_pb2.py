# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tienda.proto
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
    'tienda.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ctienda.proto\x12\x06tienda\"k\n\rTiendaGrpcDTO\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\x12\x11\n\tdireccion\x18\x02 \x01(\t\x12\x0e\n\x06\x63iudad\x18\x03 \x01(\t\x12\x11\n\tprovincia\x18\x04 \x01(\t\x12\x12\n\nhabilitado\x18\x05 \x01(\x08\"D\n\x14\x41gregarTiendaRequest\x12,\n\rtiendaGrpcDTO\x18\x01 \x01(\x0b\x32\x15.tienda.TiendaGrpcDTO\")\n\x15\x41gregarTiendaResponse\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\"4\n\nTiendaList\x12&\n\x07tiendas\x18\x01 \x03(\x0b\x32\x15.tienda.TiendaGrpcDTO\"(\n\x14ObtenerTiendaRequest\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\"L\n\x15ObtenerTiendaResponse\x12\x33\n\x14tiendaObtenerGrpcDTO\x18\x01 \x01(\x0b\x32\x15.tienda.TiendaGrpcDTO\"M\n\x16ModificarTiendaRequest\x12\x33\n\x14tiendaObtenerGrpcDTO\x18\x01 \x01(\x0b\x32\x15.tienda.TiendaGrpcDTO\"+\n\x17ModificarTiendaResponse\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\")\n\x15\x45liminarTiendaRequest\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\"*\n\x16\x45liminarTiendaResponse\x12\x10\n\x08idTienda\x18\x01 \x01(\x03\"\x1d\n\x1bTraerTodasLasTiendasRequest\"F\n\x1cTraerTodasLasTiendasResponse\x12&\n\ntiendaList\x18\x01 \x01(\x0b\x32\x12.tienda.TiendaList\"F\n$TraerTodasLasTiendasFiltradasRequest\x12\x0e\n\x06\x65stado\x18\x01 \x01(\x08\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\x03\"O\n%TraerTodasLasTiendasFiltradasResponse\x12&\n\ntiendaList\x18\x01 \x01(\x0b\x32\x12.tienda.TiendaList2\xb6\x04\n\x06Tienda\x12N\n\rAgregarTienda\x12\x1c.tienda.AgregarTiendaRequest\x1a\x1d.tienda.AgregarTiendaResponse\"\x00\x12N\n\rObtenerTienda\x12\x1c.tienda.ObtenerTiendaRequest\x1a\x1d.tienda.ObtenerTiendaResponse\"\x00\x12T\n\x0fModificarTienda\x12\x1e.tienda.ModificarTiendaRequest\x1a\x1f.tienda.ModificarTiendaResponse\"\x00\x12Q\n\x0e\x45liminarTienda\x12\x1d.tienda.EliminarTiendaRequest\x1a\x1e.tienda.EliminarTiendaResponse\"\x00\x12\x63\n\x14TraerTodasLasTiendas\x12#.tienda.TraerTodasLasTiendasRequest\x1a$.tienda.TraerTodasLasTiendasResponse\"\x00\x12~\n\x1dTraerTodasLasTiendasFiltradas\x12,.tienda.TraerTodasLasTiendasFiltradasRequest\x1a-.tienda.TraerTodasLasTiendasFiltradasResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tienda_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TIENDAGRPCDTO']._serialized_start=24
  _globals['_TIENDAGRPCDTO']._serialized_end=131
  _globals['_AGREGARTIENDAREQUEST']._serialized_start=133
  _globals['_AGREGARTIENDAREQUEST']._serialized_end=201
  _globals['_AGREGARTIENDARESPONSE']._serialized_start=203
  _globals['_AGREGARTIENDARESPONSE']._serialized_end=244
  _globals['_TIENDALIST']._serialized_start=246
  _globals['_TIENDALIST']._serialized_end=298
  _globals['_OBTENERTIENDAREQUEST']._serialized_start=300
  _globals['_OBTENERTIENDAREQUEST']._serialized_end=340
  _globals['_OBTENERTIENDARESPONSE']._serialized_start=342
  _globals['_OBTENERTIENDARESPONSE']._serialized_end=418
  _globals['_MODIFICARTIENDAREQUEST']._serialized_start=420
  _globals['_MODIFICARTIENDAREQUEST']._serialized_end=497
  _globals['_MODIFICARTIENDARESPONSE']._serialized_start=499
  _globals['_MODIFICARTIENDARESPONSE']._serialized_end=542
  _globals['_ELIMINARTIENDAREQUEST']._serialized_start=544
  _globals['_ELIMINARTIENDAREQUEST']._serialized_end=585
  _globals['_ELIMINARTIENDARESPONSE']._serialized_start=587
  _globals['_ELIMINARTIENDARESPONSE']._serialized_end=629
  _globals['_TRAERTODASLASTIENDASREQUEST']._serialized_start=631
  _globals['_TRAERTODASLASTIENDASREQUEST']._serialized_end=660
  _globals['_TRAERTODASLASTIENDASRESPONSE']._serialized_start=662
  _globals['_TRAERTODASLASTIENDASRESPONSE']._serialized_end=732
  _globals['_TRAERTODASLASTIENDASFILTRADASREQUEST']._serialized_start=734
  _globals['_TRAERTODASLASTIENDASFILTRADASREQUEST']._serialized_end=804
  _globals['_TRAERTODASLASTIENDASFILTRADASRESPONSE']._serialized_start=806
  _globals['_TRAERTODASLASTIENDASFILTRADASRESPONSE']._serialized_end=885
  _globals['_TIENDA']._serialized_start=888
  _globals['_TIENDA']._serialized_end=1454
# @@protoc_insertion_point(module_scope)
