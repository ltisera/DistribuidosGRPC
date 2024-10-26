import grpc
from protos import producto_pb2
from protos import producto_pb2_grpc
from protos import tienda_pb2
from DAO.productoDAO import ProductoDAO
from DAO.stockDAO import StockDAO

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
            productos = pdao.traerTodosLosProductos(request.idTienda, True)
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
            productos = pdao.traerTodosLosProductosFiltrados(idTienda, nombre, codigo, talle, color, True)
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