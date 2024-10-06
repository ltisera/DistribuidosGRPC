from datetime import datetime
import os, sys

import mysql.connector
import json
from mysql.connector import Error
from settings.conexionDB import ConexionBD

from confluent_kafka import Producer

from DAO.stockDAO import StockDAO

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

class OrdenCompraDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarOrdenCompra(self, idTienda, idOrden, idStock, cantidad, fechaSolicitud):
        try:
            self.crearConexion()

            estado = "SOLICITADA"
            ordenDeDespacho = None
            fechaSolicitud = int(datetime.now().timestamp() * 1000)
            fechaRecepcion = None
            observaciones = None
            sql = ("INSERT INTO ordendecompra (idStock, cantidad, estado, observaciones, fechaSolicitud, fechaRecepcion, ordenDeDespacho) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            values = (idStock, cantidad, estado, observaciones, fechaSolicitud, fechaRecepcion, ordenDeDespacho)
            print(values) 
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Orden de compra agregada con éxito.")

            idOrden = self._micur.lastrowid 

            check_sql = "SELECT tienda FROM stock WHERE idStock = %s"
            self._micur.execute(check_sql, (idStock,))
            resultado = self._micur.fetchone()

            if resultado is None:
                print("No se encontró la tienda para el idStock proporcionado.")
                return None
        
            idTienda = resultado[0]

            mensaje = {
                'idTienda': idTienda,
                'idOrdenDeCompra': idOrden,
                'idStock': idStock,
                'cantidad': cantidad,
                'fechaSolicitud': fechaSolicitud
            }

            producer.produce('orden-de-compra', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)

            producer.flush()

            return idOrden
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None

    def modificarOrdenCompra(self, idOrdenCompra):
        try:
            self.crearConexion()

            check_sql = "SELECT estado, ordenDeDespacho, cantidad, idStock FROM ordendecompra WHERE idOrdenDeCompra = %s"
            self._micur.execute(check_sql, (idOrdenCompra,))
            resultado = self._micur.fetchone()

            if resultado is None:
                print("Orden de compra no encontrada.")
                return None
            
            estado, ordenDeDespacho, cantidad, idStock = resultado

            if estado != "ACEPTADA":
                print("La orden no se puede modificar porque no está en estado 'ACEPTADA'.")
                return 0
            
            if not ordenDeDespacho:
                print("La orden no se puede modificar porque el campo 'ordenDeDespacho' está vacío.")
                return 0

            estado = "RECIBIDA"
            fechaRecepcion = int(datetime.now().timestamp() * 1000)

            sql = ("UPDATE ordendecompra SET estado = %s, fechaRecepcion = %s WHERE idOrdenDeCompra = %s")
            values = (estado, fechaRecepcion, idOrdenCompra)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Orden de compra actualizada con éxito.")

            mensaje = {
                'ordenDeDespacho': ordenDeDespacho,
                'fechaRecepcion': fechaRecepcion,
            }

            producer.produce('recepcion', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)

            producer.flush()

            sdao = StockDAO()
            sdao.modificarStock(idStock, cantidad)

            return idOrdenCompra
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
            return None
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return None
        finally:
            self.cerrarConexion()
    
if __name__ == '__main__':
    a = OrdenCompraDAO()