from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto

class ProyectoDAO:
    @staticmethod
    def insertar(proyecto: Proyecto) -> Proyecto:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"INSERT INTO proyecto (id, nombre, fecha_inicio) VALUES ({marca}, {marca}, {marca})"
            cursor.execute(sql, (proyecto.id_proyecto, proyecto.nombre, proyecto.fecha_inicio))
            conexion.commit()
            return proyecto
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_id(id_proyecto: str) -> Proyecto | None:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"SELECT id, nombre, fecha_inicio FROM proyecto WHERE id = {marca}"
            cursor.execute(sql, (id_proyecto,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Proyecto(id_proyecto=fila[0], nombre=fila[1], fecha_inicio=fila[2])
        finally:
            conexion.close()

    @staticmethod
    def listar() -> list[Proyecto]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, nombre, fecha_inicio FROM proyecto")
            filas = cursor.fetchall()
            return [Proyecto(id_proyecto=f[0], nombre=f[1], fecha_inicio=f[2]) for f in filas]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(proyecto: Proyecto) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"UPDATE proyecto SET nombre = {marca}, fecha_inicio = {marca} WHERE id = {marca}"
            cursor.execute(sql, (proyecto.nombre, proyecto.fecha_inicio, proyecto.id_proyecto))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_proyecto: str) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"DELETE FROM proyecto WHERE id = {marca}"
            cursor.execute(sql, (id_proyecto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
