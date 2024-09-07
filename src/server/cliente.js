const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

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

app.get('/', (req, res) => {
  res.send(`
    <form action="/login" method="POST">
        <label for="usuario">Usuario:</label>
        <input type="text" id="usuario" name="usuario" required><br><br>

        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required><br><br>
        
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre" required><br><br>

        <label for="apellido">Apellido:</label>
        <input type="text" id="apellido" name="apellido" required><br><br>

        <label for="habilitado">Habilitado:</label>
        <input type="checkbox" id="habilitado" name="habilitado"><br><br>

        <label for="casaCentral">Casa Central:</label>
        <input type="checkbox" id="casaCentral" name="casaCentral"><br><br>
        
        <label for="idTienda">Id Tienda:</label>
        <input type="text" id="idTienda" name="idTienda" required><br><br>

        <button type="submit">Enviar</button>
    </form>
  `);
});

app.post('/login', (req, res) => {
  const { usuario, password, nombre, apellido, habilitado, casaCentral, idTienda } = req.body;

  // Convert boolean values from checkbox inputs
  const habilitadoBool = habilitado === 'on';
  const casaCentralBool = casaCentral === 'on';

  agregarUsuario(usuario, password, nombre, apellido, habilitadoBool, casaCentralBool, parseInt(idTienda, 10))
    .then(() => res.send('Usuario agregado con éxito'))
      .catch((error) => {
        console.error('Error:', error);
        res.status(500).send('Error al agregar usuario');
      });
});

// Función para llamar al método AgregarUsuario
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
