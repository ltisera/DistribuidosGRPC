const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.join(__dirname, '..', '..', 'protos', 'usuario.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const usuarioProto = grpc.loadPackageDefinition(packageDefinition).usuario;

// Crear el cliente gRPC
const client = new usuarioProto.Usuario('localhost:50051', grpc.credentials.createInsecure());

// INICIAR SESION
function iniciarSesion(req, res) {
  const { usuario, password } = req.body;
  client.IniciarSesion({ usuario, password }, (error, response) => {
    if (error) {
      console.error(error);
      res.send('Error en la solicitud');
    } else if (response.idUsuario >= 0) {
      req.session.authenticated = true;
      req.session.usuario = usuario;
      req.session.idUsuario = response.idUsuario;
      req.session.tipoUsuario = "general";
      if (response.casaCentral){
        req.session.tipoUsuario = "casaCentral";
      }
      res.redirect('/home');
    } else {
        res.redirect('/?mensaje=sessionFailed');
    }
  });
}

// CERRAR SESION
function cerrarSesion(req, res) {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
      res.send('Error al cerrar sesión');
    } else {
      res.redirect('/');
    }
  });
}

// CREAR USUARIO
function crearUsuario(req, res) {
  if (req.session.authenticated) {
    const { usuario, password, nombre, apellido, casaCentral, idTienda } = req.body;
    const habilitadoBool = true;
    const casaCentralBool = casaCentral === 'on';

    agregarUsuario(usuario, password, nombre, apellido, habilitadoBool, casaCentralBool, parseInt(idTienda, 10))
    .then(response => {
        if (response  === '-1') {
          res.status(400).send("La tienda no existe")
        } else if (response  === '0') {
          res.status(400).send("El nombre de usuario ya existe")
        } else{
          res.redirect('/usuarios?mensaje=successAddUser')
        } 
      })
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar usuario');
      });
  } else {
    res.redirect('/');
  }
}

// OBETENER USUARIO
function mostrarUsuario(req, res) {
  if (req.session.authenticated) {
    const { idUsuario } = req.params;
    client.ObtenerUsuario({ idUsuario: parseInt(idUsuario, 10) }, (error, response) => {
        if (error) {
            console.error('Error al obtener usuario:', error);
            res.status(500).send('Error al obtener usuario');
        } else if (response && response.usuarioObtenerGrpcDTO) {
            res.json(response.usuarioObtenerGrpcDTO);
        } else {
            res.status(404).send('Usuario no encontrado');
        }
    });
  } else {
    res.redirect('/');
  }
}

// MODIFICAR USUARIO
function modificarUsuario(req, res) {
  if (req.session.authenticated) {
    const { userId, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda } = req.body;

    const usuarioActualizar = {
        idUsuario: parseInt(userId, 10),
        usuario,
        password,
        nombre,
        apellido,
        habilitado: habilitado === 'true',
        casaCentral: casaCentral === 'true',
        idTienda: parseInt(idTienda, 10)
    };
    client.ModificarUsuario({ usuarioObtenerGrpcDTO: usuarioActualizar }, (error, response) => {
        if (error) {
          console.error('Error al modificar usuario:', error);
          res.status(500).send('Error al modificar usuario');
        } else {
          if (response.idUsuario  === '0') {
            res.status(400).send("El nombre de usuario ya existe")
          } else{
            res.redirect('/usuarios?mensaje=successModifyUser');
          }
        }
    });
  } else {
    res.redirect('/');
  }
}

// ELIMINAR USUARIO
function eliminarUsuario(req, res) {
  if (req.session.authenticated) {
    const { userId } = req.body;
    const idUsuario =  parseInt(userId, 10)
    client.EliminarUsuario({ idUsuario }, (error, response) => {
        if (error) {
            console.error('Error al eliminar usuario:', error);
            res.status(500).send('Error al eliminar usuario');
        } else {
          res.redirect('/usuarios?mensaje=successDeleteUser');
        }
    });
  } else {
    res.redirect('/');
  }
}

// TRAER USUARIOS
function traerUsuarios(req, res) {
  if (req.session.authenticated) {
    client.TraerTodosLosUsuarios({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodosLosUsuarios: ' + error.message);
        return res.status(400).send('Error al traer usuarios');
      }
      try {
        if (response && response.usuarioList && response.usuarioList.usuarios) {
          const usuarios = response.usuarioList.usuarios.map(usuario => ({
            idUsuario: usuario.idUsuario,
            usuario: usuario.usuario,
            tienda: usuario.idTienda,
            habilitado: usuario.habilitado
          }));
          res.json(usuarios);
        } else {
          console.error('Respuesta del servidor no contiene UsuarioList.');
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

// TRAER USUARIOS FILTRADOS
function traerUsuariosFiltrados(req, res) {
  if (req.session.authenticated) {
    let {idTienda, nombre} = req.query
    if(!idTienda){
      idTienda = 0
    }
    if(!nombre){
      nombre = " "
    }
    client.TraerTodosLosUsuariosFiltrados({idTienda, nombre}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodosLosUsuariosFiltrados: ' + error.message);
        return res.status(400).send('Error al traer usuarios');
      }
      try {
        if (response && response.usuarioList && response.usuarioList.usuarios) {
          const usuarios = response.usuarioList.usuarios.map(usuario => ({
            idUsuario: usuario.idUsuario,
            usuario: usuario.usuario,
            tienda: usuario.idTienda,
            habilitado: usuario.habilitado
          }));
          res.json(usuarios);
        } else {
          console.error('Respuesta del servidor no contiene UsuarioList.');
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

// AGREGAR USUARIO AUXILIAR
function agregarUsuario(usuario, password, nombre, apellido, habilitado, casaCentral, idTienda) {
  return new Promise((resolve, reject) => {
    const nuevoUsuario = {
      usuario: usuario,
      password: password,
      nombre: nombre,
      apellido: apellido,
      habilitado: habilitado,
      casaCentral: casaCentral,
      idTienda: idTienda
    };

    const request = { usuarioGrpcDTO: nuevoUsuario };

    client.AgregarUsuario(request, (error, response) => {
      if (error) {
        reject('Error al llamar al método AgregarUsuario: ' + error.message);
      } else {
        console.log('Respuesta:', response);
        resolve(response.idUsuario);
      }
    });
  });
}

module.exports = {
  iniciarSesion,
  cerrarSesion,
  crearUsuario,
  traerUsuarios,
  mostrarUsuario,
  modificarUsuario,
  eliminarUsuario,
  traerUsuariosFiltrados
};
