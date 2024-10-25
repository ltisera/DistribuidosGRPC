from datetime import datetime
import json
import threading
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

from DAO.filtrosDAO import FiltrosDAO
from protos import usuario_pb2
from protos import usuario_pb2_grpc
from protos import tienda_pb2
from protos import tienda_pb2_grpc
from protos import producto_pb2
from protos import producto_pb2_grpc
from protos import ordenCompra_pb2
from protos import ordenCompra_pb2_grpc
from protos import novedades_pb2
from protos import novedades_pb2_grpc

from DAO.tiendaDAO import TiendaDAO
from DAO.usuarioDAO import UsuarioDAO
from DAO.productoDAO import ProductoDAO
from DAO.stockDAO import StockDAO
from DAO.ordenCompraDAO import OrdenCompraDAO
from DAO.novedadesDAO import NovedadesDAO

# KAFKA
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

# CONSUMIDOR
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)

# SUBSCRIBIRSE A LOS TOPICOS
def actualizar_subscripciones():
    crear_topicos()
    tdao = TiendaDAO()
    tiendas = tdao.traerTodasLasTiendas()
    topics = []
    topics.append("novedades")
    topics += [f"{tienda[0]}-solicitudes" for tienda in tiendas]
    topics += [f"{tienda[0]}-despacho" for tienda in tiendas]
    
    consumer.subscribe(topics)

    print("Suscrito a los siguientes tópicos:")
    for topic in topics:
        print(topic)

# CREAR TOPICOS                       
def crear_topicos():
    admin_client = AdminClient({'bootstrap.servers': 'localhost:9092'})

    tdao = TiendaDAO()
    tiendas = tdao.traerTodasLasTiendas()
    topics = []
    topics.append(f"novedades")
    for tienda in tiendas:
        id_tienda = tienda[0]
        topics.append(f"{id_tienda}-solicitudes")
        topics.append(f"{id_tienda}-despacho")

    existing_topics = admin_client.list_topics().topics.keys()

    if "novedades" in existing_topics:
        print("El tópico 'novedades' ya existe.")
    else:
        print("El tópico 'novedades' no existe y será creado.")

    new_topics = []
    for topic in topics:
        if topic not in existing_topics:
            new_topics.append(NewTopic(topic, num_partitions=1, replication_factor=1))

    if new_topics:
        fs = admin_client.create_topics(new_topics)
        for topic, f in fs.items():
            try:
                f.result()
                print(f'Tópico {topic} creado con éxito.')
            except Exception as e:
                print(f'Error al crear el tópico {topic}: {e}')
    else:
        print("Todos los tópicos ya existen. No se crearon nuevos.")

# CONSUMIR MENSAJES
def consumir_mensajes():
    while True:
        msg = consumer.poll(1.0) 
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error al consumir el mensaje: {msg.error()}')
                break
        else:
            data = json.loads(msg.value().decode('utf-8'))
            print(f'Mensaje recibido: {data}')
            if msg.topic().endswith('-solicitudes'):
                procesar_solicitud(data)
            elif msg.topic().endswith('-despacho'):
                procesar_despacho(data)
            elif msg.topic().endswith('novedades'):
                procesar_novedades(data)

# PROCESAR TOPICO SOLICITUD
def procesar_solicitud(data):
    estado = data.get('estado')
    idOrden = data.get('idOrden')
    observaciones = data.get('observaciones')

    odao = OrdenCompraDAO()
    odao.actualizarOrdenCompra(idOrden, estado, observaciones)

# PROCESAR TOPICO DESPACHO
def procesar_despacho(data):
    idOrdenDespacho = data.get('idOrdenDespacho')
    idOrden = data.get('idOrden')
    odao = OrdenCompraDAO()
    odao.agregarDespachoAOrdenCompra(idOrden, idOrdenDespacho)

# PROCESAR TOPICO NOVEDADES
def procesar_novedades(data):
    try:
        nombre = data.get('nombre')
        talles = data.get('talles')
        url = data.get('url')


        for talle_data in talles:
            talle = talle_data.get('talle')
            color = talle_data.get('color')
            codigo = talle_data.get('codigo')
            ndao = NovedadesDAO()
            ndao.agregarNovedad(codigo, nombre, talle, color, url)
    except Exception as e:
        print(f"Error al procesar novedades: {str(e)}")

# SOAP
import time
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from zeep import Client
from flask import jsonify
from xml.etree import ElementTree as ET
app = Flask(__name__)
CORS(app)

@app.route('/soap/wsdl', methods=['GET'])
def get_wsdl():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../wsdl'), 'service.wsdl')

def serve_flask():
    app.run(port=5000)

