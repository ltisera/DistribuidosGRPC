import sys

from .configs import getConfigDB

import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

class ConexionBD:
    _pbd = None

    def __init__(self):
        self._micur = None
        self._bd = None

    def crearConexion(self):
        if ConexionBD._pbd is None:
            connectionDict = getConfigDB()
            ConexionBD._pbd = mysql.connector.pooling.MySQLConnectionPool(**connectionDict)
        self._bd = ConexionBD._pbd.get_connection()
        self._micur = self._bd.cursor()
    
    def cursorDict(self):
        self._micur = self._bd.cursor(dictionary=True, buffered=True)

    def cerrarConexion(self):
        if self._micur:
            self._micur.close()
            self._micur = None
        if self._bd:
            self._bd.close()
            self._bd = None

    def __enter__(self):
        self.crearConexion()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cerrarConexion()

    def conexiones_en_uso(self):
        try:
            if ConexionBD._pbd:
                return ConexionBD._pbd._cnx_queue.qsize()
        except Exception as e:
            print(f"Error al obtener conexiones en uso: {str(e)}")

if __name__ == '__main__':
    with ConexionBD() as conexion:
        print("Conexión creada con éxito.")
        print(f"Conexiones disponibles al inicio: {conexion.conexiones_en_uso()}")