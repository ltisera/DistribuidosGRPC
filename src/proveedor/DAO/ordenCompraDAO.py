from datetime import datetime
import os, sys
import traceback

import mysql.connector
import json
from mysql.connector import Error
from DAO.ordenCompraAsociadaDAO import OrdenCompraAsociadaDAO
from DAO.ordenDespachoDAO import OrdenDespachoDAO
from settings.conexionDB import ConexionBD

from DAO.stockDAO import StockDAO

# KAFKA
from confluent_kafka import Producer

# PRODUCTOR
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print('Error al enviar el mensaje: {}'.format(err))
    else:
        print('Mensaje enviado a {} [{}]'.format(msg.topic(), msg.partition()))

class OrdenCompraDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    # PROCESAR ORDEN COMPRA
    def procesarOrdenCompra(self, idTienda, idOrden, idStock, codigo, cantidad, fechaSolicitud):
        with self:
            try:
                observaciones = None
                ocaDao = OrdenCompraAsociadaDAO()
                stock = ocaDao.traerStock(idStock)
                producto = ocaDao.traerProducto(codigo)

                if stock is None:
                    print("No se encontró stock para el id proporcionado.")
                    return None
                
                if producto is None:
                    print("No se encontró producto para el codigo proporcionado.")
                    return None

                cantidadInt = int(cantidad)

                sql = ("INSERT INTO ordendecompra (codigo, tienda, color, talle, cantidad, estado, observaciones, fechaSolicitud, fechaRecepcion, ordenDeDespacho, idOrdenAsociada) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                values = (codigo, idTienda, producto[3], stock[2], cantidadInt, None, observaciones, fechaSolicitud, None, None, idOrden)
                self._micur.execute(sql, values)
                self._bd.commit()

                ordenCompraId = self._micur.lastrowid
                print("Orden de compra agregada con éxito.")

                resultado = self.verificarDisponibilidad(codigo, cantidadInt)

                if resultado == -2:
                    observaciones = f"Articulo {codigo}: no existe"
                    estado = "RECHAZADA"
                    print("Entro al -2")
                    self.modificarOrdenCompra(ordenCompraId, estado, observaciones, None)
                elif resultado == -1:
                    observaciones = f"Articulo {codigo}: cantidad mal informada"
                    estado = "RECHAZADA"
                    print("Entro al -1")
                    self.modificarOrdenCompra(ordenCompraId, estado, observaciones, None)
                elif resultado == 0:
                    observaciones = f"Articulo {codigo}: no se cuenta con stock disponible"
                    estado = "ACEPTADA"
                    print("Entro al 0")
                    self.modificarOrdenCompra(ordenCompraId, estado, observaciones, None)
                else:
                    print("Entro al 1")
                    observaciones = None
                    estado = "ACEPTADA"
                    odDao = OrdenDespachoDAO()
                    fechaEstimada = int(datetime.now().timestamp() * 1000 + 259200000) # DENTRO DE 3 DIAS
                    idDespacho = odDao.agregarOrdenDespacho(fechaEstimada, ordenCompraId)
                    mensaje = {
                        'idOrdenDespacho': idDespacho,
                        'idOrden': idOrden,
                        'fechaEstimada': fechaEstimada,
                    }
                    producer.produce(f'{idTienda}-despacho', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
                    sDao = StockDAO()
                    sDao.disminuirStock(codigo, cantidadInt)
                    self.modificarOrdenCompra(ordenCompraId, estado, observaciones, idDespacho)

                mensaje = {
                    'idOrden': idOrden,
                    'estado': estado,
                    'observaciones': observaciones,
                }
                producer.produce(f'{idTienda}-solicitudes', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
                producer.flush()
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")

    # MODIFICAR ORDEN COMPRA
    def modificarOrdenCompra(self, idOrdenCompra, estado, observaciones, idDespacho):
        with self: 
            try:
                sql = ("UPDATE ordendecompra SET observaciones = %s, estado = %s, ordenDeDespacho = %s WHERE idOrdenDeCompra = %s")
                values = (observaciones, estado, idDespacho, idOrdenCompra)

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

    # VERIFICAR DISPONIBILIDAD
    def verificarDisponibilidad(self, codigo, cantidad):
        with self:
            try:
                sql = "SELECT * FROM stock WHERE producto = %s"
                self._micur.execute(sql, (codigo,))
                stock_resultado = self._micur.fetchone()

                if stock_resultado is None:
                    return -2 #("Articulo: %s: No se encontró stock para el codigo proporcionado.", codigo)
                
                if cantidad < 1:
                    return -1 #("Articulo: %s: Cantidad mal informada.", codigo)

                print("Cantidad solicitada: ", cantidad)
                print("Cantidad: ", stock_resultado[2])

                if cantidad > stock_resultado[2]:
                    return 0
                
                return 1
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None

    # PROCESAR RECIBO DE MERCADERIA
    def procesarRecibo(self, idOrdenDespacho, fechaRecepcion):
        with self: 
            try:
                sql = ("UPDATE ordendecompra SET fechaRecepcion = %s WHERE ordenDeDespacho = %s")
                values = (fechaRecepcion, idOrdenDespacho)

                self._micur.execute(sql, values)
                self._bd.commit()
                print("Orden de compra actualizada con éxito.")
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
                return None
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
                return None
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")

    def verificarOrdenesDeCompra(self, idStock):
        with self: 
            try:
                if self._micur is None:
                    print("Error: El cursor no está inicializado.")
                    return

                sql = ("SELECT producto FROM stock WHERE idStock = %s")
                values = (idStock,)
                self._micur.execute(sql, values)
                stock_resultado = self._micur.fetchone()

                if stock_resultado is None:
                    print("No se encontró el stock.")
                    return

                codigo = stock_resultado[0]

                sql = ("SELECT * FROM ordendecompra WHERE codigo = %s AND estado = 'ACEPTADA' AND observaciones = %s")
                observaciones = f'Articulo {codigo}: no se cuenta con stock disponible'
                values = (codigo, observaciones)
                self._micur.execute(sql, values)
                orden_resultado = self._micur.fetchall()

                if not orden_resultado:
                    print("No se encontraron órdenes de compra aceptadas.")
                    return
            
                for orden in orden_resultado:
                    idOrdenAsociada = orden[11]
                    cantidadOrden = orden[5]
                    idTienda = orden[2]
                    idOrdenCompra = orden[0]

                    if self._micur is None:
                        print("Error: El cursor no está inicializado.")
                        return
                    sql = ("SELECT cantidad FROM stock WHERE idStock = %s")
                    values = (idStock,)
                    self._micur.execute(sql, values)
                    stock_resultado = self._micur.fetchone()
                    
                    if stock_resultado is None:
                        print("No se encontró el stock.")
                        return

                    cantidad = stock_resultado[0]

                    if(cantidad >= cantidadOrden):
                        odDao = OrdenDespachoDAO()
                        fechaEstimada = int(datetime.now().timestamp() * 1000 + 259200000) # DENTRO DE 3 DIAS
                        idDespacho = odDao.agregarOrdenDespacho(fechaEstimada, idOrdenCompra)
                        mensaje = {
                            'idOrdenDespacho': idDespacho,
                            'idOrden': idOrdenAsociada,
                            'fechaEstimada': fechaEstimada,
                        }
                        producer.produce(f'{idTienda}-despacho', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
                        sDao = StockDAO()
                        sDao.disminuirStock(codigo, cantidadOrden)
                        estado = 'ACEPTADA'
                        observaciones = None
                        self.modificarOrdenCompra(idOrdenCompra, estado, observaciones, idDespacho)
                        mensaje = {
                            'idOrden': idOrdenAsociada,
                            'estado': estado,
                            'observaciones': observaciones,
                        }
                        producer.produce(f'{idTienda}-solicitudes', json.dumps(mensaje).encode('utf-8'), callback=delivery_report)
                        producer.flush()
                        print("Orden de compra actualizada con éxito.")
            
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
                return None
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
                return None
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
                print(traceback.format_exc())

if __name__ == '__main__':
    a = OrdenCompraDAO()
