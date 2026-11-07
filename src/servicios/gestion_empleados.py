from servicios.permisos import exigir_admin
from persistencia.empleado_dao import EmpleadoDAO

def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()

def buscar(sesion, empleado_id):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(empleado_id)

def crear(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.insertar(empleado)

def actualizar(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.actualizar(empleado)

def eliminar(sesion, empleado_id):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(empleado_id)
