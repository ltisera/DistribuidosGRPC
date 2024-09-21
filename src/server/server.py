import grpc
from concurrent import futures
import os, sys



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(CURRENT_DIR + '\\DAO')
sys.path.append(CURRENT_DIR + '\\settings')

PARENT_DIR = os.path.dirname(CURRENT_DIR)
PROTO_DIR = os.path.join(PARENT_DIR, 'protos')
sys.path.append(PROTO_DIR)
sys.path.append(os.path.join(CURRENT_DIR, 'dao'))

from protos import usuario_pb2
from protos import usuario_pb2_grpc
from protos import tienda_pb2
from protos import tienda_pb2_grpc
from protos import producto_pb2
from protos import producto_pb2_grpc

from DAO.tiendaDAO import TiendaDAO
from DAO.usuarioDAO import UsuarioDAO
from DAO.productoDAO import ProductoDAO
from DAO.stockDAO import StockDAO

# USUARIO
class UsuarioServicer(usuario_pb2_grpc.UsuarioServicer):
    def IniciarSesion(self, request, context):
        usuario = request.usuario
        password = request.password
        udao = UsuarioDAO()
        usuario = udao.iniciarSesion(usuario, password)
        idUsuario = -1
        casaCentral = ""
        idTienda = -1

        if usuario is not None:
            idUsuario = usuario[0]
            casaCentral = usuario[6]
            idTienda = usuario[7]

        return usuario_pb2.IniciarSesionResponse(idUsuario=idUsuario, casaCentral=casaCentral, idTienda=idTienda)

    def AgregarUsuario(self, request, context):
        #agregado = "" 
        try:
            usuario = request.usuarioGrpcDTO.usuario
            password = request.usuarioGrpcDTO.password
            nombre = request.usuarioGrpcDTO.nombre
            apellido = request.usuarioGrpcDTO.apellido
            habilitado = request.usuarioGrpcDTO.habilitado
            casaCentral = request.usuarioGrpcDTO.casaCentral
            idTienda = request.usuarioGrpcDTO.idTienda

            udao = UsuarioDAO()
            idUsuario = udao.agregarUsuario(usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
            return usuario_pb2.AgregarUsuarioResponse(idUsuario = idUsuario) # agregado = usuario_pb2.AgregarUsuarioResponse(idUsuario = idUsuario)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.AgregarUsuarioResponse() # agregado = usuario_pb2.AgregarUsuarioResponse()
        #return agregado
        

    def ObtenerUsuario(self, request, context):
        try:
            udao = UsuarioDAO()
            idUsuario = request.idUsuario
            usuario = udao.obtenerUsuario(idUsuario)


            if usuario is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'Usuario con id {idUsuario} no encontrado.')
                return usuario_pb2.ObtenerUsuarioResponse()

            usuario_dto = usuario_pb2.UsuarioGrpcDTO(
                    idUsuario=usuario[0],
                    usuario=usuario[1],
                    password=usuario[2],
                    nombre=usuario[3],
                    apellido=usuario[4],
                    habilitado=usuario[5],
                    casaCentral=usuario[6],
                    idTienda=usuario[7]
                )

            response = usuario_pb2.ObtenerUsuarioResponse(usuarioGrpcDTO=usuario_dto)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.ObtenerUsuarioResponse()

    def ModificarUsuario(self, request, context):
        try:
            idUsuario = request.usuarioGrpcDTO.idUsuario
            usuario = request.usuarioGrpcDTO.usuario
            password = request.usuarioGrpcDTO.password
            nombre = request.usuarioGrpcDTO.nombre
            apellido = request.usuarioGrpcDTO.apellido
            habilitado = request.usuarioGrpcDTO.habilitado
            casaCentral = request.usuarioGrpcDTO.casaCentral
            idTienda = request.usuarioGrpcDTO.idTienda

            udao = UsuarioDAO()
            idUsuario = udao.modificarUsuario(idUsuario, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
            response = usuario_pb2.ModificarUsuarioResponse(idUsuario=idUsuario)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.ModificarUsuarioResponse()
        
    def EliminarUsuario(self, request, context):
        try:
            idUsuario = request.idUsuario

            udao = UsuarioDAO()
            idUsuario = udao.eliminarUsuario(idUsuario)
            response = usuario_pb2.EliminarUsuarioResponse(idUsuario=idUsuario)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.EliminarUsuarioResponse()

    def TraerTodosLosUsuarios(self, request, context):
        try:
            udao = UsuarioDAO()
            usuarios = udao.traerTodosLosUsuarios()
            usuario_list = usuario_pb2.UsuarioList()
            
            for usuario in usuarios:
                usuario_dto = usuario_pb2.UsuarioGrpcDTO(
                    idUsuario=usuario[0],
                    usuario=usuario[1],
                    password=usuario[2],
                    nombre=usuario[3],
                    apellido=usuario[4],
                    habilitado=usuario[5],
                    casaCentral=usuario[6],
                    idTienda=usuario[7]
                )
                usuario_list.usuarios.append(usuario_dto)
            response = usuario_pb2.TraerTodosLosUsuariosResponse(usuarioList=usuario_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.TraerTodosLosUsuariosResponse()
        
    def TraerTodosLosUsuariosFiltrados(self, request, context):
        try:
            idTienda = request.idTienda
            nombre = request.nombre
            udao = UsuarioDAO()
            usuarios = udao.traerTodosLosUsuariosFiltrados(idTienda, nombre)
            usuario_list = usuario_pb2.UsuarioList()

            if usuarios:
                for usuario in usuarios:
                    usuario_dto = usuario_pb2.UsuarioGrpcDTO(
                        idUsuario=usuario[0],
                        usuario=usuario[1],
                        password=usuario[2],
                        nombre=usuario[3],
                        apellido=usuario[4],
                        habilitado=usuario[5],
                        casaCentral=usuario[6],
                        idTienda=usuario[7]
                    )
                    usuario_list.usuarios.append(usuario_dto)

            response = usuario_pb2.TraerTodosLosUsuariosFiltradosResponse(usuarioList=usuario_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.TraerTodosLosUsuariosFiltradosResponse()

# TIENDA
class TiendaServicer(tienda_pb2_grpc.TiendaServicer):
    def AgregarTienda(self, request, context):
        try:
            idTienda = request.tiendaGrpcDTO.idTienda
            direccion = request.tiendaGrpcDTO.direccion
            ciudad = request.tiendaGrpcDTO.ciudad
            provincia = request.tiendaGrpcDTO.provincia
            habilitado = request.tiendaGrpcDTO.habilitado

            tdao = TiendaDAO()
            idTienda = tdao.agregarTienda(idTienda, direccion, ciudad, provincia, habilitado)
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
        

# PRODUCTO
class ProductoServicer(producto_pb2_grpc.ProductoServicer):
    def AgregarProducto(self, request, context):
        try:
            idProducto = request.productoGrpcDTO.idProducto
            nombre = request.productoGrpcDTO.nombre
            foto = request.productoGrpcDTO.foto
            color = request.productoGrpcDTO.color
            codigo = request.productoGrpcDTO.codigo
            habilitado = request.productoGrpcDTO.habilitado
            talle = request.productoGrpcDTO.talle
            pdao = ProductoDAO()
            sdao = StockDAO()
            idProducto = pdao.agregarProducto(idProducto, nombre, foto, color, codigo, habilitado, talle)
            for tienda in request.tiendas:
                sdao.agregarStock(tienda,0,talle,idProducto)
            return producto_pb2.AgregarProductoResponse(idProducto = idProducto)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.AgregarProductoResponse()

    def AgregarTalle(self, request, context):
        try:
            idProducto = request.idProducto
            talle = request.talle
            sdao = StockDAO()
            idStock = sdao.agregarStock(1,0,talle,idProducto)
            if (idStock > 0):
                for tienda in request.tiendas:
                    sdao.agregarStock(tienda,0,talle,idProducto)
            return producto_pb2.AgregarTalleResponse(idStock = idStock)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.AgregarTalleResponse()


    def ObtenerProducto(self, request, context):
        try:
            pdao = ProductoDAO()
            idProducto = request.idProducto
            talle = request.talle
            producto = pdao.obtenerProducto(idProducto)

            if producto is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'Producto con id {idProducto} no encontrado.')
                return producto_pb2.ObtenerProductoResponse()
                
            sdao = StockDAO()
            listaTiendas = sdao.obtenerTiendasDeProducto(idProducto, talle)
            tienda_list = tienda_pb2.TiendaList()
            if listaTiendas:
                for tienda in listaTiendas:
                    tienda_dto = tienda_pb2.TiendaGrpcDTO(
                        idTienda=tienda[0],
                        direccion=tienda[1],
                        ciudad=tienda[2],
                        provincia=tienda[3],
                        habilitado=tienda[4],
                    )
                    tienda_list.tiendas.append(tienda_dto)

            producto_dto = producto_pb2.ProductoGrpcDTO(
                    idProducto=producto[0],
                    nombre=producto[1],
                    foto=producto[2],
                    color=producto[3],
                    codigo=producto[4],
                    habilitado=producto[5],
                    talle=producto[6]
                ) 
            
            response = producto_pb2.ObtenerProductoResponse(productoGrpcDTO=producto_dto, tiendas=tienda_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.ObtenerProductoResponse()

    def ModificarProducto(self, request, context):
        try:
            idProducto = request.productoGrpcDTO.idProducto
            nombre = request.productoGrpcDTO.nombre
            foto = request.productoGrpcDTO.foto
            color = request.productoGrpcDTO.color
            codigo = request.productoGrpcDTO.codigo
            habilitado = request.productoGrpcDTO.habilitado
            talle = request.productoGrpcDTO.talle

            pdao = ProductoDAO()
            idProducto = pdao.modificarProducto(idProducto, nombre, foto, color, codigo, habilitado, talle)
            response = producto_pb2.ModificarProductoResponse(idProducto=idProducto)

            sdao = StockDAO()
            for tienda in request.tiendas:
                if(tienda.estado):
                    sdao.agregarStock(tienda.id,0,talle,idProducto)
                else:
                    id = sdao.obtenerStockPorTiendaProductoYTalle(tienda.id,talle,idProducto)
                    if(id is not None):
                        sdao.eliminarStock(id)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.ModificarProductoResponse()

    def EliminarProducto(self, request, context):
        try:
            idProducto = request.idProducto

            pdao = ProductoDAO()
            idProducto = pdao.eliminarProducto(idProducto)
            response = producto_pb2.EliminarProductoResponse(idProducto=idProducto)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.EliminarProductoResponse()

    def TraerTodosLosProductos(self, request, context):
        try:
            pdao = ProductoDAO()
            productos = pdao.traerTodosLosProductos(1)
            producto_list = producto_pb2.ProductoList()
            for producto in productos:
                producto_dto = producto_pb2.ProductoGrpcDTO(
                    idProducto=producto[0],
                    nombre=producto[1],
                    foto=producto[2],
                    color=producto[3],
                    codigo=producto[4],
                    habilitado=producto[5],
                    talle=producto[6],
                )
                producto_list.productos.append(producto_dto)
            response = producto_pb2.TraerTodosLosProductosResponse(productoList=producto_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.TraerTodosLosProductosResponse()
        
    def TraerTodosLosProductosFiltrados(self, request, context):
        try:
            nombre = request.nombre
            codigo = request.codigo
            talle = request.talle
            color = request.color
            pdao = ProductoDAO()
            productos = pdao.traerTodosLosProductosFiltrados(1,nombre, codigo, talle, color)
            producto_list = producto_pb2.ProductoList()
            if productos:
                for producto in productos:
                    producto_dto = producto_pb2.ProductoGrpcDTO(
                        idProducto=producto[0],
                        nombre=producto[1],
                        foto=producto[2],
                        color=producto[3],
                        codigo=producto[4],
                        habilitado=producto[5],
                        talle=producto[6],
                    )
                    producto_list.productos.append(producto_dto)

            response = producto_pb2.TraerTodosLosProductosFiltradosResponse(productoList=producto_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.TraerTodosLosProductosFiltradosResponse()
        
# STOCK

    def AgregarStock(self, request, context):
        try:
            idStock = request.idStock
            cantidad = request.cantidad
            sdao = StockDAO()
            sdao.modificarStock(idStock, cantidad)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
        return producto_pb2.AgregarStockResponse()

    def TraerProductosXTienda(self, request, context):
        try:
            pdao = ProductoDAO()
            productos = pdao.traerTodosLosProductos(request.idTienda)
            producto_list = producto_pb2.StockList()
            for producto in productos:
                producto_dto = producto_pb2.StockGrpcDTO(
                    idProducto=producto[0],
                    nombre=producto[1],
                    foto=producto[2],
                    color=producto[3],
                    codigo=producto[4],
                    cantidad=producto[7],
                    talle=producto[6],
                    idStock=producto[8],
                )
                producto_list.productos.append(producto_dto)
            response = producto_pb2.TraerProductosXTiendaResponse(productoList=producto_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.TraerProductosXTiendaResponse()
        
    def TraerProductosFiltradosXTienda(self, request, context):
        try:
            idTienda = request.idTienda
            nombre = request.nombre
            codigo = request.codigo
            talle = request.talle
            color = request.color
            pdao = ProductoDAO()
            productos = pdao.traerTodosLosProductosFiltrados(idTienda, nombre, codigo, talle, color)
            producto_list = producto_pb2.StockList()
            if productos:
                for producto in productos:
                    producto_dto = producto_pb2.StockGrpcDTO(
                        idProducto=producto[0],
                        nombre=producto[1],
                        foto=producto[2],
                        color=producto[3],
                        codigo=producto[4],
                        cantidad=producto[7],
                        talle=producto[6],
                        idStock=producto[8],
                    )
                    producto_list.productos.append(producto_dto)

            response = producto_pb2.TraerProductosFiltradosXTiendaResponse(productoList=producto_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return producto_pb2.TraerProductosFiltradosXTiendaResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuario_pb2_grpc.add_UsuarioServicer_to_server(UsuarioServicer(), server)
    tienda_pb2_grpc.add_TiendaServicer_to_server(TiendaServicer(), server)
    producto_pb2_grpc.add_ProductoServicer_to_server(ProductoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
