import grpc
import testgrpc_pb2
import testgrpc_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = testgrpc_pb2_grpc.PropioStub(channel)
        response = stub.Imprimi(testgrpc_pb2.usuario(cualEsNombre="LUCAS", cualEsPassword="1234"))
        print(f"¿Se imprimió el Password?: {response.yaLoImprimio}")

if __name__ == '__main__':
    run()