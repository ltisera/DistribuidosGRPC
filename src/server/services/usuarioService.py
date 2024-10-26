import grpc
from protos import usuario_pb2
from protos import usuario_pb2_grpc
from DAO.usuarioDAO import UsuarioDAO

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
            return usuario_pb2.AgregarUsuarioResponse(idUsuario = idUsuario)
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.AgregarUsuarioResponse()
        
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