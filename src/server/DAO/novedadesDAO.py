import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class NovedadesDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarNovedad(self, codigo, nombre, talle, color, url):
        try:
            self.crearConexion()
            sql = ("INSERT INTO novedades(codigo, nombre, talle, color, url)"
                   "VALUES (%s, %s, %s, %s, %s)")
            values = (codigo, nombre, talle, color, url)
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

    def eliminarNovedad(self, codigo):
        try:
            self.crearConexion()
            sql = ("DELETE FROM novedades WHERE codigo = %s")
            values = (codigo,)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Novedad eliminada con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        return None

    def traerTodasLasNovedades(self):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM novedades n LEFT JOIN producto p ON n.codigo = p.codigo WHERE p.codigo IS NULL")
            self._micur.execute(sql)
            resultados = self._micur.fetchall()
            return resultados
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
    a = NovedadesDAO()