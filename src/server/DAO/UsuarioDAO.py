import mysql.connector
from mysql.connector import Error

from server.settings.conexionDB import ConexionBD

class UsuarioDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def iniciarSesion(self, usuario, password):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM usuario u WHERE u.usuario = %s AND u.password = %s")
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
        try:
            self.crearConexion()
            sql = ("INSERT INTO usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            values = (usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
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
    
    def obtenerUsuario(self, idUsuario):
        try:
            self.crearConexion()
            sql = "SELECT * FROM usuario WHERE idUsuario = %s"
            values = (idUsuario,)
            self._micur.execute(sql, values)
            resultado = self._micur.fetchone()
            print(f"Resultado de la consulta: {resultado}") 
            return resultado
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None
    
    def modificarUsuario(self, idUsuario, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda):
        try:
            self.crearConexion()

            habilitado = int(habilitado)
            casaCentral = int(casaCentral)

            print("Usuario: ", usuario, " Password: ", password, " Nombre: ", nombre, " Apellido: ", apellido, " Habilitado: ", habilitado, " CasaCentral: ", casaCentral, "IdTienda: ", idTienda)

            sql = ("UPDATE usuario SET usuario = %s, password = %s, nombre = %s, apellido = %s, habilitado = %s, casaCentral = %s, Tienda_idTienda = %s WHERE idUsuario = %s")
            values = (usuario, password, nombre, apellido, habilitado, casaCentral, idTienda, idUsuario)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Usuario actualizado con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None
    
    def eliminarUsuario(self, idUsuario):
        try:
            self.crearConexion()

            sql = ("UPDATE usuario SET habilitado = %s WHERE idUsuario = %s")
            values = (0, idUsuario)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Usuario eliminado con éxito.")
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
