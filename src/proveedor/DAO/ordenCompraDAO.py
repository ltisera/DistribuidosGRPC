from datetime import datetime
import os, sys

import mysql.connector
import json
from mysql.connector import Error
from DAO.ordenCompraAsociadaDAO import OrdenCompraAsociadaDAO
from DAO.ordenDespachoDAO import OrdenDespachoDAO
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

    def procesarOrdenCompra(self, idTienda, idOrden, idStock, codigo, cantidad, fechaSolicitud):
        try:
            self.crearConexion()

            observaciones = None
            ocaDao = OrdenCompraAsociadaDAO()
        
            stock = ocaDao.traerStock(idStock)

            if stock is None:
                print("No se encontró stock para el id proporcionado.")
                return None
            
            resultado = OrdenCompraDAO.verificarDisponibilidad(codigo, cantidad)

            if resultado == -2:
                observaciones = f"Articulo {codigo}: no existe"
                estado = "RECHAZADA"
            elif resultado == -1:
                observaciones = f"Articulo {codigo}: cantidad mal informada"
                estado = "RECHAZADA"
            elif resultado == 0:
                observaciones = f"Articulo {codigo}: no se cuenta con stock disponible"
                estado = "ACEPTADA"
            else:
                observaciones = None
                estado = "ACEPTADA"
                odDao = OrdenDespachoDAO()
                fechaEstimada = int(datetime.now().timestamp() * 1000 + 259200000) # DENTRO DE 3 DIAS
                idDespacho = odDao.agregarOrdenDespacho(fechaEstimada, idOrden)
                mensaje = {
                    'idOrdenDespacho': idDespacho,
                    'idOrden': idOrden,
                    'fechaEstimada': fechaEstimada,
                }
                producer.produce(f'{idTienda}/despacho', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
                producer.flush()
                sDao = StockDAO()
                sDao.modificarStock(codigo, cantidad)

            mensaje = {
                'idOrden': idOrden,
                'estado': estado,
                'observaciones': observaciones,
            }

            producer.produce(f'{idTienda}/solicitudes', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
            producer.flush()

            sql = ("INSERT INTO ordendecompra (codigo, tienda, color, talle, cantidad, estado, observaciones, fechaSolicitud, fechaRecepcion, ordenDeDespacho, idOrdenAsociada) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            values = (codigo, idTienda, stock.color, stock.talle, cantidad, estado, observaciones, fechaSolicitud, None, None, idOrden)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Orden de compra agregada con éxito.")

            return self._micur.lastrowid 
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

            sql = ("UPDATE ordendecompra SET observaciones = %s WHERE idOrdenDeCompra = %s")
            values = (None)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Orden de compra actualizada con éxito.")

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

    def verificarDisponibilidad(self, codigo, cantidad):
        try:
            sql = "SELECT * FROM stock WHERE producto = %s"
            self._micur.execute(sql, (codigo,))
            stock_resultado = self._micur.fetchone()

            if stock_resultado is None:
                return -2 #("Articulo: %s: No se encontró stock para el codigo proporcionado.", codigo)
            
            if cantidad < 1:
                return 0-1 #("Articulo: %s: Cantidad mal informada.", codigo)

            if cantidad > stock_resultado.cantidad:
                return 0
            
            return 1
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None

 
if __name__ == '__main__':
    a = OrdenCompraDAO()
