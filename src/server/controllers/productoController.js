const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', '..', 'protos', 'producto.proto'); // Asegúrate de tener el archivo correcto

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const productoProto = grpc.loadPackageDefinition(packageDefinition).producto;

// Crear el cliente gRPC
const client = new productoProto.Producto('localhost:50051', grpc.credentials.createInsecure());

// CREAR PRODUCTO
function crearProducto(req, res) {
  if (req.session.authenticated) {
    const { idProducto, nombre, foto, color, codigo } = req.body;

    agregarProducto(idProducto, nombre, foto, color, codigo)
      .then(() => {
        res.redirect('/productos?mensaje=successAddProducto');
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar producto');
      });
  } else {
    res.redirect('/');
  }
}

// OBTENER PRODUCTO
function mostrarProducto(req, res) {
  if (req.session.authenticated) {
    const { idProducto } = req.params;
    client.ObtenerProducto({ idProducto }, (error, response) => {
      if (error) {
        console.error('Error al obtener producto:', error);
        res.status(500).send('Error al obtener producto');
      } else if (response && response.productoGrpcDTO) {
        res.json(response.productoGrpcDTO);
      } else {
        res.status(404).send('Producto no encontrado');
      }
    });
  } else {
    res.redirect('/');
  }
}

// MODIFICAR PRODUCTO
function modificarProducto(req, res) {
  if (req.session.authenticated) {
    const { idProducto, nombre, foto, color, codigo } = req.body;

    const productoActualizar = {
      idProducto,
      nombre,
      foto,
      color,
      codigo
    };
    
    client.ModificarProducto({ productoGrpcDTO: productoActualizar }, (error, response) => {
      if (error) {
        console.error('Error al modificar producto:', error);
        res.status(500).send('Error al modificar producto');
      } else {
        if (response.idProducto === '0') {
          res.status(400).send("El código del producto ya existe");
        } else {
          res.redirect('/productos?mensaje=successModifyProduct');
        }
      }
    });
  } else {
    res.redirect('/');
  }
}

// ELIMINAR PRODUCTO
function eliminarProducto(req, res) {
  if (req.session.authenticated) {
    const { idProducto } = req.body;
    client.EliminarProducto({ idProducto }, (error, response) => {
      if (error) {
        console.error('Error al eliminar producto:', error);
        res.status(500).send('Error al eliminar producto');
      } else {
        res.redirect('/productos?mensaje=successDeleteProduct');
      }
    });
  } else {
    res.redirect('/');
  }
}

// TRAER PRODUCTOS
function traerProductos(req, res) {
  if (req.session.authenticated) {
    client.TraerTodosLosProductos({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodosLosProductos: ' + error.message);
        return res.status(400).send('Error al traer productos');
      }
      try {
        if (response && response.productoList && response.productoList.productos) {
          const productos = response.productoList.productos.map(producto => ({
            idProducto: producto.idProducto,
            nombre: producto.nombre,
            foto: producto.foto,
            color: producto.color,
            codigo: producto.codigo
          }));
          res.json(productos);
        } else {
          console.error('Respuesta del servidor no contiene ProductoList.');
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

// TRAER PRODUCTOS FILTRADOS
function traerProductosFiltrados(req, res) {
  if (req.session.authenticated) {
    let { idProducto, estado } = req.query;
    if (!idProducto) {
        idProducto != -1;
    }
    client.TraerTodosLosProductosFiltrados({ codigo, estado }, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodosLosProductosFiltrados: ' + error.message);
        return res.status(400).send('Error al traer productos');
      }
      try {
        if (response && response.productoList && response.productoList.productos) {
          const productos = response.productoList.productos.map(producto => ({
            idProducto: producto.idProducto,
            nombre: producto.nombre,
            foto: producto.foto,
            color: producto.color,
            codigo: producto.codigo
          }));
          res.json(productos);
        } else {
          console.error('Respuesta del servidor no contiene ProductoList.');
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

// AGREGAR PRODUCTO AUXILIAR
function agregarProducto(idProducto, nombre, foto, color, codigo) {
  return new Promise((resolve, reject) => {
    const nuevoProducto = {
      idProducto,
      nombre,
      foto,
      color,
      codigo
    };

    const request = { productoGrpcDTO: nuevoProducto };

    client.AgregarProducto(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarProducto: ' + error.message);
      } else {
        console.log('Respuesta:', response);
        resolve(response.codigo);
      }
    });
  });
}

module.exports = {
  crearProducto,
  mostrarProducto,
  modificarProducto,
  traerProductos,
  eliminarProducto,
  traerProductosFiltrados
};
