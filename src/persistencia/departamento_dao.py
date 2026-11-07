from dominio.departamento import Departamento
from persistencia.conexion import abrir_conexion, marcador_sql

class DepartamentoDAO:
    @staticmethod
    def buscar_por_nombre(nombre):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT id, nombre, descripcion, gerente_empleado_id FROM departamento WHERE nombre = {marcador_sql()}", (nombre,))
            fila = cursor.fetchone()
            return Departamento(nombre=fila[1], descripcion=fila[2], gerente_id=fila[3], id_dept=fila[0]) if fila else None
        finally:
            conexion.close()

    @staticmethod
    def insertar(departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"INSERT INTO departamento (nombre, descripcion, gerente_empleado_id) VALUES ({marca}, {marca}, {marca})",
                           (departamento.nombre, departamento.descripcion, departamento.gerente_id))
            departamento.id_dept = cursor.lastrowid
            conexion.commit()
            return departamento
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def asignar_gerente(departamento_id, empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"SELECT id FROM empleado WHERE id = {marca}", (empleado_id,))
            if cursor.fetchone() is None:
                raise ValueError("El empleado gerente no existe.")
            cursor.execute(f"UPDATE departamento SET gerente_empleado_id = {marca} WHERE id = {marca}", (empleado_id, departamento_id))
            if not cursor.rowcount:
                raise ValueError("El departamento no existe.")
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def asignar_empleado(empleado_id, departamento_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(f"SELECT id FROM departamento WHERE id = {marca}", (departamento_id,))
            if cursor.fetchone() is None:
                raise ValueError("El departamento no existe.")
            cursor.execute(f"UPDATE empleado SET departamento_id = {marca} WHERE id = {marca}", (departamento_id, empleado_id))
            if not cursor.rowcount:
                raise ValueError("El empleado no existe.")
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
