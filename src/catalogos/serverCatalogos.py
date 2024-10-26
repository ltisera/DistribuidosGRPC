from flask import Flask, request, Response
import os, sys
from xml.etree import ElementTree as ET

from flask_cors import CORS

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(CURRENT_DIR + '\\DAO')
sys.path.append(CURRENT_DIR + '\\settings')

PARENT_DIR = os.path.dirname(CURRENT_DIR)
PROTO_DIR = os.path.join(PARENT_DIR, 'protos')
sys.path.append(PROTO_DIR)
sys.path.append(os.path.join(CURRENT_DIR, 'dao'))

from DAO.catalogoDAO import CatalogoDAO
from DAO.usuarioDAO import UsuarioDAO

app = Flask(__name__)
CORS(app)

@app.route('/soap/crear_catalogo', methods=['POST'])
def crear_catalogo():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    print("Entro a crear catalogo")

    namespaces = {'tns': 'http://localhost:8080/soap'}
    nombre_elem = root.find('.//tns:nombre', namespaces)
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)

    nombre = nombre_elem.text if nombre_elem is not None else None
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None

    catalogo_dao = CatalogoDAO()
    catalogo_dao.agregarCatalogo(nombre, id_tienda)

    return "Catalogo creado exitosamente", 200

@app.route('/listaCatalogosSoap', methods=['POST'])
def listar_catalogos():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:8080/soap'}
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None

    cdao = CatalogoDAO()
    resultados = cdao.obtenerCatalogos(id_tienda)

    if resultados is None:
        return "<Error>Hubo un problema al consultar las órdenes.</Error>", 500, {'Content-Type': 'text/xml'}

    root = ET.Element("Resultados")
    for item in resultados:
        catalogo = ET.SubElement(root, "Catalogo")
        ET.SubElement(catalogo, "IdCatalogo").text = str(item[0])
        ET.SubElement(catalogo, "Nombre").text = str(item[1])
        ET.SubElement(catalogo, "IdTienda").text = str(item[2])

    response_xml =  ET.tostring(root, encoding='utf-8', xml_declaration=True)  
    return response_xml, 200, {'Content-Type': 'text/xml'}

@app.route('/eliminarCatalogoSoap', methods=['POST'])
def borrar_catalogo():
    xml_data = request.data
    xml_doc = ET.fromstring(xml_data)
    
    namespaces = {'tns': 'http://localhost:8080/soap'}
    catalogo_id_elem = xml_doc.find('.//tns:id_catalogo', namespaces)
    
    if catalogo_id_elem is None:
        return "ID del filtro no encontrado", 400

    catalogo_id = catalogo_id_elem.text

    cdao = CatalogoDAO()
    cdao.eliminarCatalogo(catalogo_id)
    
    return "Catalogo eliminado", 200 

@app.route('/procesarCSV', methods=['POST'])
def procesarCSV():
    print("ENTREEEEEE")
    errores = []
    soap_request = request.data.decode('utf-8')
    # Obtener archivo del request
    start_index = soap_request.find('<archivo>') + len('<archivo>')
    end_index = soap_request.find('</archivo>')
    archivo = soap_request[start_index:end_index]
    if not archivo:
        return Response(
            create_soap_response("No se proporcionó un archivo"), 
            content_type="text/xml"
        )

    # Leer el archivo y procesar cada línea
    lineas = archivo.splitlines()
    udao = UsuarioDAO()
    for num_linea, linea in enumerate(lineas, start=1):
        print(linea)
        campos = linea.split(";")
        
        if len(campos) != 5:
            errores.append(f"Línea {num_linea}: número incorrecto de campos.")
            continue
        
        usuario, password, nombre, apellido, codigo_tienda = campos

        try:
            codigo_tienda = int(codigo_tienda)
        except ValueError:
            errores.append(f"Línea {num_linea}: el campo 'codigo_tienda' no es un número.")
            continue

        esCasaCentral = codigo_tienda == 1
        error = udao.agregarUsuario(usuario, password, nombre, apellido, True, esCasaCentral, codigo_tienda)
        if error:
            errores.append(f"Línea {num_linea}: {error}")

    response_content = create_soap_response(errores)
    return Response(response_content, content_type="text/xml")

def create_soap_response(errores):
    error_messages = "".join(f"<error>{error}</error>" for error in errores)
    if not errores:
        error_messages = "<error>No hubo errores.</error>"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <procesarCSVResponse>
            <errores>
                {error_messages}
            </errores>
        </procesarCSVResponse>
    </soap:Body>
</soap:Envelope>
"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
