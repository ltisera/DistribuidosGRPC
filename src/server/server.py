
import os, sys

import grpc
from concurrent import futures
import mysql

import testgrpc_pb2
import testgrpc_pb2_grpc

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
#sys.path.append(CURRENT_DIR + '\\proto')
sys.path.append(CURRENT_DIR + '\\DAO')


from DAO.UsuarioDAO import UsuarioDAO

class PropioServicer(testgrpc_pb2_grpc.PropioServicer):
    def Imprimi(self, request, context):
        print("Me aseguro2")
        print("Me aseguro2")
        
        nombre = request.cualEsNombre
        password = request.cualEsPassword
        print("Entra: " + nombre + " " + password)
        udao = UsuarioDAO()
        print("La clase se creoo")
        #udao.agregarUsuario(2, request.cualEsNombre, request.cualEsPaswword,"Cam","Matho", True, False,123)
        queDevuelve = udao.agregarUsuario(9, nombre, password, "no9r", "ceat9rhoc", True, False, 123)
        print("Esto devuelve: " + queDevuelve)
        return testgrpc_pb2.siImprimio(yaLoImprimio = queDevuelve)
        

def serve():
    print("Me aseguro")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    testgrpc_pb2_grpc.add_PropioServicer_to_server(PropioServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()