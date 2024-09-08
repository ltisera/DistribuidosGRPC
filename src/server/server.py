import grpc
from concurrent import futures
import os, sys

from server.dao.usuarioDAO import UsuarioDAO

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(CURRENT_DIR + '\\DAO')

PARENT_DIR = os.path.dirname(CURRENT_DIR)
PROTO_DIR = os.path.join(PARENT_DIR, 'protos')
sys.path.append(PROTO_DIR)
sys.path.append(os.path.join(CURRENT_DIR, 'dao'))

from protos import usuario_pb2
from protos import usuario_pb2_grpc

class UsuarioServicer(usuario_pb2_grpc.UsuarioServicer):
    def IniciarSesion(self, request, context):
        usuario = request.usuario
        password = request.password
        udao = UsuarioDAO()
        exito = udao.iniciarSesion(usuario, password)
        return usuario_pb2.IniciarSesionResponse(exito=exito)

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
            idUsuario = udao.agregarUsuario( usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
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

            usuario_dto = usuario_pb2.UsuarioObtenerGrpcDTO(
                    idUsuario=usuario[0],
                    usuario=usuario[1],
                    password=usuario[2],
                    nombre=usuario[3],
                    apellido=usuario[4],
                    habilitado=usuario[5],
                    casaCentral=usuario[6],
                    idTienda=usuario[7]
                )

            response = usuario_pb2.ObtenerUsuarioResponse(usuarioObtenerGrpcDTO=usuario_dto)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return usuario_pb2.ObtenerUsuarioResponse()

    def ModificarUsuario(self, request, context):
        try:
            idUsuario = request.usuarioObtenerGrpcDTO.idUsuario
            usuario = request.usuarioObtenerGrpcDTO.usuario
            password = request.usuarioObtenerGrpcDTO.password
            nombre = request.usuarioObtenerGrpcDTO.nombre
            apellido = request.usuarioObtenerGrpcDTO.apellido
            habilitado = request.usuarioObtenerGrpcDTO.habilitado
            casaCentral = request.usuarioObtenerGrpcDTO.casaCentral
            idTienda = request.usuarioObtenerGrpcDTO.idTienda

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
                usuario_dto = usuario_pb2.UsuarioObtenerGrpcDTO(
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
                    usuario_dto = usuario_pb2.UsuarioObtenerGrpcDTO(
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuario_pb2_grpc.add_UsuarioServicer_to_server(UsuarioServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
