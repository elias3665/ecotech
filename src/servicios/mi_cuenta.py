from servicios.permisos import exigir_sesion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registrotrabajo_dao import RegistroTrabajoDAO
from dominio.empleado import Empleado

def mi_ficha(sesion):
    exigir_sesion(sesion)
    return EmpleadoDAO.buscar_por_id(sesion["empleado_id"])

def actualizar_mi_ficha(sesion, nombre, correo):
    exigir_sesion(sesion)
    empleado = Empleado(nombre=nombre, email=correo, id=sesion["empleado_id"])
    return EmpleadoDAO.actualizar(empleado)

def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTrabajoDAO.listar_por_empleado(sesion["empleado_id"])
