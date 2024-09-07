const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const session = require('express-session');

const PROTO_PATH = path.join(__dirname, '..', 'protos', 'usuario.proto');

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

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
  secret: 'tp-grpc', // Cambia esto por una cadena segura en producción
  resave: false,
  saveUninitialized: true,
}));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/home', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

app.post('/login', (req, res) => {
  const { usuario, password } = req.body;
  
  console.log(`Enviando solicitud con usuario='${usuario}' y contraseña='${password}'`);

  client.IniciarSesion({ usuario, password }, (error, response) => {
    if (error) {
      console.error(error);
      res.send('Error en la solicitud');
    } else if (response.exito) {
      req.session.authenticated = true;
      req.session.usuario = usuario;
      res.redirect('/home');
    } else {
      res.send('Usuario o contraseña incorrectos');
    }
  });
});

app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
      res.send('Error al cerrar sesión');
    } else {
      res.redirect('/');
    }
  });
});

app.post('/crearUsuario', (req, res) => {
  if (req.session.authenticated) {
    const { usuario, password, nombre, apellido, casaCentral, idTienda } = req.body;
    const habilitadoBool = true
    const casaCentralBool = casaCentral === 'on';

    agregarUsuario(usuario, password, nombre, apellido, habilitadoBool, casaCentralBool, parseInt(idTienda, 10))
      .then(() => res.send('Usuario agregado con éxito'))
        .catch((error) => {
          console.error('Error:', error);
          res.status(500).send('Error al agregar usuario');
        });
  } else {
    res.redirect('/');
  }
});

app.get('/usuarios', (req, res) => {
  if (req.session.authenticated) {
    client.TraerTodosLosUsuarios({}, (error, response) => {
      if (error) {
        console.error('Error al llamar al método TraerTodosLosUsuarios: ' + error.message);
        return res.status(400).send('Error al traer usuarios');
      } 
      try {
        if (response && response.usuarioList && response.usuarioList.usuarios) {
          const usuarios = response.usuarioList.usuarios.map(usuario => ({
            usuario: usuario.usuario,
            tienda: usuario.idTienda,
            habilitado: usuario.habilitado
          }));
          console.log('Respuesta:', usuarios);
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
});

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
        resolve();
      }
    });
  });
}

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor web ejecutándose en http://localhost:${PORT}`);
});
