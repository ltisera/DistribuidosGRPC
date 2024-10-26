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

if __name__ == '__main__':
    a = CatalogoDAO()