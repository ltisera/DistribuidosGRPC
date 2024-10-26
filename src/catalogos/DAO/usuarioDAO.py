import os, sys

import mysql.connector
import json
from mysql.connector import Error
from settings.conexionDB import ConexionBD

class UsuarioDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarUsuario(self, usuario, password, nombre, apellido, habilitado, casaCentral, idTienda):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM usuario WHERE usuario = %s"
            self._micur.execute(check_sql, (usuario,))
            countUsuario = self._micur.fetchone()[0]
        
            if countUsuario > 0:
                return("Error: El nombre de usuario ya existe.")
            
            check_sql = "SELECT * FROM tienda WHERE idTienda = %s"
            self._micur.execute(check_sql, (idTienda,))
            countTienda = self._micur.fetchone()
        
            if countTienda != None:
                return("Error: La tienda no existe.")
            
            if countTienda[4] != False:
                return("Error: La tienda no esta habilitada.")
            
            sql = ("INSERT INTO usuario (usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            values = (usuario, password, nombre, apellido, habilitado, casaCentral, idTienda)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Usuario agregado con éxito.")
            return None
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
