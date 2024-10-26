from flask import Flask, request, Response

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

from DAO.catalogoDAO import CatalogoDAO
from DAO.usuarioDAO import UsuarioDAO

app = Flask(__name__)

@app.route('/catalogoSoap', methods=['POST'])
def soap_server():
    # Obtener el contenido de la solicitud
    soap_request = request.data.decode('utf-8')
    
    # Aquí procesamos la solicitud SOAP
    if '<nombre>' in soap_request:
        # Extraer el nombre del catálogo
        start_index = soap_request.find('<nombre>') + len('<nombre>')
        end_index = soap_request.find('</nombre>')
        nombre = soap_request[start_index:end_index]
        if not nombre:
            return generate_soap_fault("Nombre del catálogo es obligatorio.")
        else:
            #HACER LLAMADAS PARA CREAR CATALOGO
            catDao = CatalogoDAO()
            catDao.agregarCatalogo(nombre)
            print(nombre)
        
        # Si todo es correcto, generamos la respuesta
        return generate_soap_response(nombre)
    else:
        return generate_soap_fault("Solicitud no válida.")

def generate_soap_response(nombre):
    # Respuesta SOAP exitosa
    response = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Body>
      <crearCatalogoResponse>
         <status>200</status>
         <message>Catálogo '{nombre}' creado exitosamente</message>
      </crearCatalogoResponse>
   </soap:Body>
</soap:Envelope>"""
    return Response(response, mimetype='text/xml')

def generate_soap_fault(error_message):
    # Respuesta SOAP de error
    response = f"""<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Body>
      <soap:Fault>
         <faultcode>SOAP-ENV:Client</faultcode>
         <faultstring>{error_message}</faultstring>
      </soap:Fault>
   </soap:Body>
</soap:Envelope>"""
    return Response(response, mimetype='text/xml', status=500)


#REVISAR

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
    app.run(host='127.0.0.1', port=6000)
