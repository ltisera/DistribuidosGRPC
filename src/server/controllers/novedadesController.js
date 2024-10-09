const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH_NOVEDADES = path.join(__dirname, '..', '..', 'protos', 'novedades.proto');
const PROTO_PATH_PRODUCTO = path.join(__dirname, '..', '..', 'protos', 'producto.proto');

// Cargar el proto de novedades
const packageDefinitionNovedades = protoLoader.loadSync(PROTO_PATH_NOVEDADES, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });
  
const novedadProto = grpc.loadPackageDefinition(packageDefinitionNovedades).novedades;
  
// Crear el cliente gRPC para novedades
const clientNovedades = new novedadProto.Novedades('localhost:50051', grpc.credentials.createInsecure());

// Cargar el proto de productos
const packageDefinitionProducto = protoLoader.loadSync(PROTO_PATH_PRODUCTO, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });
  
const productoProto = grpc.loadPackageDefinition(packageDefinitionProducto).producto;
  
// Crear el cliente gRPC para productos
const clientProducto = new productoProto.Producto('localhost:50051', grpc.credentials.createInsecure());

// AGREGAR NOVEDAD
function agregarNovedad(req, res) {
  if (req.session.authenticated) {
    const { url, codigo, nombre, talle, color } = req.body;

    const idTienda = req.session.idTienda
    console.log(idTienda)

    agregarProductoNovedad(url, codigo, nombre, talle, color, parseInt(idTienda, 10))
    .then(response => {
        if (response  === '-1') {
          res.status(400).send("La tienda no existe")
        } else{
          res.redirect('/novedades?mensaje=successAddNovedad')
        } 
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar novedad');
      });
  } else {
    res.redirect('/');
  }
}

// ELIMINAR NOVEDAD
function eliminarNovedad(req, res) {
    if (req.session.authenticated) {
      const { codigo } = req.body;
      clientNovedades.EliminarNovedad({ codigo }, (error, response) => {
          if (error) {
              console.error('Error al eliminar novedad:', error);
              res.status(500).send('Error al eliminar novedad');
          } else {
            res.redirect('/novedades?mensaje=successDeleteNovedad');
          }
      });
    } else {
      res.redirect('/');
    }
  }

// TRAER NOVEDADES
function traerNovedades(req, res) {
  if (req.session.authenticated) {
    clientNovedades.TraerTodasLasNovedades({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodasLasNovedades: ' + error.message);
        return res.status(400).send('Error al traer novedades');
      }
      try {
        if (response && response.novedadList && response.novedadList.novedades) {
          const novedades = response.novedadList.novedades.map(novedad => ({
            codigo: novedad.codigo,
            url: novedad.url,
            nombre: novedad.nombre,
            talle: novedad.talle,
            color: novedad.color,
          }));
          res.json(novedades);
        } else {
          console.error('Respuesta del servidor no contiene NovedadList.');
          res.status(400).send('Error en la respuesta del servidor');
        }
      } catch (e) {
        console.error('Error al procesar la respuesta:', e);
        res.status(500).send('Error al procesar la respuesta');
      }
    });
  } else {
    res.redirect('/');
  }
}

// AGREGAR NOVEDAD AUXILIAR
function agregarProductoNovedad(url, codigo, nombre, talle, color, idTienda) {
  return new Promise((resolve, reject) => {
    const nuevaNovedad = {
        idProducto: null,
        nombre: nombre,
        foto: url,
        color: color,
        codigo: codigo,
        habilitado: true,
        talle: talle,
    };
    const listaTiendas = [idTienda];
    const request = { productoGrpcDTO: nuevaNovedad, tiendas: listaTiendas};

    clientProducto.AgregarProducto(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarProducto: ' + error.message);
      } else {
        resolve(response.idUsuario);
      }
    });
  });
}

module.exports = {
    agregarNovedad,
    eliminarNovedad,
    traerNovedades,
};
