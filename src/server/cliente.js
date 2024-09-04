const express = require('express');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const bodyParser = require('body-parser');

// Cargar el archivo .proto
const PROTO_PATH = '../protos/testgrpc.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});
const testgrpc = grpc.loadPackageDefinition(packageDefinition).testgrpc;

// Crear el cliente gRPC
const client = new testgrpc.Propio('localhost:50051', grpc.credentials.createInsecure());

// Crear la aplicación Express
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// Servir el formulario en la ruta principal
app.get('/', (req, res) => {
    res.send(`
        <form action="/login" method="POST">
            <label for="name">Nombre:</label>
            <input type="text" id="name" name="name" required><br><br>
            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Enviar</button>
        </form>
    `);
});

// Ruta para manejar el envío del formulario
app.post('/login', (req, res) => {
    const { name, password } = req.body;

    // Llamar al método gRPC con los datos del formulario
    client.Imprimi({ cualEsNombre: name, cualEsPassword: password }, (error, response) => {
        if (error) {
            res.status(500).send('Error al comunicarse con el servidor gRPC.');
        } else {
            res.send(`¿Se imprimió el nombre?: ${response.yaLoImprimio}`);
        }
    });
});

// Iniciar el servidor Express
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor web ejecutándose en http://localhost:${PORT}`);
});
