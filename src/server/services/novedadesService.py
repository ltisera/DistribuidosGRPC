import grpc
from protos import novedades_pb2
from protos import novedades_pb2_grpc
from DAO.novedadesDAO import NovedadesDAO

class NovedadesServicer(novedades_pb2_grpc.NovedadesServicer):
    def EliminarNovedad(self, request, context):
        try:
            codigo = request.codigo
            ndao = NovedadesDAO()
            codigo = ndao.eliminarNovedad(codigo)
            response = novedades_pb2.EliminarNovedadResponse(codigo=codigo)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return novedades_pb2.EliminarNovedadResponse()

    def TraerTodasLasNovedades(self, request, context):
        try:
            ndao = NovedadesDAO()
            novedades = ndao.traerTodasLasNovedades()
            novedad_list = novedades_pb2.NovedadList()
            
            for novedad in novedades:
                novedad_dto = novedades_pb2.NovedadGrpcDTO(
                    codigo=novedad[0],
                    nombre=novedad[1],
                    talle=novedad[2],
                    color=novedad[3],
                    url=novedad[4],
                )
                novedad_list.novedades.append(novedad_dto)
            response = novedades_pb2.TraerTodasLasNovedadesResponse(novedadList=novedad_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return novedades_pb2.TraerTodasLasNovedadesResponse()