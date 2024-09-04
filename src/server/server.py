import os, sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(CURRENT_DIR + '\\DAO')

PARENT_DIR = os.path.dirname(CURRENT_DIR)  # Un nivel arriba del directorio actual
PROTO_DIR = os.path.join(PARENT_DIR, 'protos')  # Directorio 'proto' un nivel arriba

sys.path.append(PROTO_DIR)


import grpc
from concurrent import futures
import mysql

from protos import usuario_pb2, usuario_pb2_grpc



from DAO.UsuarioDAO import UsuarioDAO

class pepito(usuario_pb2_grpc.UsuarioServicer):
    def Imprimi(self, request, context):
        
        usuario = request.usuarioGrpcDTO.usuario
        password = request.usuarioGrpcDTO.password
        nombre = request.usuarioGrpcDTO.nombre
        apellido = request.usuarioGrpcDTO.apellido
        habilitado = request.usuarioGrpcDTO.habilitado
        casaCentral = request.usuarioGrpcDTO.casaCentral
        idTienda = 1

        print("Entra: " + nombre + " " + password)
        udao = UsuarioDAO()
        print("La clase se creoo")
        #udao.agregarUsuario(2, request.cualEsNombre, request.cualEsPaswword,"Cam","Matho", True, False,123)
        queDevuelve = udao.agregarUsuario( usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
        print("Esto devuelve: " + str(queDevuelve))
        return usuario_pb2.AgregarUsuarioResponse(queDevuelve)
        
        

def serve():
    print("Me aseguro")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuario_pb2_grpc.add_UsuarioServicer_to_server(pepito(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()