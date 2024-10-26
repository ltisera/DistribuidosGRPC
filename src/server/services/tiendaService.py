import grpc
from protos import tienda_pb2
from protos import tienda_pb2_grpc
from DAO.tiendaDAO import TiendaDAO

class TiendaServicer(tienda_pb2_grpc.TiendaServicer):
    def AgregarTienda(self, request, context):
        from server import actualizar_subscripciones
        try:
            idTienda = request.tiendaGrpcDTO.idTienda
            direccion = request.tiendaGrpcDTO.direccion
            ciudad = request.tiendaGrpcDTO.ciudad
            provincia = request.tiendaGrpcDTO.provincia
            habilitado = request.tiendaGrpcDTO.habilitado

            tdao = TiendaDAO()
            idTienda = tdao.agregarTienda(idTienda, direccion, ciudad, provincia, habilitado)
            actualizar_subscripciones()
            return tienda_pb2.AgregarTiendaResponse(idTienda = idTienda)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.AgregarTiendaResponse()
        
    def ObtenerTienda(self, request, context):
        try:
            tdao = TiendaDAO()
            idTienda = request.idTienda
            tienda = tdao.obtenerTienda(idTienda)


            if tienda is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'Tienda con id {idTienda} no encontrado.')
                return tienda_pb2.ObtenerTiendaResponse()

            tienda_dto = tienda_pb2.TiendaGrpcDTO(
                    idTienda=tienda[0],
                    direccion=tienda[1],
                    ciudad=tienda[2],
                    provincia=tienda[3],
                    habilitado=tienda[4]
                ) 

            response = tienda_pb2.ObtenerTiendaResponse(tiendaGrpcDTO=tienda_dto)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.ObtenerTiendaResponse()

    def ModificarTienda(self, request, context):
        try:
            idTienda = request.tiendaGrpcDTO.idTienda
            direccion = request.tiendaGrpcDTO.direccion
            ciudad = request.tiendaGrpcDTO.ciudad
            provincia = request.tiendaGrpcDTO.provincia
            habilitado = request.tiendaGrpcDTO.habilitado

            tdao = TiendaDAO()
            idTienda = tdao.modificarTienda(idTienda, direccion, ciudad, provincia, habilitado)
            response = tienda_pb2.ModificarTiendaResponse(idTienda=idTienda)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.ModificarTiendaResponse()

    def EliminarTienda(self, request, context):
        try:
            idTienda = request.idTienda

            tdao = TiendaDAO()
            idTienda = tdao.eliminarTienda(idTienda)
            response = tienda_pb2.EliminarTiendaResponse(idTienda=idTienda)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.EliminarTiendaResponse()

    def TraerTodasLasTiendas(self, request, context):
        try:
            tdao = TiendaDAO()
            tiendas = tdao.traerTodasLasTiendas()
            tienda_list = tienda_pb2.TiendaList()
            for tienda in tiendas:
                tienda_dto = tienda_pb2.TiendaGrpcDTO(
                    idTienda=tienda[0],
                    direccion=tienda[1],
                    ciudad=tienda[2],
                    provincia=tienda[3],
                    habilitado=tienda[4],
                )
                tienda_list.tiendas.append(tienda_dto)
            response = tienda_pb2.TraerTodasLasTiendasResponse(tiendaList=tienda_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.TraerTodasLasTiendasResponse()
        
    def TraerTodasLasTiendasFiltradas(self, request, context):
        try:
            idTienda = request.idTienda
            estado = request.estado
            tdao = TiendaDAO()
            tiendas = tdao.traerTodasLasTiendasFiltradas(idTienda, estado)
            tienda_list = tienda_pb2.TiendaList()
            if tiendas:
                for tienda in tiendas:
                    tienda_dto = tienda_pb2.TiendaGrpcDTO(
                        idTienda=tienda[0],
                        direccion=tienda[1],
                        ciudad=tienda[2],
                        provincia=tienda[3],
                        habilitado=tienda[4],
                    )
                    tienda_list.tiendas.append(tienda_dto)

            response = tienda_pb2.TraerTodasLasTiendasFiltradasResponse(tiendaList=tienda_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return tienda_pb2.TraerTodasLasTiendasFiltradasResponse()