# CARGAR WSDL
def cargar_wsdl():
    wsdl_url = 'http://localhost:5000/soap/wsdl'
    try:
        client = Client(wsdl_url)
        print(client.wsdl.services)
        return client
    except Exception as e:
        print(f'Error al cargar WSDL: {e}')
        return None
    
@app.route('/soap/consultar_ordenes', methods=['POST'])
def consultar_ordenes():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:5000/soap'}
    codigo_producto_elem = root.find('.//tns:codigo_producto', namespaces)
    rango_fechas_elem = root.find('.//tns:rango_fechas', namespaces)
    estado_elem = root.find('.//tns:estado', namespaces)
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)

    codigo_producto = codigo_producto_elem.text if codigo_producto_elem is not None else None
    estado = estado_elem.text if estado_elem is not None else None
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None

    rango_fechas = None
    if rango_fechas_elem is not None and rango_fechas_elem.text:
        fechas = rango_fechas_elem.text.split(',')
        if len(fechas) == 2:
            start_date = fechas[0].strip()
            end_date = fechas[1].strip()
            if start_date and end_date:
                rango_fechas = [
                    int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) * 1000,
                    int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) * 1000
                ]
            else:
                rango_fechas = None

    odao = OrdenCompraDAO()
    resultados = odao.filtrarOrdenes(codigo_producto, rango_fechas, estado, id_tienda)

    if resultados is None:
        return "<Error>Hubo un problema al consultar las órdenes.</Error>", 500, {'Content-Type': 'text/xml'}

    response_xml = convertir_a_xml(resultados)
    return response_xml, 200, {'Content-Type': 'text/xml'}

def convertir_a_xml(data):
    root = ET.Element("Resultados")
    for item in data:
        orden = ET.SubElement(root, "Orden")

        ET.SubElement(orden, "IdOrden").text = str(item[0])
        ET.SubElement(orden, "Producto").text = str(item[1])
        ET.SubElement(orden, "Estado").text = str(item[3])
        ET.SubElement(orden, "Observaciones").text = str(item[4])
        ET.SubElement(orden, "FechaSolicitud").text = str(item[5])
        ET.SubElement(orden, "FechaRecepcion").text = str(item[6])
        ET.SubElement(orden, "OrdenDespacho").text = str(item[7])
        ET.SubElement(orden, "Tienda").text = str(item[8])
        ET.SubElement(orden, "CantidadTotal").text = str(item[9])

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)  

@app.route('/soap/guardar_filtro', methods=['POST'])
def guardar_filtro():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:5000/soap'}
    id_usuario_elem = root.find('.//tns:id_usuario', namespaces)
    nombre_elem = root.find('.//tns:nombre', namespaces)
    codigo_producto_elem = root.find('.//tns:codigo_producto', namespaces)
    rango_fechas_elem = root.find('.//tns:rango_fechas', namespaces)
    estado_elem = root.find('.//tns:estado', namespaces)
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)

    id_usuario = id_usuario_elem.text if id_usuario_elem is not None else None
    nombre = nombre_elem.text if nombre_elem is not None else None
    codigo_producto = codigo_producto_elem.text if codigo_producto_elem is not None else None
    estado = estado_elem.text if estado_elem is not None else None
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None

    rango_fechas = None
    if rango_fechas_elem is not None and rango_fechas_elem.text:
        fechas = rango_fechas_elem.text.split(',')
        if len(fechas) == 2:
            start_date = fechas[0].strip()
            end_date = fechas[1].strip()
            if start_date and end_date:
                rango_fechas = [
                    int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) * 1000,
                    int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) * 1000
                ]
            else:
                rango_fechas = None

    fdao = FiltrosDAO()
    fdao.guardar_filtro(id_usuario, nombre, codigo_producto, rango_fechas, estado, id_tienda)
    
@app.route('/soap/obtener_filtros', methods=['POST'])
def obtener_filtros():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:5000/soap'}
    id_usuario_elem = root.find('.//tns:id_usuario', namespaces)
    id_usuario = id_usuario_elem.text if id_usuario_elem is not None else None

    fdao = FiltrosDAO()
    resultados = fdao.obtener_filtros(id_usuario)

    if resultados is None:
        return "<Error>Hubo un problema al obtener los filtros.</Error>", 500, {'Content-Type': 'text/xml'}
    
    root = ET.Element("Resultados")
    for item in resultados:
        filtro = ET.SubElement(root, "Filtro")
        ET.SubElement(filtro, "Id").text = str(item[0])
        ET.SubElement(filtro, "Nombre").text = str(item[1])
        ET.SubElement(filtro, "Producto").text = str(item[3])
        ET.SubElement(filtro, "RangoFechasStart").text = str(item[4])
        ET.SubElement(filtro, "RangoFechasEnd").text = str(item[5])
        ET.SubElement(filtro, "Estado").text = str(item[6])
        ET.SubElement(filtro, "IdTienda").text = str(item[7])

    response_xml =  ET.tostring(root, encoding='utf-8', xml_declaration=True)  
    return response_xml, 200, {'Content-Type': 'text/xml'}

