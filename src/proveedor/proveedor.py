import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from DAO.productoDAO import ProductoDAO
import mysql.connector

from confluent_kafka import Producer

# Configuración del productor de Kafka
conf = {
    'bootstrap.servers': 'localhost:29092',  # Dirección del servidor Kafka
    'client.id': 'python-producer'
}

# Crear el productor
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print('Error al enviar el mensaje: {}'.format(err))
    else:
        print('Mensaje enviado a {} [{}]'.format(msg.topic(), msg.partition()))

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
        for talle_data in talles:
            talle = talle_data['talle']
            for color_data in talle_data['colores']:
                color = color_data['color']
                cantidad = int(color_data['cantidad'])
                idProducto = pdao.agregarProducto(nombre, foto, color, talle, cantidad)
        if idProducto:
            tallesNovedades = [
                {
                    'talle': talle_data['talle'],
                    'colores': [color_data['color'] for color_data in talle_data['colores']]
                }
                for talle_data in talles
            ]

            mensaje = {
                'idProducto': idProducto,
                'talles': tallesNovedades,
                'url': foto,
            }
            producer.produce('novedades', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
            producer.flush()

            return jsonify({'message': 'Producto agregado exitosamente', 'id': idProducto}), 201
        else:
            return jsonify({'error': 'No se pudo agregar el producto'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

if __name__ == '__main__':
    app.run(port=5000)
