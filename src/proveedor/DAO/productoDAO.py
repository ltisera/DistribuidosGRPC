import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD
from DAO.stockDAO import StockDAO

class ProductoDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarProducto(self, nombre, foto, color, talle, cantidad):
        try:
            self.crearConexion()

            sql = ("INSERT INTO producto (nombre, color, foto)"
                   "VALUES (%s, %s, %s)")
            values = (nombre, color, foto)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto agregado con éxito.")
            sdao = StockDAO()
            sdao.agregarStock(cantidad, talle, self._micur.lastrowid )
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
    
    def traerTodosLosProductos(self):
        try:
            self.crearConexion()
            sql = ("SELECT producto.idProducto, producto.nombre, producto.color, producto.foto,"
               "stock.talle, stock.cantidad, stock.idStock FROM producto INNER JOIN stock ON producto.idProducto = stock.producto")
            self._micur.execute(sql)
            resultados = self._micur.fetchall()
            productos = []
            for row in resultados:
                producto = {
                    'idProducto': row[0],
                    'nombre': row[1],
                    'color': row[2],
                    'foto': row[3],
                    'talle': row[4],
                    'cantidad': row[5],
                    'idStock': row[6]
                }
                productos.append(producto)
            return productos
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
    a = ProductoDAO()