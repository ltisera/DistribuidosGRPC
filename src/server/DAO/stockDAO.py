import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class StockDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarStock(self, idTienda, cantidad, talle, idProducto):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM stock WHERE tienda = %s AND producto = %s AND talle LIKE %s"
            self._micur.execute(check_sql, (idTienda, idProducto, talle))
            countStock = self._micur.fetchone()[0]
        
            if countStock > 0:
                print("El producto " + str(idProducto) + " con el talle " + str(talle) + " ya está habilitado en la tienda " + str(idTienda))
                return 0
            
            sql = ("INSERT INTO stock (tienda, cantidad, talle, producto)"
                   "VALUES (%s, %s, %s, %s)")
            values = (idTienda, cantidad, talle, idProducto)
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
    
    def obtenerStockPorTiendaProductoYTalle(self, idTienda, talle, idProducto):
        try:
            self.crearConexion()
            check_sql = "SELECT idStock FROM stock WHERE tienda = %s AND producto = %s AND talle LIKE %s"
            self._micur.execute(check_sql, (idTienda, idProducto, talle))
            id = self._micur.fetchone()
            return id
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return id
    
    def obtenerTiendasDeProducto(self, idProducto, talle):
        try:
            self.crearConexion()
            sql = ("SELECT tienda.* FROM stock INNER JOIN tienda ON stock.tienda = tienda.idTienda WHERE stock.producto = %s AND stock.talle = %s")
            values = [idProducto, talle]
            self._micur.execute(sql, values)
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
    
    def modificarStock(self, idStock, cantidad):
        try:
            self.crearConexion()

            sql = ("UPDATE stock SET cantidad = cantidad + %s WHERE idStock = %s")
            values = (cantidad, idStock)

            self._micur.execute(sql, values)
            self._bd.commit()
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
            sql = ("DELETE FROM stock WHERE idStock = %s")
            values = (idStock)

            self._micur.execute(sql, values)
            self._bd.commit()
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