import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

from DAO.tiendaDAO import TiendaDAO
from DAO.ordenCompraDAO import OrdenCompraDAO
from DAO.novedadesDAO import NovedadesDAO

# CONSUMIDOR
consumer_conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)

# SUBSCRIBIRSE A LOS TOPICOS
def actualizar_subscripciones():
    crear_topicos()
    tdao = TiendaDAO()
    tiendas = tdao.traerTodasLasTiendas()
    topics = []
    topics.append("novedades")
    topics += [f"{tienda[0]}-solicitudes" for tienda in tiendas]
    topics += [f"{tienda[0]}-despacho" for tienda in tiendas]
    
    consumer.subscribe(topics)

    print("Suscrito a los siguientes tópicos:")
    for topic in topics:
        print(topic)

# CREAR TOPICOS                       
def crear_topicos():
    admin_client = AdminClient({'bootstrap.servers': 'localhost:29092'})

    tdao = TiendaDAO()
    tiendas = tdao.traerTodasLasTiendas()
    topics = []
    topics.append(f"novedades")
    for tienda in tiendas:
        id_tienda = tienda[0]
        topics.append(f"{id_tienda}-solicitudes")
        topics.append(f"{id_tienda}-despacho")

    existing_topics = admin_client.list_topics().topics.keys()

    if "novedades" in existing_topics:
        print("El tópico 'novedades' ya existe.")
    else:
        print("El tópico 'novedades' no existe y será creado.")

    new_topics = []
    for topic in topics:
        if topic not in existing_topics:
            new_topics.append(NewTopic(topic, num_partitions=1, replication_factor=1))

    if new_topics:
        fs = admin_client.create_topics(new_topics)
        for topic, f in fs.items():
            try:
                f.result()
                print(f'Tópico {topic} creado con éxito.')
            except Exception as e:
                print(f'Error al crear el tópico {topic}: {e}')
    else:
        print("Todos los tópicos ya existen. No se crearon nuevos.")

# CONSUMIR MENSAJES
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
            if msg.topic().endswith('-solicitudes'):
                procesar_solicitud(data)
            elif msg.topic().endswith('-despacho'):
                procesar_despacho(data)
            elif msg.topic().endswith('novedades'):
                procesar_novedades(data)

# PROCESAR TOPICO SOLICITUD
def procesar_solicitud(data):
    estado = data.get('estado')
    idOrden = data.get('idOrden')
    observaciones = data.get('observaciones')

    odao = OrdenCompraDAO()
    odao.actualizarOrdenCompra(idOrden, estado, observaciones)

# PROCESAR TOPICO DESPACHO
def procesar_despacho(data):
    idOrdenDespacho = data.get('idOrdenDespacho')
    idOrden = data.get('idOrden')
    odao = OrdenCompraDAO()
    odao.agregarDespachoAOrdenCompra(idOrden, idOrdenDespacho)

# PROCESAR TOPICO NOVEDADES
def procesar_novedades(data):
    try:
        nombre = data.get('nombre')
        talles = data.get('talles')
        url = data.get('url')


        for talle_data in talles:
            talle = talle_data.get('talle')
            color = talle_data.get('color')
            codigo = talle_data.get('codigo')
            ndao = NovedadesDAO()
            ndao.agregarNovedad(codigo, nombre, talle, color, url)
    except Exception as e:
        print(f"Error al procesar novedades: {str(e)}")