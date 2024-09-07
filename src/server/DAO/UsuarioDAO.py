import mysql.connector
from mysql.connector import Error

from server.dao.configs import getConfigDB

class ConexionBD:
    def __init__(self):
        self._micur = None
        self._bd = None

    def crearConexion(self):
        config = getConfigDB()
        try:
            self._bd = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                port=config['port'],
                password=config['password'],
                database=config['database'],
                auth_plugin=config['auth_plugin']
            )
            self._micur = self._bd.cursor(dictionary=True)
        except Error as e:
            print(f"Error al conectar con la BD: {e}")

    def cerrarConexion(self):
        if self._micur:
            self._micur.close()
        if self._bd:
            self._bd.close()

class UsuarioDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarUsuario(self, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda):
        print(f"Valores a insertar: usuario={usuario}, password={password}, nombre={nombre}, apellido={apellido}, habilitado={habilitado}, casaCentral={casaCentral}, idTienda={idTienda}")
        try:
            self.crearConexion()
            sql = ("INSERT INTO usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            values = (usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Usuario agregado con éxito")
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

if __name__ == '__main__':
    a = UsuarioDAO()
