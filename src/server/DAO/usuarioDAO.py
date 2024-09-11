import os, sys

import mysql.connector
import json
from mysql.connector import Error
from settings.conexionDB import ConexionBD

class UsuarioDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def iniciarSesion(self, usuario, password):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM usuario u WHERE u.usuario = %s AND u.password = %s")
            self._micur.execute(sql, (usuario, password))
            resultado = self._micur.fetchone()
            print("Resultado", str(resultado))
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

    def agregarUsuario(self, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM usuario WHERE usuario = %s"
            self._micur.execute(check_sql, (usuario,))
            countUsuario = self._micur.fetchone()[0]
        
            if countUsuario > 0:
                print("El nombre de usuario ya existe.")
                return 0
            
            check_sql = "SELECT COUNT(*) FROM tienda WHERE idTienda = %s"
            self._micur.execute(check_sql, (idTienda,))
            countTienda = self._micur.fetchone()[0]
        
            if countTienda == 0:
                print("La tienda no existe.")
                return -1

            sql = ("INSERT INTO usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            values = (usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Usuario agregado con éxito.")
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

            check_sql = "SELECT COUNT(*) FROM usuario WHERE usuario = %s"
            self._micur.execute(check_sql, (usuario,))
            countUsuario = self._micur.fetchone()[0]
        
            if countUsuario > 0:
                print("El nombre de usuario ya existe.")
                return 0

            habilitado = int(habilitado)
            casaCentral = int(casaCentral)

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
    
    def traerTodosLosUsuariosFiltrados(self, idTienda, nombre):
        try:
            self.crearConexion()
            sql = "SELECT * FROM usuario WHERE 1=1"
            values = []
            
            if idTienda != 0:
                sql += " AND Tienda_idTienda = %s"
                values.append(idTienda)
            
            if nombre.strip() != "":
                sql += " AND usuario LIKE %s"
                values.append(f"%{nombre}%")
            self._micur.execute(sql, tuple(values))
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
