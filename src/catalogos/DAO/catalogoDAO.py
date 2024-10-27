import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class CatalogoDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarCatalogo(self, nombre, idTienda):
        try:
            self.crearConexion()
            sql = ("INSERT INTO catalogo(nombre, idTienda)"
                   "VALUES (%s, %s)")
            values = (nombre, idTienda)
            self._micur.execute(sql, values)
            self._bd.commit()
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

    def obtenerCatalogo(self, idCatalogo):
        try:
            self.crearConexion()
            sql = "SELECT nombre FROM catalogo WHERE idCatalogo = %s"
            self._micur.execute(sql, (idCatalogo,))
            catalogo = self._micur.fetchone()
            return catalogo
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            return []
        finally:
            self.cerrarConexion()

    def obtenerCatalogos(self, idTienda):
        try:
            self.crearConexion()
            sql = "SELECT * FROM catalogo WHERE idTienda = %s"
            self._micur.execute(sql, (idTienda,))
            catalogos = self._micur.fetchall()
            return catalogos
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            return []
        finally:
            self.cerrarConexion()

    def eliminarCatalogo(self, idCatalogo):
        try:
            self.crearConexion()
            sql = "DELETE FROM catalogo WHERE idCatalogo = %s"
            self._micur.execute(sql, (idCatalogo,))
            self._bd.commit()
        except Exception as e:
            print(f"Error al borrar catalogo: {str(e)}")
        finally:
            self.cerrarConexion()        

    def obtenerProductosPorTienda(self, idTienda):
        try:
            self.crearConexion()
            sql = """
                SELECT p.idProducto, p.nombre, p.foto, p.color, s.talle
                FROM producto p
                INNER JOIN stock s ON p.idProducto = s.producto
                WHERE s.tienda = %s
            """
            self._micur.execute(sql, (idTienda,))
            productos = self._micur.fetchall()
            return productos
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            return []
        finally:
            self.cerrarConexion()
    
    def obtenerProductosPorCatalogo(self, idCatalogo):
        try:
            self.crearConexion()
            sql = """
                SELECT p.idProducto, p.nombre, p.foto, p.color, s.talle
                FROM producto p
                INNER JOIN stock s ON p.idProducto = s.producto
                INNER JOIN catalogo_has_producto cp ON p.idProducto = cp.idProducto
                WHERE cp.idCatalogo = %s and s.talle = cp.talle
                GROUP BY p.idProducto, p.nombre, p.foto, p.color, s.talle
            """
            self._micur.execute(sql, (idCatalogo,))
            productos = self._micur.fetchall()
            return productos
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            return []
        finally:
            self.cerrarConexion()

    def agregarProductoACatalogo(self, id_catalogo, id_producto, talle):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM catalogo_has_producto c WHERE c.idCatalogo = %s AND c.idProducto = %s AND c.talle = %s"
            self._micur.execute(check_sql, (id_catalogo, id_producto, talle))
            countProducto = self._micur.fetchone()[0]
        
            if countProducto > 0:
                print("El producto ya se encuentra en el catalogo.")
                return 0

            sql = "INSERT INTO catalogo_has_producto (idCatalogo, idProducto, talle) VALUES (%s, %s, %s)"
            self._micur.execute(sql, (id_catalogo, id_producto, talle))
            self._bd.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            self._bd.rollback()
        finally:
            self.cerrarConexion()

    def eliminarProductoDeCatalogo(self, id_catalogo, id_producto, talle):
        try:
            self.crearConexion()
            sql = "DELETE FROM catalogo_has_producto WHERE idCatalogo = %s AND idProducto = %s AND talle = %s"
            self._micur.execute(sql, (id_catalogo, id_producto, talle))
            self._bd.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
            self._bd.rollback()
        finally:
            self.cerrarConexion()

if __name__ == '__main__':
    a = CatalogoDAO()