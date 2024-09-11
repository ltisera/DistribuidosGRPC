import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class TiendaDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarTienda(self, idTienda, direccion, ciudad, provincia, habilitado):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM tienda WHERE idTienda = %s"
            self._micur.execute(check_sql, (idTienda,))
            countUsuario = self._micur.fetchone()[0]
        
            if countUsuario > 0:
                print("Ya existe una tienda con ese código.")
                return 0
            
            sql = ("INSERT INTO tienda (idTienda, direccion, ciudad, provincia, habilitado)"
                   "VALUES (%s, %s, %s, %s, %s)")
            values = (idTienda, direccion, ciudad, provincia, habilitado)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Tienda agregada con éxito.")
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
    
    def obtenerTienda(self, idTienda):
        try:
            self.crearConexion()
            sql = "SELECT * FROM tienda WHERE idTienda = %s"
            values = (idTienda,)
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
    
    def modificarTienda(self, idTienda, direccion, ciudad, provincia, habilitado):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM tienda WHERE idTienda = %s"
            self._micur.execute(check_sql, (idTienda,))
            countTienda = self._micur.fetchone()[0]
        
            if countTienda > 0:
                print("Ese codigo de tienda ya existe.")
                return 0

            habilitado = int(habilitado)

            sql = ("UPDATE tienda SET direccion = %s, ciudad = %s, provincia = %s, habilitado = %s WHERE idTienda = %s")
            values = (direccion, ciudad, provincia, habilitado, idTienda)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Tienda actualizada con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None

    def eliminarTienda(self, idTienda):
        try:
            self.crearConexion()

            sql = ("UPDATE tienda SET habilitado = %s WHERE idTienda = %s")
            values = (0, idTienda)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Tienda eliminada con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None
    
    def traerTodasLasTiendas(self):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM tienda")
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
    
    def traerTodasLasTiendasFiltradas(self, idTienda, habilitado):
        try:
            self.crearConexion()
            sql = "SELECT * FROM tienda WHERE 1=1"
            values = []
            
            if idTienda != -1:
                sql += " AND idTienda = %s"
                values.append(idTienda)

            if habilitado != -1:
                sql += " AND habilitado = %s"
                values.append(habilitado)

            self._micur.execute(sql, tuple(values))
            resultados = self._micur.fetchall()
            print(resultados) 
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
    a = TiendaDAO()