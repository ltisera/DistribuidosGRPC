const path = require('path');
const session = require('express-session');

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

const catalogoController = require('./controllers/catalogoController');
const usuarioController = require('./controllers/usuarioController');
const tiendaController = require('./controllers/tiendaController');
const productoController = require('./controllers/productoController');
const ordenCompraController = require('./controllers/ordenCompraController');
const novedadesController = require('./controllers/novedadesController');

app.use(session({
  secret: 'tp-grpc',
  resave: false,
  saveUninitialized: true
}));


//CAMBIAR DE LUGAR
const http = require('http'); // O https si tu server usa SSL.
const multer = require('multer');
const fs = require('fs');

const upload = multer({ dest: 'uploads/' });

app.post('/cargarCSV', upload.single('csvFile'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No se ha proporcionado ningún archivo.');
  }

  // Leer el archivo CSV
  const csvFilePath = req.file.path;
  const fileData = fs.readFileSync(csvFilePath, 'utf8');

  const mensajeXml = `
      <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
              <procesarCSV>
                  <archivo>${fileData}</archivo>
                  <nombre>${req.file.originalname}</nombre>
              </procesarCSV>
          </soap:Body>
      </soap:Envelope>
  `;

  const options = {
      hostname: 'localhost',
      port: 6000,
      path: '/procesarCSV',
      method: 'POST',
      headers: {
          'Content-Type': 'text/xml',
          'Content-Length': Buffer.byteLength(mensajeXml),
          'SOAPAction': '' // Puede ser requerido por algunos servidores.
      }
  };

  const soapRequest = http.request(options, (soapRes) => {
      let responseData = '';

      soapRes.on('data', (chunk) => {
          responseData += chunk;
      });

      soapRes.on('end', () => {
          // Aquí se procesa la respuesta SOAP
          const errores = parseSoapResponse(responseData);
          fs.unlink(csvFilePath, (err) => {
              if (err) {
                  console.error(`Error al eliminar el archivo: ${err}`);
              } else {
                  console.log(`Archivo ${csvFilePath} eliminado exitosamente.`);
              }
          });

          // Devolver los errores al navegador
          if (errores.length > 0) {
              return res.status(400).json({ errores }); // Enviar errores como respuesta JSON
          } else {
              return res.status(200).json({ mensaje: 'Archivo procesado correctamente.' });
          }
      });
  });

  soapRequest.on('error', (error) => {
      console.error(`Error en la solicitud SOAP: ${error.message}`);
      res.status(500).send('Error en el servidor.');
  });

  console.log("Te envio el xml EN LOTES");
  soapRequest.write(mensajeXml); // Enviamos el cuerpo SOAP.
  soapRequest.end();
});

// Función para parsear la respuesta SOAP
function parseSoapResponse(soapResponse) {
  const start = soapResponse.indexOf('<errores>') + '<errores>'.length;
  const end = soapResponse.indexOf('</errores>');
  const erroresXml = soapResponse.substring(start, end);
  
  // Extraer los mensajes de error en un arreglo
  const errores = [];
  const errorMatches = erroresXml.match(/<error>(.*?)<\/error>/g);
  if (errorMatches) {
      errorMatches.forEach((error) => {
          errores.push(error.replace(/<\/?error>/g, ''));
      });
  }
  return errores;
}


// LOGIN
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/html', 'login.html'));
});

app.post('/login', usuarioController.iniciarSesion);

// HOME
app.get('/home', (req, res) => {
  if (req.session.authenticated) {
    const usuario = encodeURIComponent(req.session.usuario);
    res.redirect(`/html/home.html?usuario=${usuario}`);
  } else {
    res.redirect('/');
  }
});

// USUARIO
app.get('/crearUsuario', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/usuarios', 'crearUsuario.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearUsuario', usuarioController.crearUsuario);

app.get('/logout', usuarioController.cerrarSesion);

app.get('/usuarios', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/usuarios', 'usuarios.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/usuarios', usuarioController.traerUsuarios);

app.get('/usuario/:idUsuario', usuarioController.mostrarUsuario);

app.get('/modificarUsuario', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public/html/usuarios', 'modificarUsuario.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/modificarUsuario', usuarioController.modificarUsuario);

app.post('/eliminarUsuario', usuarioController.eliminarUsuario);

app.get('/api/usuarios/filtrados', usuarioController.traerUsuariosFiltrados);

app.get('/obtenerUsuarioActual', usuarioController.obtenerUsuarioActual);

// TIENDA

app.get('/crearTienda', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/tiendas', 'crearTienda.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearTienda', tiendaController.crearTienda);

app.get('/crearCatalogo', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/catalogo', 'crearCatalogo.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearCatalogo', catalogoController.crearCatalogo);

app.get('/catalogos', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/catalogo', 'catalogos.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/tiendas', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/tiendas', 'tiendas.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/tiendas', tiendaController.traerTiendas);

app.get('/tienda/:idTienda', tiendaController.mostrarTienda);

app.get('/modificarTienda', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public/html/tiendas', 'modificarTienda.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/modificarTienda', tiendaController.modificarTienda);

app.post('/eliminarTienda', tiendaController.eliminarTienda);

app.get('/api/tiendas/filtradas', tiendaController.traerTiendasFiltradas);

app.get('/obtenerTiendaActual', tiendaController.obtenerTiendaActual);

// PRODUCTO
app.get('/crearProducto', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/productos', 'crearProducto.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearProducto', productoController.crearProducto);

app.get('/productos', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/productos', 'productos.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/productos', productoController.traerProductos);

app.get('/producto/:idProducto/:talle', productoController.mostrarProducto);

app.get('/modificarProducto', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public/html/productos', 'modificarProducto.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/modificarProducto', productoController.modificarProducto);

app.post('/eliminarProducto', productoController.eliminarProducto);

app.get('/agregarTalle', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public/html/productos', 'agregarTalle.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/agregarTalle', productoController.agregarTalle);

app.get('/api/productos/filtrados', productoController.traerProductosFiltrados);

// STOCK
app.get('/stock', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html', 'stock.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/stock', productoController.traerStock);

app.get('/api/stock/filtrado', productoController.traerStockFiltrado);

app.post('/agregarStock', productoController.agregarStock);


// ORDEN COMPRA
app.get('/crearOrden', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/ordenes', 'crearOrden.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearOrden', ordenCompraController.crearOrdenCompra);

app.get('/ordenes', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/ordenes', 'ordenes.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/informeOrdenes', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/ordenes', 'informeOrdenes.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/ordenesCasaCentral', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/ordenes', 'ordenesCasaCentral.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/ordenes', ordenCompraController.traerOrdenes);

app.post('/modificarOrden', ordenCompraController.modificarOrdenCompra);

app.post('/eliminarOrden', ordenCompraController.eliminarOrdenCompra);

// NOVEDADES
app.post('/agregarNovedad', novedadesController.agregarNovedad);

app.get('/novedades', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public/html/novedades', 'novedades.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/novedades', novedadesController.traerNovedades);

app.post('/eliminarNovedad', novedadesController.eliminarNovedad);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor web ejecutándose en http://localhost:${PORT}`);
});
