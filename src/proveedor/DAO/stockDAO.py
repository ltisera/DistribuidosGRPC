import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class StockDAO(ConexionBD):
    def __init__(self):
        super().__init__()
    
    # AGREGAR STOCK
    def agregarStock(self, cantidad, talle, idProducto):
        with self:
            try:
                check_sql = "SELECT COUNT(*) FROM stock WHERE producto = %s AND talle LIKE %s"
                self._micur.execute(check_sql, (idProducto, talle))
                countStock = self._micur.fetchone()[0]
            
                if countStock > 0:
                    print("El producto " + str(idProducto) + " con el talle " + str(talle) + " ya está habilitado")
                    return 0
                
                sql = ("INSERT INTO stock (cantidad, talle, producto)"
                    "VALUES (%s, %s, %s)")
                values = (cantidad, talle, idProducto)
                self._micur.execute(sql, values)
                self._bd.commit()
                return self._micur.lastrowid 
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error agregarStock: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None

    # DISMINUIR STOCK
    def disminuirStock(self, codigo, cantidad):
        with self:
            try:
                sql = ("UPDATE stock SET cantidad = cantidad - %s WHERE producto = %s")
                values = (cantidad, codigo)

                self._micur.execute(sql, values)
                self._bd.commit()
                idStock = self._micur.lastrowid
            except mysql.connector.errors.IntegrityError as err:
                idStock = None
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                idStock = None
                print(f"Database Error disminuirStock: {str(err)}")
            except Exception as e:
                idStock = None
                print(f"Unexpected Error: {str(e)}")
            return idStock
        
    # MODIFICAR STOCK
    def modificarStock(self, idStock, cantidad):
        with self:
            try:
                sql = ("UPDATE stock SET cantidad = %s WHERE idStock = %s")
                values = (cantidad, idStock)

                self._micur.execute(sql, values)
                self._bd.commit()
            except mysql.connector.errors.IntegrityError as err:
                idStock = None
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                idStock = None
                print(f"Database Error modificarStock: {str(err)}")
            except Exception as e:
                idStock = None
                print(f"Unexpected Error: {str(e)}")
            return idStock
    
if __name__ == '__main__':
    a = StockDAO()