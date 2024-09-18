const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', '..', 'protos', 'producto.proto');

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
    const { idProducto, nombre, foto, color, codigo, talle} = req.body;

    agregarProducto(idProducto, nombre, foto, color, codigo, talle)
    .then(() => {
        res.redirect('/productos?mensaje=succesAddProducto')
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar producto');
      });
    
  } else {
    res.redirect('/');
  }
}

// OBETENER PRODUCTO
function mostrarProducto(req, res) {
  if (req.session.authenticated) {
    const { idProducto } = req.params;
    client.ObtenerProducto({ idProducto: parseInt(idProducto, 10) }, (error, response) => {
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
    const {idProducto, nombre, foto, color, codigo} = req.body;

    const productoActualizar = {
        idProducto: parseInt(idProducto, 10),
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
          if (response.idProducto  === '0') {
            res.status(400).send("El codigo del producto ya existe")
          } else{
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
    const idProductoDelete =  parseInt(idProducto, 10)
    client.EliminarProducto({ idProductoDelete }, (error, response) => {
        if (error) {
            console.error('Error al eliminar producto:', error);
            res.status(500).send('Error al eliminar producto');
        } else {
          res.redirect('/productos?mensaje=successDeleteProducto');
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
            codigo: producto.codigo,
            talle: producto.talle
          }));
          res.json(productos);{}
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
    let {codigo, nombre, talle, color} = req.query
    client.TraerTodosLosProductosFiltrados({codigo, nombre, talle, color}, (error, response) => {
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
            codigo: producto.codigo,
            talle: producto.talle
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
function agregarProducto(idProducto, nombre, foto, color, codigo, talle) {
  return new Promise((resolve, reject) => {
    const nuevoProducto = {
        idProducto: idProducto,
        nombre: nombre,
        foto: foto,
        color: color,
        codigo: codigo,
        talle: talle
    };

    const request = { productoGrpcDTO: nuevoProducto };

    client.AgregarProducto(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarProducto: ' + error.message);
      } else {
        resolve(response.idProducto);
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
