import os
from datetime import datetime
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from zeep import Client
from flask import jsonify
from xml.etree import ElementTree as ET

from DAO.ordenCompraDAO import OrdenCompraDAO
from DAO.filtrosDAO import FiltrosDAO

app = Flask(__name__)
CORS(app)

@app.route('/soap/wsdl', methods=['GET'])
def get_wsdl():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../wsdl'), 'service.wsdl')

def serve_flask():
    app.run(port=9000)

# CARGAR WSDL
def cargar_wsdl():
    wsdl_url = 'http://localhost:9000/soap/wsdl'
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

    namespaces = {'tns': 'http://localhost:9000/soap'}
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

    namespaces = {'tns': 'http://localhost:9000/soap'}
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

    namespaces = {'tns': 'http://localhost:9000/soap'}
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

    namespaces = {'tns': 'http://localhost:9000/soap'}
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
    
    namespaces = {'tns': 'http://localhost:9000/soap'}
    filtro_id_elem = xml_doc.find('.//tns:id', namespaces)
    
    if filtro_id_elem is None:
        return "ID del filtro no encontrado", 400

    filtro_id = filtro_id_elem.text

    fdao = FiltrosDAO()
    fdao.borrar_filtro(filtro_id)
    
    return "Filtro eliminado", 200 