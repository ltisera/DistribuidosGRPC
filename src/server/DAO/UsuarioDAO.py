import mysql.connector
from mysql.connector import Error

from server.dao.conexionDB import ConexionBD

class UsuarioDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def iniciarSesion(self, usuario, password):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM usuario u WHERE u.usuario = %s AND u.password = %s")
            print(f"Ejecutando consulta: {sql} con usuario='{usuario}' y contraseña='{password}'")
            self._micur.execute(sql, (usuario, password))
            resultados = self._micur.fetchall()
            print("Resultados", str(resultados))
            return len(resultados) > 0
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None

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
    
    def traerTodosLosUsuarios(self):
        try:
            self.crearConexion()
            #sql = ("SELECT u.usuario, t.direccion, u.habilitado FROM usuario u INNER JOIN tienda t ON u.Tienda_idTienda = t.idTienda")
            sql = ("SELECT * FROM usuario")
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
    a = UsuarioDAO()
