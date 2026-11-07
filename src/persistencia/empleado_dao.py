from typing import Optional

from persistencia.conexion import abrir_conexion, obtener_motor, marcador_sql
from dominio.empleado import Empleado

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado: Empleado) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""
                INSERT INTO empleado (nombre, email, departamento_id)
                VALUES ({marcador}, {marcador}, {marcador})
            """
            cursor.execute(sql, (empleado.nombre, empleado.email, empleado.departamento_id))
            empleado.id = cursor.lastrowid
            conexion.commit()
            return empleado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado: int) -> Optional[Empleado]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"""
                    SELECT id, nombre, email, departamento_id
                    FROM empleado WHERE id = {marca}
                """
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Empleado(id=fila[0], nombre=fila[1], email=fila[2], departamento_id=fila[3])
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_correo(correo: str) -> Optional[Empleado]:
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT id, nombre, email, departamento_id FROM empleado WHERE email = {marcador_sql()}",
                (correo,)
            )
            fila = cursor.fetchone()
            return (Empleado(id=fila[0], nombre=fila[1], email=fila[2], departamento_id=fila[3])
                    if fila else None)
        finally:
            conexion.close()

    @staticmethod
    def listar() -> list[Empleado]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, nombre, email, departamento_id FROM empleado")
            filas = cursor.fetchall()
            return [Empleado(id=f[0], nombre=f[1], email=f[2], departamento_id=f[3]) for f in filas]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(empleado: Empleado) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"""
                UPDATE empleado
                SET nombre = {marca}, email = {marca}
                WHERE id = {marca}
            """
            cursor.execute(sql, (empleado.nombre, empleado.email, empleado.id))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_empleado: int) -> bool:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            cursor.execute(f"DELETE FROM empleado WHERE id = {marca}", (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