@app.route('/soap/obtener_filtro', methods=['GET'])
def obtener_filtro():
    filtro_id = request.args.get('id')
    fdao = FiltrosDAO()
    filtro = fdao.obtener_filtro_por_id(filtro_id)

    if filtro is None:
        return "<Error>No se encontró el filtro.</Error>", 404, {'Content-Type': 'text/xml'}

    root = ET.Element("Filtro")

    def format_date(timestamp):
        if timestamp is None or timestamp == "None":
            return ""
        return datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')


    ET.SubElement(root, "Nombre").text = str(filtro[1])
    ET.SubElement(root, "Producto").text = str(filtro[3]) if filtro[3] is not None else ""
    ET.SubElement(root, "RangoFechasStart").text = format_date(filtro[4])
    ET.SubElement(root, "RangoFechasEnd").text = format_date(filtro[5])
    ET.SubElement(root, "Estado").text = str(filtro[6]) if filtro[6] is not None else ""
    ET.SubElement(root, "IdTienda").text = str(filtro[7]) if filtro[7] is not None else ""

    response_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)  
    return response_xml, 200, {'Content-Type': 'text/xml'}

@app.route('/soap/editar_filtro', methods=['POST'])
def editar_filtro():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:5000/soap'}
    id_elem = root.find('.//tns:id', namespaces)
    nombre_elem = root.find('.//tns:nombre', namespaces)
    codigo_producto_elem = root.find('.//tns:codigo_producto', namespaces)
    rango_fechas_elem = root.find('.//tns:rango_fechas', namespaces)
    estado_elem = root.find('.//tns:estado', namespaces)
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)

    id = id_elem.text if id_elem is not None else None
    nombre = nombre_elem.text if nombre_elem is not None else None
    codigo_producto = codigo_producto_elem.text if codigo_producto_elem is not None else None
    estado = estado_elem.text if estado_elem is not None else None
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None

    if rango_fechas_elem is not None and rango_fechas_elem.text:
        fechas = rango_fechas_elem.text.split(',')
        if len(fechas) == 2:
            start_date = fechas[0].strip()
            end_date = fechas[1].strip()
            if start_date and end_date:
                rango_fechas = [
                    int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) * 1000,
                    int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) * 1000
                ]
            else:
                rango_fechas = None
                
        
    fdao = FiltrosDAO()
    fdao.editar_filtro(id, nombre, codigo_producto, rango_fechas, estado, id_tienda)
    return "Filtro editado exitosamente", 200

@app.route('/soap/borrar_filtro', methods=['POST'])
def borrar_filtro():
    xml_data = request.data
    xml_doc = ET.fromstring(xml_data)
    
    namespaces = {'tns': 'http://localhost:5000/soap'}
    filtro_id_elem = xml_doc.find('.//tns:id', namespaces)
    
    if filtro_id_elem is None:
        return "ID del filtro no encontrado", 400

    filtro_id = filtro_id_elem.text

    fdao = FiltrosDAO()
    fdao.borrar_filtro(filtro_id)
    
    return "Filtro eliminado", 200

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
            actualizar_subscripciones()
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

# ORDEN COMPRA
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

# NOVEDADES
class NovedadesServicer(novedades_pb2_grpc.NovedadesServicer):
    def EliminarNovedad(self, request, context):
        try:
            codigo = request.codigo
            ndao = NovedadesDAO()
            codigo = ndao.eliminarNovedad(codigo)
            response = novedades_pb2.EliminarNovedadResponse(codigo=codigo)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return novedades_pb2.EliminarNovedadResponse()

    def TraerTodasLasNovedades(self, request, context):
        try:
            ndao = NovedadesDAO()
            novedades = ndao.traerTodasLasNovedades()
            novedad_list = novedades_pb2.NovedadList()
            
            for novedad in novedades:
                novedad_dto = novedades_pb2.NovedadGrpcDTO(
                    codigo=novedad[0],
                    nombre=novedad[1],
                    talle=novedad[2],
                    color=novedad[3],
                    url=novedad[4],
                )
                novedad_list.novedades.append(novedad_dto)
            response = novedades_pb2.TraerTodasLasNovedadesResponse(novedadList=novedad_list)
            return response
        except Exception as e:
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return novedades_pb2.TraerTodasLasNovedadesResponse()

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
    
    
