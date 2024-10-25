const express = require('express');
const http = require('http'); // O https si tu server usa SSL.
const app = express();
  
app.use(express.json());



function crearCatalogo(req, res){
    const {nombre} = req.body;
    const mensajeSoap = `
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Body>
          <nombre>${nombre}</nombre>
        </soapenv:Body>
      </soapenv:Envelope>
    `;
    
    const options = {
        hostname: 'localhost',
        port: 6000,
        path: '/catalogoSoap',
        method: 'POST',
        headers: {
          'Content-Type': 'text/xml',
          'Content-Length': Buffer.byteLength(mensajeSoap),
          'SOAPAction': '' // Puede ser requerido por algunos servidores.
        }
      };

      return new Promise((resolve, reject) => {
        const req = http.request(options, (res) => {
          let responseData = '';
    
          res.on('data', (chunk) => {
            responseData += chunk;
          });
    
          res.on('end', () => {
            resolve(responseData); // Devolvemos la respuesta SOAP.
          });
        });
    
        req.on('error', (error) => {
          reject(error); // En caso de error.
        });
        console.log("Te envio el xml");
        req.write(mensajeSoap); // Enviamos el cuerpo SOAP.
        req.end();
      });


    
};

module.exports = {
    crearCatalogo
  };


//***************************************************

/*
  
  const enviarCatalogoSOAP = (nombreCatalogo) => {
    const soapBody = `
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>
          <nombre>${nombreCatalogo}</nombre>
        </soapenv:Body>
      </soapenv:Envelope>
    `;
  
    const options = {
      hostname: 'localhost',
      port: 5000,
      path: '/soap',
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml',
        'Content-Length': Buffer.byteLength(soapBody),
        'SOAPAction': '' // Puede ser requerido por algunos servidores.
      }
    };
  
    return new Promise((resolve, reject) => {
      const req = http.request(options, (res) => {
        let responseData = '';
  
        res.on('data', (chunk) => {
          responseData += chunk;
        });
  
        res.on('end', () => {
          resolve(responseData); // Devolvemos la respuesta SOAP.
        });
      });
  
      req.on('error', (error) => {
        reject(error); // En caso de error.
      });
  
      req.write(soapBody); // Enviamos el cuerpo SOAP.
      req.end();
    });
  };
  
  // Definimos una ruta en Express para enviar SOAP.
  app.post('/enviar-catalogo', async (req, res) => {
    const { nombreCatalogo } = req.body; // Obtenemos el nombre del body.
  
    try {
      const soapResponse = await enviarCatalogoSOAP(nombreCatalogo);
      res.send(`Respuesta del servidor: ${soapResponse}`);
    } catch (error) {
      res.status(500).send(`Error al enviar SOAP: ${error.message}`);
    }
  });
  
  // Iniciamos el servidor en el puerto 3000.
  const PORT = 3000;
  app.listen(PORT, () => {
    console.log(`Servidor Express escuchando en http://localhost:${PORT}`);
  });

  */