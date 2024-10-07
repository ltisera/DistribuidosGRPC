import json
import random
import string
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from DAO.ordenCompraDAO import OrdenCompraDAO
from DAO.productoDAO import ProductoDAO

from confluent_kafka import Producer, Consumer, KafkaError

# Configuración del productor de Kafka
producer_conf = {
    'bootstrap.servers': 'localhost:29092',  # Dirección del servidor Kafka
    'client.id': 'python-producer'
}

# Crear el productor
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print('Error al enviar el mensaje: {}'.format(err))
    else:
        print('Mensaje enviado a {} [{}]'.format(msg.topic(), msg.partition()))

# Crear el consumidor
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['orden-de-compra', 'recepcion'])

from DAO.stockDAO import StockDAO

app = Flask(__name__, static_url_path='', static_folder='public')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')

@app.route('/api/producto', methods=['POST'])
def agregar_producto():
    data = request.json
    nombre = data.get('nombre')
    foto = data.get('foto')
    talles = data.get('talles')
    pdao = ProductoDAO()
    try:
        print("Talles: ", talles)
        tallesNovedades = []
        for talle_data in talles:
            talle = talle_data['talle']
            for color_data in talle_data['colores']:
                color = color_data['color']
                cantidad = int(color_data['cantidad'])
                codigo = generar_codigo_aleatorio()
                idProducto = pdao.agregarProducto(codigo, nombre, foto, color, talle, cantidad)
                tallesNovedades.append({
                    'talle': talle,
                    'color': color,
                    'codigo': codigo
                })
        if idProducto:
            mensaje = {
                'nombre': nombre,
                'talles': tallesNovedades,
                'url': foto,
            }
            producer.produce('novedades', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
            producer.flush()

            return jsonify({'message': 'Producto agregado exitosamente', 'codigo': codigo}), 201
        else:
            return jsonify({'error': 'No se pudo agregar el producto'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generar_codigo_aleatorio(length=10):
    caracteres = string.ascii_letters + string.digits  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    codigo = ''.join(random.choice(caracteres) for _ in range(length))
    return codigo

@app.route('/api/producto/<int:idStock>/cantidad', methods=['PUT'])
def modificar_cantidad(idStock):
    data = request.json
    cantidad = data.get('cantidad')

    sdao = StockDAO()
    try:
        result = sdao.modificarStock(idStock, cantidad)
        if result:
            return jsonify({'message': 'Cantidad actualizada con éxito'}), 200
        else:
            return jsonify({'error': 'No se pudo actualizar la cantidad'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    pdao = ProductoDAO()
    productos = pdao.traerTodosLosProductos()
    return jsonify(productos), 200

# KAFKA
def procesar_orden(data):
    print(f'Procesando orden de compra: {data}')
    id_tienda = data.get('idTienda')
    id_orden_de_compra = data.get('idOrdenDeCompra')
    codigo = data.get('codigo')
    cantidad = data.get('cantidad')
    fecha_solicitud = data.get('fechaSolicitud')
    idStock = data.get('idStock')

    odao = OrdenCompraDAO()
    odao.procesarOrdenCompra(id_tienda, id_orden_de_compra, idStock, codigo, cantidad, fecha_solicitud)

def procesar_recepcion(data):
    print(f'Procesando recepcion: {data}')
    fecha_recepcion = data.get('fechaRecepcion')
    orden_despacho = data.get('ordenDeDespacho')

    odao = OrdenCompraDAO()
    odao.procesarRecibo(orden_despacho, fecha_recepcion)

def consumir_mensajes():
    while True:
        msg = consumer.poll(1.0) 
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f'Error al consumir el mensaje: {msg.error()}')
                break
        else:
            data = json.loads(msg.value().decode('utf-8'))
            print(f'Mensaje recibido: {data}')

            if msg.topic() == 'orden-de-compra':
                procesar_orden(data)
            elif msg.topic() == 'recepcion':
                procesar_recepcion(data)

if __name__ == '__main__':
    import threading
    threading.Thread(target=consumir_mensajes, daemon=True).start()
    app.run(port=5000)
