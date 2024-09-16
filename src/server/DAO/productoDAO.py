import mysql.connector
from mysql.connector import Error
from settings.conexionDB import ConexionBD

class ProductoDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def agregarProducto(self, idProducto, nombre, foto, color, codigo):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM producto WHERE idProducto = %s"
            self._micur.execute(check_sql, (idProducto,))
            countProducto = self._micur.fetchone()[0]
        
            if countProducto > 0:
                print("Ya existe un producto con ese ID.")
                return 0
            
            sql = ("INSERT INTO producto (idProducto, nombre, foto, color, codigo)"
                   "VALUES (%s, %s, %s, %s, %s)")
            values = (idProducto, nombre, foto, color, codigo)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto agregado con éxito.")
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
    
    def obtenerProducto(self, idProducto):
        try:
            self.crearConexion()
            sql = "SELECT * FROM producto WHERE idProducto = %s"
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
    
    def modificarProducto(self, idProducto, nombre, foto, color, codigo):
        try:
            self.crearConexion()

            check_sql = "SELECT COUNT(*) FROM producto WHERE idProducto = %s"
            self._micur.execute(check_sql, (idProducto,))
            countProducto = self._micur.fetchone()[0]
        
            if countProducto == 0:
                print("No existe un producto con ese ID.")
                return 0

            sql = ("UPDATE producto SET nombre = %s, foto = %s, color = %s, codigo = %s WHERE idProducto = %s")
            values = (nombre, foto, color, codigo, idProducto)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto actualizado con éxito.")
        except mysql.connector.errors.IntegrityError as err:
            print(f"Integrity Error: {str(err)}")
        except mysql.connector.Error as err:
            print(f"Database Error: {str(err)}")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
        finally:
            self.cerrarConexion()
        
        return None

    def eliminarProducto(self, idProducto):
        try:
            self.crearConexion()

            sql = "DELETE FROM producto WHERE idProducto = %s"
            values = (idProducto,)

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
    
    def traerTodosLosProductos(self):
        try:
            self.crearConexion()
            sql = "SELECT * FROM producto"
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
    
    def traerTodosLosProductosFiltrados(self, idProducto, color):
        try:
            self.crearConexion()
            sql = "SELECT * FROM producto WHERE 1=1"
            values = []
            
            if idProducto != -1:
                sql += " AND idProducto = %s"
                values.append(idProducto)

            if color:
                sql += " AND color = %s"
                values.append(color)

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
    a = ProductoDAO()
