# SISTEMAS DISTRIBUIDOS TP CUATRIMESTRAL
Entrega TP de sistemas distribuidos

### -Lenguajes a utilizar:
    -Python
    -NodeJS
### -Motor Base de datos:
    -MySQL Server 9.0.1
    
### Comandos ejecutados en el cmd:
    pip install mysql-connector-python grpcio-tools
    pip install Flask Flask-CORS confluent-kafka Pillow fpdf
    npm install @grpc/grpc-js @grpc/proto-loader express multer

    py compilaProto.py <--- Usar en caso de modificar el proto


### Para Ejecutar:
    docker-compose up -d (En la carpeta de kafka)
    py server.py
    py cliente.py
    py proveedor.py
    py serverCatalogos.py
    
    NOTA: Ejecutarlo en consolas diferentes

### Librerias Utilizadas:
    pyMSQL
    pyFlask
    Express
    Concurrent
    Grpcio
    Grpc-js
    ConfluentKafka
    Multer
    FPDF
    Pillow


bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties