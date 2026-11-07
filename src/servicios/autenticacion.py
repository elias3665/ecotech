import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin

MAX_BYTES_BCRYPT = 72

def crear_hash(clave: str) -> str:
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")

def registrar_usuario(empleado_id: int, nombre: str, clave: str, sesion=None) -> int:
    exigir_admin(sesion)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("El empleado no existe.")
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta. El usuario ya existe.")
    if UsuarioDAO.buscar_por_empleado(empleado_id) is not None:
        raise ValueError("Este empleado ya cuenta con un usuario asignado.")

    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    return UsuarioDAO.insertar(usuario)

def autenticar(nombre: str, clave: str) -> dict | None:
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None

    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None:
        return None

    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None

    return {"id": cuenta.id, "empleado_id": cuenta.empleado_id, "nombre_usuario": cuenta.nombre_usuario, "rol": cuenta.rol}
