import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class StockDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarStock(self, idTienda, cantidad, talle, idProducto):
        try:
            self.crearConexion()
            
            sql = ("INSERT INTO stock (tienda, cantidad, talle, producto)"
                   "VALUES (%s, %s, %s, %s)")
            values = (idTienda, cantidad, talle, idProducto)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Stock agregada con éxito.")
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
    
    def obtenerStock(self, idStock):
        try:
            self.crearConexion()
            sql = "SELECT * FROM stock WHERE idStock = %s"
            values = (idStock,)
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
    
    def modificarStock(self, idStock, cantidad, talle):
        try:
            self.crearConexion()

            sql = ("UPDATE stock SET cantidad = %s, talle = %s WHERE idStock = %s")
            values = (talle, cantidad, idStock)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Stock actualizada con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            idStock = None
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            idStock = None
            print(f"Database Error: {str(err)}")
        except Exception as e:
            idStock = None
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return idStock

    def eliminarStock(self, idStock):
        try:
            self.crearConexion()
            
        #implementar
            #sql = ("UPDATE stock SET habilitado = %s WHERE idStock = %s")
            #values = (0, idStock)

            #self._micur.execute(sql, values)
            #self._bd.commit()
            print("Stock eliminada con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None
    
    def traerTodosLosStocks(self):
        try:
            self.crearConexion()
            sql = ("SELECT * FROM stock")
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
    a = StockDAO()