import grpc
from concurrent import futures
import testgrpc_pb2
import testgrpc_pb2_grpc

import mysql

class PropioServicer(testgrpc_pb2_grpc.PropioServicer):
    def Imprimi(self, request, context):
        if(request.cualEsNombre != "LUCAS"):
            nombre_completo = f"{request.cualEsNombre} {request.cualEsPassword}"
            print(f"Nombre completo recibido: {nombre_completo}")
            print("Password:" + request.cualEsPassword)
            print("Nombre:" + request.cualEsNombre)
            return testgrpc_pb2.siImprimio(yaLoImprimio=True)
        else:
            return testgrpc_pb2.siImprimio(yaLoImprimio=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    testgrpc_pb2_grpc.add_PropioServicer_to_server(PropioServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()