from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/catalogoSoap', methods=['POST'])
def soap_server():
    print("Aca estoy narigon")
    # Obtener el contenido de la solicitud
    soap_request = request.data.decode('utf-8')
    
    # Aquí procesamos la solicitud SOAP
    if '<crearCatalogo>' in soap_request:
        # Extraer el nombre del catálogo
        start_index = soap_request.find('<nombre>') + len('<nombre>')
        end_index = soap_request.find('</nombre>')
        nombre = soap_request[start_index:end_index]
        
        if not nombre:
            return generate_soap_fault("Nombre del catálogo es obligatorio.")
        
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6000)
