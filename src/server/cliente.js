const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Carga el archivo .proto
const PROTO_PATH = '../protos/testgrpc.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});
const testgrpc = grpc.loadPackageDefinition(packageDefinition).testgrpc;

// Crear el cliente
const client = new testgrpc.Propio('localhost:50051', grpc.credentials.createInsecure());

// Ejecutar la llamada al método Imprimi
client.Imprimi({ cualEsNombre: 'LucaS', cualEsApellido: 'Pérez' }, (error, response) => {
    if (!error) {
        console.log(`¿Se imprimió el nombre?: ${response.yaLoImprimio}`);
    } else {
        console.error(error);
    }
});
