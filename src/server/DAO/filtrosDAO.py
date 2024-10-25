import mysql.connector
from mysql.connector import Error

from settings.conexionDB import ConexionBD

class FiltrosDAO(ConexionBD):
    def __init__(self):
        super().__init__()

    def guardar_filtro(self, usuario_id, nombre, codigo_producto, rango_fechas, estado, id_tienda):
        try:
            self.crearConexion()
            sql = (
                "INSERT INTO filtros (nombre, usuario_id, codigo_producto, rango_fechas_start, rango_fechas_end, estado, id_tienda) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            params = [
                nombre,
                usuario_id,
                codigo_producto,
                rango_fechas[0] if rango_fechas else None,
                rango_fechas[1] if rango_fechas else None,
                estado,
                id_tienda
            ]
            print("Parametros: ", params)
            self._micur.execute(sql, params)
            self._bd.commit()
        except Exception as e:
            print(f"Error al guardar filtro: {str(e)}")
        finally:
            self.cerrarConexion()

    def obtener_filtro_por_id(self, id_filtro):
        try:
            self.crearConexion()
            sql = "SELECT * FROM filtros WHERE id = %s"
            self._micur.execute(sql, (id_filtro,))
            return self._micur.fetchone()
        except Exception as e:
            print(f"Error al obtener filtro por ID: {str(e)}")
            return None
        finally:
            self.cerrarConexion()

    def obtener_filtros(self, usuario_id):
        try:
            self.crearConexion()
            sql = "SELECT * FROM filtros WHERE usuario_id = %s"
            self._micur.execute(sql, (usuario_id,))
            return self._micur.fetchall()
        except Exception as e:
            print(f"Error al obtener filtros: {str(e)}")
            return []
        finally:
            self.cerrarConexion()

    def editar_filtro(self, filtro_id, nombre, codigo_producto, rango_fechas, estado, id_tienda):
        try:
            self.crearConexion()
            sql = (
                "UPDATE filtros SET nombre = %s, codigo_producto = %s, rango_fechas_start = %s, "
                "rango_fechas_end = %s, estado = %s, id_tienda = %s WHERE id = %s"
            )
            params = [
                nombre,
                codigo_producto,
                rango_fechas[0] if rango_fechas else None,
                rango_fechas[1] if rango_fechas else None,
                estado,
                id_tienda,
                filtro_id
            ]
            self._micur.execute(sql, params)
            self._bd.commit()
        except Exception as e:
            print(f"Error al editar filtro: {str(e)}")
        finally:
            self.cerrarConexion()

    def borrar_filtro(self, filtro_id):
        try:
            self.crearConexion()
            sql = "DELETE FROM filtros WHERE id = %s"
            self._micur.execute(sql, (filtro_id,))
            self._bd.commit()
        except Exception as e:
            print(f"Error al borrar filtro: {str(e)}")
        finally:
            self.cerrarConexion()
if __name__ == '__main__':
    a = FiltrosDAO()