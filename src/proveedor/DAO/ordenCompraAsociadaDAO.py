from datetime import datetime
import os, sys

import mysql.connector
from mysql.connector import Error
from settings.conexionDBAsociada import ConexionBD

class OrdenCompraAsociadaDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def traerOrdenCompra(self, idOrden):
        with self:
            try:
                sql = "SELECT * FROM ordendecompra WHERE idOrdenDeCompra = %s"
                self._micur.execute(sql, (idOrden,))
                orden_resultado = self._micur.fetchone()

                if orden_resultado is None:
                    print("No se encontró la orden de compra para el id proporcionado.")
                    return None
                return orden_resultado
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None
    
    def traerStock(self, idStock):
        with self:
            try:
                sql = "SELECT * FROM stock WHERE idStock = %s"
                self._micur.execute(sql, (idStock,))
                stock_resultado = self._micur.fetchone()

                return stock_resultado
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None

    def traerProducto(self, codigo):
        try:
            self.crearConexion()

            sql = "SELECT * FROM producto WHERE codigo = %s"
            self._micur.execute(sql, (codigo,))
            stock_resultado = self._micur.fetchone()

            return stock_resultado
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
    a = OrdenCompraAsociadaDAO()
