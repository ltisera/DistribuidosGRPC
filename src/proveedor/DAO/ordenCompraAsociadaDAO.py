from datetime import datetime
import os, sys

import mysql.connector
from mysql.connector import Error
from settings.conexionDBAsociada import ConexionBD

class OrdenCompraAsociadaDAO(ConexionBD):
    def __init__(self):
        super().__init__()
  
    # TRAER STOCK
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

    # TRAER PRODUCTO
    def traerProducto(self, codigo):
        with self:
            try:
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
            return None

if __name__ == '__main__':
    a = OrdenCompraAsociadaDAO()
