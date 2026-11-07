from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.registrotrabajo import RegistroTrabajo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO

class RegistroTrabajoDAO:
    @staticmethod
    def insertar(registro: RegistroTrabajo) -> RegistroTrabajo:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"""INSERT INTO registro_trabajo (empleado_id, proyecto_id, fecha, horas, descripcion)
                        VALUES ({marca}, {marca}, {marca}, {marca}, {marca})"""
            cursor.execute(sql, (registro.empleado.id, registro.proyecto.id_proyecto,
                                    registro.fecha, registro.horas, registro.descripcion))
            conexion.commit()
            registro.id = cursor.lastrowid
            return registro
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def existe(empleado_id, proyecto_id, fecha, descripcion):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            cursor.execute(
                f"SELECT 1 FROM registro_trabajo WHERE empleado_id={marca} AND proyecto_id={marca} "
                f"AND fecha={marca} AND descripcion={marca} LIMIT 1",
                (empleado_id, proyecto_id, fecha, descripcion)
            )
            return cursor.fetchone() is not None
        finally:
            conexion.close()

    @staticmethod
    def listar_completo() -> list[RegistroTrabajo]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, empleado_id, proyecto_id, fecha, horas, descripcion FROM registro_trabajo")
            filas = cursor.fetchall()
            registros = []
            for f in filas:
                emp = EmpleadoDAO.buscar_por_id(f[1])
                proy = ProyectoDAO.buscar_por_id(f[2])
                if emp and proy:
                    reg = RegistroTrabajo(id_registro=f[0], empleado=emp, proyecto=proy,
                                            fecha=f[3], horas=f[4], descripcion=f[5])
                    registros.append(reg)
            return registros
        finally:
            conexion.close()

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT id, empleado_id, proyecto_id, fecha, horas, descripcion FROM registro_trabajo WHERE empleado_id = {marcador_sql()} ORDER BY fecha DESC", (empleado_id,))
            registros = []
            for f in cursor.fetchall():
                emp = EmpleadoDAO.buscar_por_id(f[1])
                proy = ProyectoDAO.buscar_por_id(f[2])
                if emp and proy:
                    registros.append(RegistroTrabajo(id_registro=f[0], empleado=emp, proyecto=proy, fecha=f[3], horas=f[4], descripcion=f[5]))
            return registros
        finally:
            conexion.close()
