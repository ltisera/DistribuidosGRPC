const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', '..', 'protos', 'tienda.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const tiendaProto = grpc.loadPackageDefinition(packageDefinition).tienda;

// Crear el cliente gRPC
const client = new tiendaProto.Tienda('localhost:50051', grpc.credentials.createInsecure());

// CREAR TIENDA
function crearTienda(req, res) {
  if (req.session.authenticated) {
    const { idTienda, direccion, ciudad, provincia, habilitado} = req.body;
    const habilitadoBool = (habilitado == "true");

    agregarTienda(idTienda, direccion, ciudad, provincia, habilitadoBool)
    .then(() => {
        res.redirect('/tiendas?mensaje=successAddTienda')
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar tienda');
      });
  } else {
    res.redirect('/');
  }
}

// OBETENER TIENDA
function mostrarTienda(req, res) {
  if (req.session.authenticated) {
    const { idTienda } = req.params;
    client.ObtenerTienda({ idTienda: parseInt(idTienda, 10) }, (error, response) => {
        if (error) {
            console.error('Error al obtener tienda:', error);
            res.status(500).send('Error al obtener tienda');
        } else if (response && response.tiendaGrpcDTO) {
            res.json(response.tiendaGrpcDTO);
        } else {
            res.status(404).send('Tienda no encontrada');
        }
    });
  } else {
    res.redirect('/');
  }
}

// MODIFICAR TIENDA
function modificarTienda(req, res) {
  if (req.session.authenticated) {
    const { idTienda, direccion, ciudad, provincia, habilitado} = req.body;

    const tiendaActualizar = {
        idTienda: parseInt(idTienda, 10),
        direccion,
        ciudad,
        provincia,
        habilitado: habilitado === 'true',
    };
    client.ModificarTienda({ tiendaGrpcDTO: tiendaActualizar }, (error, response) => {
        if (error) {
          console.error('Error al modificar tienda:', error);
          res.status(500).send('Error al modificar tienda');
        } else {
          if (response.idTienda  === '0') {
            res.status(400).send("El codigo de tienda ya existe")
          } else{
            res.redirect('/usuarios?mensaje=successModifyTienda');
          }
        }
    });
  } else {
    res.redirect('/');
  }
}

// ELIMINAR TIENDA
function eliminarTienda(req, res) {
  if (req.session.authenticated) {
    const { idTienda } = req.body;
    const idTiendaDelete =  parseInt(idTienda, 10)
    client.EliminarTienda({ idTiendaDelete }, (error, response) => {
        if (error) {
            console.error('Error al eliminar tienda:', error);
            res.status(500).send('Error al eliminar tienda');
        } else {
          res.redirect('/tiendas?mensaje=successDeleteTienda');
        }
    });
  } else {
    res.redirect('/');
  }
}

// TRAER TIENDAS
function traerTiendas(req, res) {
  if (req.session.authenticated) {
    client.TraerTodasLasTiendas({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodasLasTiendas: ' + error.message);
        return res.status(400).send('Error al traer tiendas');
      }
      try {
        if (response && response.tiendaList && response.tiendaList.tiendas) {
          const tiendas = response.tiendaList.tiendas.map(tienda => ({
            idTienda: tienda.idTienda,
            direccion: tienda.direccion,
            ciudad: tienda.ciudad,
            provincia: tienda.provincia,
            habilitado: tienda.habilitado
          }));
          res.json(tiendas);
        } else {
          console.error('Respuesta del servidor no contiene TiendaList.');
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

// TRAER TIENDAS FILTRADOS
function traerTiendasFiltradas(req, res) {
  if (req.session.authenticated) {
    let {idTienda, estado} = req.query
    if(!idTienda){
      idTienda = -1
    }
    client.TraerTodasLasTiendasFiltradas({idTienda, estado}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodasLasTiendasFiltradas: ' + error.message);
        return res.status(400).send('Error al traer tiendas');
      }
      try {
        if (response && response.tiendaList && response.tiendaList.tiendas) {
          const tiendas = response.tiendaList.tiendas.map(tienda => ({
            idTienda: tienda.idTienda,
            direccion: tienda.direccion,
            ciudad: tienda.ciudad,
            provincia: tienda.provincia,
            habilitado: tienda.habilitado
          }));
          res.json(tiendas);
        } else {
          console.error('Respuesta del servidor no contiene TiendaList.');
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

// AGREGAR TIENDA AUXILIAR
function agregarTienda(idTienda, direccion, ciudad, provincia, habilitado) {
  return new Promise((resolve, reject) => {
    const nuevaTienda = {
        idTienda: idTienda,
        direccion: direccion,
        ciudad: ciudad,
        provincia: provincia,
        habilitado: habilitado
    };

    const request = { tiendaGrpcDTO: nuevaTienda };

    client.AgregarTienda(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarTienda: ' + error.message);
      } else {
        resolve(response.idTienda);
      }
    });
  });
}

module.exports = {
  crearTienda,
  mostrarTienda,
  modificarTienda,
  traerTiendas,
  eliminarTienda,
  traerTiendasFiltradas
};
