import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import mysql.connector
import json
from mysql.connector import Error
from DAO.ConexionBD import ConexionBD
from DAO.CONFIGS.variablesGlobales import TUSUARIO
class UsuarioDAO(ConexionBD):
    def __int__(self):
        pass
    
    def traerUsuarioXUsuario(self, usuario):
        usTraido = None
        try:
            self.crearConexion()
            self.cursorDict()
            self._micur.execute("SELECT * FROM " + TUSUARIO + " WHERE usuario = %s", (usuario,))
            usTraido = self._micur.fetchone()
        except Error as e:
            print("Error al conectar con la BD", e)

        finally:
            self.cerrarConexion()
        
        return usTraido
    
    def traerUsuarioSIMPLE(self, id):
        usTraido = None
        try:
            self.crearConexion()
            self.cursorDict()
            self._micur.execute("SELECT * FROM " + TUSUARIO + " WHERE idusuario = %s", (id,))
            usTraido = self._micur.fetchone()
        except Error as e:
            print("Error al conectar con la BD", e)

        finally:
            self.cerrarConexion()
        
        return usTraido

    def agregarUsuario(self, id, usuario, password, nombre, apellido, esHabilitado, esCasaCentral, idTienda):
        print(f"Valores a insertar: id={id}, usuario={usuario}, password={password}, nombre={nombre}, apellido={apellido}, esHabilitado={esHabilitado}, esCasaCentral={esCasaCentral}, idTienda={idTienda}")
        print("agregar usuario")
        devolve = False
        try:
            self.crearConexion()

            self._micur.execute("INSERT INTO " + TUSUARIO + " (idUsuario, usuario, password, nombre, apellido, habilitado, casaCentral, Tienda_idTienda) values (%s, %s, %s, %s, %s, %s, %s, %s)", (id, usuario, password, nombre, apellido, esHabilitado, esCasaCentral, idTienda))
            self._bd.commit()
            print("Commiteado con esito")
            devolve = True
            #inscripcion = self._micur.fetchone()
                
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        

        finally:
            print("Cerrando conexion")
            self.cerrarConexion()
            print("Coneccion derada")
        
        print("PASO POR ACA")
        nose = True
        print("Udao devuelve: " + str(nose))
        print("COMO ME ROMPES EL MENSAJE")
        return devolve
    

if __name__ == '__main__':
    a = UsuarioDAO()
    #ingresa UAsuario
    #a.agregarUsuario(1, "hola", "1233", "Camila", "Tisera", True, False, 123)
    #Lee Usuario
    print(a.traerUsuarioSIMPLE(1))
    print("Finnn eaaa")