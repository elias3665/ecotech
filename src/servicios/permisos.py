def exigir_sesion(sesion):
    if not isinstance(sesion, dict) or sesion.get("rol") not in ("admin", "empleado"):
        raise PermissionError("Debe iniciar una sesión válida.")
    if type(sesion.get("empleado_id")) is not int or sesion["empleado_id"] <= 0:
        raise PermissionError("Sesión inválida.")

def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "admin":
        raise PermissionError("Acción solo para administrador.")
