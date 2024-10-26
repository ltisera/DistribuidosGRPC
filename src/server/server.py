from concurrent import futures
import os, sys, time, threading, grpc

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(CURRENT_DIR + '\\DAO')
sys.path.append(CURRENT_DIR + '\\settings')
PARENT_DIR = os.path.dirname(CURRENT_DIR)
PROTO_DIR = os.path.join(PARENT_DIR, 'protos')
sys.path.append(PROTO_DIR)
sys.path.append(os.path.join(CURRENT_DIR, 'dao'))

# PROTOS
from protos import usuario_pb2_grpc
from protos import tienda_pb2_grpc
from protos import producto_pb2_grpc
from protos import ordenCompra_pb2_grpc
from protos import novedades_pb2_grpc

# SERVICIOS
from services.usuarioService import UsuarioServicer
from services.productoService import ProductoServicer
from services.tiendaService import TiendaServicer
from services.ordenCompraService import OrdenCompraServicer
from services.novedadesService import NovedadesServicer

# KAFKA
from services.kafkaService import actualizar_subscripciones, consumir_mensajes

# SOAP
from services.soapService import serve_flask, cargar_wsdl

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuario_pb2_grpc.add_UsuarioServicer_to_server(UsuarioServicer(), server)
    tienda_pb2_grpc.add_TiendaServicer_to_server(TiendaServicer(), server)
    producto_pb2_grpc.add_ProductoServicer_to_server(ProductoServicer(), server)
    ordenCompra_pb2_grpc.add_OrdenCompraServicer_to_server(OrdenCompraServicer(), server)
    novedades_pb2_grpc.add_NovedadesServicer_to_server(NovedadesServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    actualizar_subscripciones()
    threading.Thread(target=consumir_mensajes, daemon=True).start()
    threading.Thread(target=serve_flask, daemon=True).start()
    time.sleep(2)
    client = cargar_wsdl()
    if client:
        print("WSDL cargado correctamente.")
    else:
        print("No se pudo cargar el WSDL.")
    serve()
    
    
