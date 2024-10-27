from PIL import Image as PILImage
import tempfile
from flask import Flask, request, Response, send_file, send_from_directory
import os, sys
from xml.etree import ElementTree as ET

from flask_cors import CORS
from fpdf import FPDF
import requests

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

@app.route('/soap/wsdl', methods=['GET'])
def get_wsdl():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../wsdl'), 'catalogo.wsdl')

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

    cdao = CatalogoDAO()
    cdao.agregarCatalogo(nombre, id_tienda)

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

@app.route('/listaProductosSoap', methods=['POST'])
def listar_productos():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:8080/soap'}
    id_tienda_elem = root.find('.//tns:id_tienda', namespaces)
    id_catalogo_elem = root.find('.//tns:id_catalogo', namespaces)
    
    id_tienda = id_tienda_elem.text if id_tienda_elem is not None else None
    id_catalogo = id_catalogo_elem.text if id_catalogo_elem is not None else None

    cdao = CatalogoDAO()
    resultados = cdao.obtenerProductosPorTienda(id_tienda)

    resultadosCatalogo = cdao.obtenerProductosPorCatalogo(id_catalogo)

    if resultados is None:
        return "<Error>Hubo un problema al consultar los productos.</Error>", 500, {'Content-Type': 'text/xml'}

    ids_productos_en_catalogo = {f"{prod[0]},{prod[4]}" for prod in resultadosCatalogo}

    root = ET.Element("Resultados")
    for item in resultados:
        producto = ET.SubElement(root, "Producto")
        id_producto = str(item[0])
        talle = str(item[4])
        ET.SubElement(producto, "IdProducto").text = str(item[0])
        ET.SubElement(producto, "Nombre").text = str(item[1])
        ET.SubElement(producto, "Foto").text = str(item[2])
        ET.SubElement(producto, "Color").text = str(item[3])
        ET.SubElement(producto, "Talle").text = str(item[4])
        ET.SubElement(producto, "EnCatalogo").text = "true" if f"{id_producto},{talle}" in ids_productos_en_catalogo else "false"

    response_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    return response_xml, 200, {'Content-Type': 'text/xml'}

@app.route('/agregarProductosSoap', methods=['POST'])
def agregar_productos():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:8080/soap'}
    id_catalogo_elem = root.find('.//tns:id_catalogo', namespaces)
    productos_elem = root.find('.//tns:productos', namespaces)
    
    id_catalogo = id_catalogo_elem.text if id_catalogo_elem is not None else None
    productos = productos_elem.text.split(',') if productos_elem is not None else []

    cdao = CatalogoDAO()
    try:
        for i in range(0, len(productos), 2):
            if i + 1 < len(productos):
                id_producto = productos[i]
                talle = productos[i + 1]
                cdao.agregarProductoACatalogo(id_catalogo, id_producto, talle)
            else:
                print(f"Producto sin talle: {productos[i]}")

        response_xml = ET.Element("Resultados")
        ET.SubElement(response_xml, "Mensaje").text = "Productos agregados con éxito"
        response = ET.tostring(response_xml, encoding='utf-8', xml_declaration=True)

        return response, 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        print(f"Error al agregar productos: {str(e)}")
        return "<Error>Hubo un problema al agregar los productos.</Error>", 500, {'Content-Type': 'text/xml'}
    
@app.route('/eliminarProductosSoap', methods=['POST'])
def eliminar_productos():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:8080/soap'}
    id_catalogo_elem = root.find('.//tns:id_catalogo', namespaces)
    productos_elem = root.find('.//tns:productos', namespaces)
    
    id_catalogo = id_catalogo_elem.text if id_catalogo_elem is not None else None
    productos = productos_elem.text.split(',') if productos_elem is not None else []

    cdao = CatalogoDAO()
    try:
        for i in range(0, len(productos), 2):
            if i + 1 < len(productos):
                id_producto = productos[i]
                talle = productos[i + 1]
                cdao.eliminarProductoDeCatalogo(id_catalogo, id_producto, talle)
            else:
                print(f"Producto sin talle: {productos[i]}")

        response_xml = ET.Element("Resultados")
        ET.SubElement(response_xml, "Mensaje").text = "Productos eliminados con éxito"
        response = ET.tostring(response_xml, encoding='utf-8', xml_declaration=True)

        return response, 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        print(f"Error al eliminar productos: {str(e)}")
        return "<Error>Hubo un problema al eliminar los productos.</Error>", 500, {'Content-Type': 'text/xml'}

@app.route('/exportarCatalogoSoap', methods=['POST'])
def exportar_catalogo():
    xml_data = request.data
    root = ET.fromstring(xml_data)

    namespaces = {'tns': 'http://localhost:8080/soap'}
    id_catalogo_elem = root.find('.//tns:id_catalogo', namespaces)
    id_catalogo = id_catalogo_elem.text if id_catalogo_elem is not None else None

    cdao = CatalogoDAO()
    catalogo = cdao.obtenerCatalogo(id_catalogo)
    productos = cdao.obtenerProductosPorCatalogo(id_catalogo)

    if catalogo is None or productos is None:
        return "<Error>No se pudo recuperar los datos del catálogo.</Error>", 500, {'Content-Type': 'text/xml'}

    catalogo_nombre = catalogo[0]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    # Titulo del catalogo
    pdf.cell(0, 10, f'Catálogo: {catalogo_nombre}', ln=True)
    pdf.ln(10)

    for idx, producto in enumerate(productos):
        imagen_url = producto[2]
    
        try:
            response = requests.get(imagen_url)
            response.raise_for_status()
            temp_image_path = f'temp_image_{idx}.jpg'

            with open(temp_image_path, 'wb') as img_file:
                img_file.write(response.content)

            with PILImage.open(temp_image_path) as img:
                imagen_ancho, imagen_alto = img.size
                nuevo_ancho = 50
                factor = nuevo_ancho / imagen_ancho
                imagen_alto = int(imagen_alto * factor)

            espacio_requerido = imagen_alto + 30 + 20  # Espacio para la imagen y el texto
            if pdf.get_y() + espacio_requerido > pdf.page_break_trigger:
                pdf.add_page()

            pdf.image(temp_image_path, x=10, y=pdf.get_y(), w=nuevo_ancho, h=imagen_alto)

            # Ajustar la posición para el nombre y la descripción
            current_y = pdf.get_y() + imagen_alto + 10  # Espacio después de la imagen
            pdf.set_y(current_y)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, producto[1], ln=True)  
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Color: {producto[3]}, Talle: {producto[4]}', ln=True)

            # Espacio adicional después de cada producto
            pdf.ln(10)  

            os.remove(temp_image_path)

        except Exception as e:
            print(f"Error al descargar la imagen: {e}")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        pdf.output(temp_pdf.name, 'F')
        temp_pdf.seek(0)

    return send_file(temp_pdf.name, as_attachment=True, download_name=f'catalogo_{id_catalogo}.pdf', mimetype='application/pdf')

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
