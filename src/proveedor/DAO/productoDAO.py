import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD
from DAO.stockDAO import StockDAO

class ProductoDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    # AGREGAR PRODUCTO
    def agregarProducto(self, codigo, nombre, foto, color, talle, cantidad):
        with self:
            try:
                sql = ("INSERT INTO producto (codigo, nombre, color, foto)"
                    "VALUES (%s, %s, %s, %s)")
                values = (codigo, nombre, color, foto)
                self._micur.execute(sql, values)
                self._bd.commit()
                print("Producto agregado con éxito.")
                sdao = StockDAO()
                sdao.agregarStock(cantidad, talle, codigo )
                return codigo
            except mysql.connector.errors.IntegrityError as err:
                print(f"Integrity Error: {str(err)}")
            except mysql.connector.Error as err:
                print(f"Database Error: {str(err)}")
            except Exception as e:
                print(f"Unexpected Error: {str(e)}")
            return None
    
    # TRAER TODOS LOS PRODUCTOS
    def traerTodosLosProductos(self):
        with self:
            try:
                sql = ("SELECT producto.codigo, producto.nombre, producto.color, producto.foto,"
                "stock.talle, stock.cantidad, stock.idStock FROM producto INNER JOIN stock ON producto.codigo = stock.producto")
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
                return None
    
if __name__ == '__main__':
    a = ProductoDAO()