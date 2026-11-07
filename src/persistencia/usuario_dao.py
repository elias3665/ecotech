from typing import Optional
from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.usuario import Usuario

class UsuarioDAO:
    @staticmethod
    def insertar(usuario: Usuario) -> int:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"""INSERT INTO usuario (nombre_usuario, password_hash, id_empleado, rol)
                      VALUES ({marca}, {marca}, {marca}, {marca})"""
            cursor.execute(sql, (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id, usuario.rol))
            conexion.commit()
            return cursor.lastrowid
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre: str) -> Optional[Usuario]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"SELECT id, nombre_usuario, password_hash, id_empleado, rol FROM usuario WHERE nombre_usuario = {marca}"
            cursor.execute(sql, (nombre.strip().lower(),))
            fila = cursor.fetchone()
            if not fila:
                return None
            return Usuario(id=fila[0], nombre_usuario=fila[1], password_hash=fila[2], empleado_id=fila[3], rol=fila[4])
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_empleado(id_empleado: int) -> Optional[Usuario]:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        try:
            marca = marcador_sql()
            sql = f"SELECT id, nombre_usuario, password_hash, id_empleado, rol FROM usuario WHERE id_empleado = {marca}"
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
            if not fila:
                return None
            return Usuario(id=fila[0], nombre_usuario=fila[1], password_hash=fila[2], empleado_id=fila[3], rol=fila[4])
        finally:
            conexion.close()
