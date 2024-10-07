import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class OrdenDespachoDAO(ConexionBD):
    def __init__(self):
        super().__init__()
    
    def agregarOrdenDespacho(self, fechaEstimada, idOrden):
        with self:
            try:
                sql = ("INSERT INTO ordendedespacho (fechaEstimada, ordenDeCompra)"
                    "VALUES (%s, %s)")
                values = (fechaEstimada, idOrden)
                self._micur.execute(sql, values)
                self._bd.commit()
                return self._micur.lastrowid 
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None
    
if __name__ == '__main__':
    a = OrdenDespachoDAO()