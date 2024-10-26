import grpc
from protos import ordenCompra_pb2
from protos import ordenCompra_pb2_grpc
from DAO.ordenCompraDAO import OrdenCompraDAO

class OrdenCompraServicer(ordenCompra_pb2_grpc.OrdenCompraServicer):
    def AgregarOrden(self, request, context):
        try:
            idStock = request.ordenCompraGrpcDTO.idStock
            cantidad = request.ordenCompraGrpcDTO.cantidad

            odao = OrdenCompraDAO()
            idOrdenDeCompra = odao.agregarOrdenCompra(idStock, cantidad)

            return ordenCompra_pb2.AgregarOrdenCompraResponse(idOrdenDeCompra = idOrdenDeCompra)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ordenCompra_pb2.AgregarOrdenResponse()

    def ModificarOrden(self, request, context):
        try:
            idOrdenDeCompra = request.ordenCompraGrpcDTO.idOrdenDeCompra
            odao = OrdenCompraDAO()
            resultado = odao.modificarOrdenCompra(idOrdenDeCompra)
            response = ordenCompra_pb2.ModificarOrdenCompraResponse(idOrdenDeCompra=resultado)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ordenCompra_pb2.ModificarOrdenCompraResponse()
        
    def EliminarOrden(self, request, context):
        try:
            idOrdenDeCompra = request.idOrdenDeCompra
            odao = OrdenCompraDAO()
            idOrdenDeCompra = odao.eliminarOrdenDeCompra(idOrdenDeCompra)
            response = ordenCompra_pb2.EliminarOrdenCompraResponse(idOrdenDeCompra=idOrdenDeCompra)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ordenCompra_pb2.EliminarOrdenCompraResponse()

    def TraerTodasLasOrdenes(self, request, context):
        try:
            odao = OrdenCompraDAO()
            ordenes = odao.traerTodasLasOrdenes(request.idTienda)
            orden_list = ordenCompra_pb2.OrdenCompraList()
            
            for orden in ordenes:
                orden_dto = ordenCompra_pb2.OrdenCompraGrpcDTO(
                    idOrdenDeCompra=orden[0],
                    idStock=orden[1],
                    cantidad=orden[2],
                    estado=orden[3],
                    observaciones=orden[4],
                    fechaSolicitud=orden[5],
                    fechaRecepcion=orden[6],
                    ordenDeDespacho=orden[7]
                )
                orden_list.ordenes.append(orden_dto)
            response = ordenCompra_pb2.TraerTodasLasOrdenesResponse(ordenList=orden_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ordenCompra_pb2.TraerTodasLasOrdenesResponse()
