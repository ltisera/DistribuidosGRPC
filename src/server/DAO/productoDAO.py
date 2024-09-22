import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD
from DAO.stockDAO import StockDAO

class ProductoDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarProducto(self, idProducto, nombre, foto, color, codigo, habilitado, talle):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM producto WHERE codigo = %s"
            self._micur.execute(check_sql, (codigo,))
            countProducto = self._micur.fetchone()[0]
        
            if countProducto > 0:
                print("Ya existe un producto con ese codigo.")
                return 0
            
            sql = ("INSERT INTO producto (nombre, foto, color, codigo, habilitado)"
                   "VALUES (%s, %s, %s, %s, %s)")
            values = (nombre, foto, color, codigo, habilitado)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto agregada con éxito.")
            sdao = StockDAO()
            sdao.agregarStock(1, 0,talle, self._micur.lastrowid )
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

    def verificarCodigoUnico(self, codigo, idProducto=None):
        try:
            self.crearConexion()
            
            # Consulta para verificar si el código ya existe
            if idProducto:
                check_sql = "SELECT COUNT(*) FROM producto WHERE codigo = %s AND idProducto != %s"
                self._micur.execute(check_sql, (codigo, idProducto))
            else:
                check_sql = "SELECT COUNT(*) FROM producto WHERE codigo = %s"
                self._micur.execute(check_sql, (codigo,))
            
            countProducto = self._micur.fetchone()[0]
            return countProducto > 0
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return False  
    
    def obtenerProducto(self, idProducto):
        try:
            self.crearConexion()
            sql = "SELECT *, 'S' AS talle FROM producto WHERE idProducto = %s"
            values = (idProducto,)
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
    
    def modificarProducto(self, idProducto, nombre, foto, color, codigo, habilitado, talle):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM producto WHERE idProducto != %s AND codigo = %s"
            self._micur.execute(check_sql, (idProducto,codigo))
            countProducto = self._micur.fetchone()[0]
        
            if countProducto  > 0:
                print("El codigo de producto ya existe.")
                return 0

            sql = ("UPDATE producto SET nombre = %s, foto = %s, color = %s, codigo= %s, habilitado = %s WHERE idProducto = %s")
            values = (nombre, foto, color, codigo, habilitado, idProducto)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto actualizado con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            idProducto = None
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            idProducto = None
            print(f"Database Error: {str(err)}")
        except Exception as e:
            idProducto = None
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return idProducto

    def eliminarProducto(self, idProducto):
        try:
            self.crearConexion()
            
            sql = ("UPDATE producto SET habilitado = %s WHERE idProducto = %s")
            values = (0, idProducto)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto eliminado con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None
    
    def traerTodosLosProductos(self, idTienda, soloHabilitados = False):
        try:
            self.crearConexion()
            sql = ("SELECT producto.*, stock.talle, stock.cantidad, stock.idStock FROM producto INNER JOIN stock ON producto.idProducto = stock.producto WHERE stock.tienda = %s")
            values = [idTienda]
            if(soloHabilitados):
                sql += " AND producto.habilitado = TRUE"
            sql += " ORDER BY stock.producto"
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
    
    def traerTodosLosProductosFiltrados(self, idTienda, nombre, codigo, talle, color, soloHabilitados = False):
        try:
            self.crearConexion()
            sql = "SELECT producto.*, stock.talle, stock.cantidad, stock.idStock FROM producto INNER JOIN stock ON producto.idProducto = stock.producto WHERE stock.tienda = %s"
            values = [idTienda]
            
            if nombre.strip() != "":
                sql += " AND nombre LIKE %s"
                values.append(nombre)

            if codigo.strip() != "":
                sql += " AND codigo LIKE %s"
                values.append(codigo)

            if talle.strip() != "":
                sql += " AND stock.talle LIKE %s"
                values.append(talle)

            if color.strip() != "":
                sql += " AND color LIKE %s"
                values.append(color)

            if(soloHabilitados):
                sql += " AND producto.habilitado = TRUE"
            sql += " ORDER BY stock.producto"
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
    a = ProductoDAO()