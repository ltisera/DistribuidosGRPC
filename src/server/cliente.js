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

const multer = require('multer');
const csvParser = require('csv-parser');
const fs = require('fs');

const upload = multer({ dest: 'uploads/' });

app.post('/cargarCSV', upload.single('csvFile'), async (req, res) => {
    if (!req.file) {
        return res.status(400).send('No se ha proporcionado ningún archivo.');
    }

    try {
        // Leer el archivo CSV
        const csvFilePath = req.file.path;
        const fileData = fs.readFileSync(csvFilePath, 'utf8');
        
        const xml = `
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <procesarCSV>
                        <archivo>${fileData}</archivo>
                        <nombre>${req.file.originalname}</nombre>
                    </procesarCSV>
                </soap:Body>
            </soap:Envelope>
        `;

        // Enviar la solicitud SOAP
        console.log(xml)
        const response = await fetch('http://127.0.0.1:6000/procesarCSV', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml;charset=UTF-8',
                'SOAPAction': 'http://127.0.0.1:6000/procesarCSV' // Cambia esto según lo que espera el servicio
            },
            body: xml
        });

        // Manejar la respuesta
        const responseText = await response.text();
        fs.unlinkSync(csvFilePath); // Eliminar el archivo temporal

        if (!response.ok) {
            console.error('Error en la respuesta del servidor SOAP:', responseText);
            return res.status(500).send('Error al procesar el archivo con el servicio SOAP.');
        }

        console.log('Respuesta del servidor SOAP:', responseText);
        res.send('Archivo CSV enviado exitosamente.');
    } catch (error) {
        console.error('Error al enviar la solicitud SOAP:', error);
        res.status(500).send('Error al procesar la solicitud.');
    }
});




// LOGIN
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/login', usuarioController.iniciarSesion);

//
app.get('/tst', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'proveedorTest.html'));
});

// HOME
app.get('/home', (req, res) => {
  if (req.session.authenticated) {
    const usuario = encodeURIComponent(req.session.usuario);
    res.redirect(`/home.html?usuario=${usuario}`);
  } else {
    res.redirect('/');
  }
});

// USUARIO
app.get('/crearUsuario', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'crearUsuario.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearUsuario', usuarioController.crearUsuario);

app.get('/logout', usuarioController.cerrarSesion);

app.get('/usuarios', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'usuarios.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/usuarios', usuarioController.traerUsuarios);

app.get('/usuario/:idUsuario', usuarioController.mostrarUsuario);

app.get('/modificarUsuario', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public', 'modificarUsuario.html'));
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
    res.sendFile(path.join(__dirname, 'public', 'crearTienda.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearTienda', tiendaController.crearTienda);

app.get('/crearCatalogo', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'crearCatalogo.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearCatalogo', catalogoController.crearCatalogo);

app.get('/catalogos', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'catalogos.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/tiendas', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'tiendas.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/tiendas', tiendaController.traerTiendas);

app.get('/tienda/:idTienda', tiendaController.mostrarTienda);

app.get('/modificarTienda', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public', 'modificarTienda.html'));
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
    res.sendFile(path.join(__dirname, 'public', 'crearProducto.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearProducto', productoController.crearProducto);

app.get('/productos', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'productos.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/productos', productoController.traerProductos);

app.get('/producto/:idProducto/:talle', productoController.mostrarProducto);

app.get('/modificarProducto', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public', 'modificarProducto.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/modificarProducto', productoController.modificarProducto);

app.post('/eliminarProducto', productoController.eliminarProducto);

app.get('/agregarTalle', (req, res) => {
  if (req.session.authenticated) {
      res.sendFile(path.join(__dirname, 'public', 'agregarTalle.html'));
  } else {
      res.redirect('/');
  }
});

app.post('/agregarTalle', productoController.agregarTalle);

app.get('/api/productos/filtrados', productoController.traerProductosFiltrados);

// STOCK

app.get('/stock', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'stock.html'));
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
    res.sendFile(path.join(__dirname, 'public', 'crearOrden.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearOrden', ordenCompraController.crearOrdenCompra);

app.get('/ordenes', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'ordenes.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/informeOrdenes', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'informeOrdenes.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/ordenesCasaCentral', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'ordenesCasaCentral.html'));
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
    res.sendFile(path.join(__dirname, 'public', 'novedades.html'));
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
