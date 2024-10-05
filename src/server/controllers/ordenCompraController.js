const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', '..', 'protos', 'ordenCompra.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const ordenProto = grpc.loadPackageDefinition(packageDefinition).ordenCompra;

// Crear el cliente gRPC
const client = new ordenProto.OrdenCompra('localhost:50051', grpc.credentials.createInsecure());

// CREAR ORDEN COMPRA
function crearOrdenCompra(req, res) {
  if (req.session.authenticated) {
    const { idStock, cantidad } = req.body;

    agregarOrdenCompra(idStock, cantidad)
    .then(response => {
        if (response  === '-1') {
          res.status(400).send("El producto a solicitar no existe")
        } else{
          res.redirect('/ordenes?mensaje=successAddOrden')
        } 
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar orden de compra');
      });
  } else {
    res.redirect('/');
  }
}

// MODIFICAR ORDEN COMPRA
function modificarOrdenCompra(req, res) {
  if (req.session.authenticated) {
    const { ordenId } = req.body;

    const OrdenActualizar = {
        idOrdenDeCompra: parseInt(ordenId, 10),
        idStock: null,
        cantidad: null,
        estado: null,
        observaciones: null,
        fechaSolicitud: null,
        fechaRecepcion: null,
        ordenDeDespacho: null
    };
    client.ModificarOrden({ ordenCompraGrpcDTO: OrdenActualizar }, (error, response) => {
        if (error) {
            console.error('Error al modificar orden de compra:', error);
            return res.status(500).send('Error al modificar orden de compra');
        } else if (response.idOrdenDeCompra  == '0') {
            return res.send('failureModifyOrden');
        } else {
            return res.send('successModifyOrden');
        }
    });
  } else {
    res.redirect('/');
  }
}

// ELIMINAR ORDEN COMPRA
function eliminarOrdenCompra(req, res) {
  if (req.session.authenticated) {
    const { ordenId } = req.body;
    const idOrdenDeCompra =  parseInt(ordenId, 10)
    client.EliminarOrden({ idOrdenDeCompra }, (error, response) => {
        if (error) {
            console.error('Error al eliminar orden de compra:', error);
            res.status(500).send('Error al eliminar orden de compra');
        } else {
          res.redirect('/ordenes?mensaje=successDeleteOrden');
        }
    });
  } else {
    res.redirect('/');
  }
}

// TRAER ORDENES COMPRA
function traerOrdenes(req, res) {
  if (req.session.authenticated) {
    client.TraerTodasLasOrdenes({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodasLasOrdenes: ' + error.message);
        return res.status(400).send('Error al traer ordenes');
      }
      try {
        if (response && response.ordenList && response.ordenList.ordenes) {
          const ordenes = response.ordenList.ordenes.map(orden => ({
            idOrdenDeCompra: orden.idOrdenDeCompra,
            idStock: orden.idStock,
            cantidad: orden.cantidad,
            estado: orden.estado,
            observaciones: orden.observaciones,
            fechaSolicitud: orden.fechaSolicitud,
            fechaRecepcion: orden.fechaRecepcion,
            ordenDeDespacho: orden.ordenDeDespacho
          }));
          res.json(ordenes);
        } else {
          console.error('Respuesta del servidor no contiene OrdenCompraList.');
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

// AGREGAR ORDEN COMPRA AUXILIAR
function agregarOrdenCompra(idStock, cantidad) {
  return new Promise((resolve, reject) => {
    const nuevaOrden = {
      idStock: idStock,
      cantidad: cantidad,
      estado: null,
      observaciones: null,
      fechaSolicitud: null,
      fechaRecepcion: null,
      ordenDeDespacho: null
    };
    
    const request = { ordenCompraGrpcDTO: nuevaOrden };

    client.AgregarOrden(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarOrdenCompra: ' + error.message);
      } else {
        resolve(response.idOrdenDeCompra);
      }
    });
  });
}

module.exports = {
  crearOrdenCompra,
  traerOrdenes,
  modificarOrdenCompra,
  eliminarOrdenCompra,
};
