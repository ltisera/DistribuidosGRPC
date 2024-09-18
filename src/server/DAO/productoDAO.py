import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

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
            
            sql = ("INSERT INTO producto (idProducto, nombre, foto, color, codigo, habilitado)"
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            values = (idProducto, nombre, foto, color, codigo, habilitado)
            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto agregada con éxito.")
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

            sql = ("UPDATE producto SET nombre = %s, foto = %s, color = %s, codigo= %s WHERE idProducto = %s")
            values = (nombre, foto, color, codigo, idProducto)

            self._micur.execute(sql, values)
            self._bd.commit()
            print("Producto actualizada con éxito.")
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
            
        #implementar
            #sql = ("UPDATE producto SET habilitado = %s WHERE idProducto = %s")
            #values = (0, idProducto)

            #self._micur.execute(sql, values)
            #self._bd.commit()
            print("Producto eliminada con éxito.")
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
            sql = ("SELECT *, 'S' AS talle FROM producto")
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
    
    def traerTodosLosProductosFiltrados(self, nombre, codigo, talle, color):
        try:
            self.crearConexion()
            sql = "SELECT *, 'S' AS talle FROM producto WHERE 1=1"
            values = []
            
            if nombre.strip() != "":
                sql += " AND nombre LIKE %s"
                values.append(nombre)

            if codigo.strip() != "":
                sql += " AND codigo LIKE %s"
                values.append(codigo)

            #implementar talle

            if color.strip() != "":
                sql += " AND color LIKE %s"
                values.append(color)

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