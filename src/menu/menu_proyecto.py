from servicios.permisos import exigir_admin
from datetime import date

from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO

def mostrar_submenu():
    print("\n--- GESTIÓN DE PROYECTOS ---")
    print("1. Crear Proyecto")
    print("2. Listar Proyectos")
    print("3. Actualizar Proyecto")
    print("4. Eliminar Proyecto")
    print("0. Volver al menú principal")

def _fecha_valida(fecha: str) -> bool:
    try:
        return date.fromisoformat(fecha).isoformat() == fecha
    except ValueError:
        return False

def crear():
    id_proy = input("Código/ID único del Proyecto: ").strip()
    nombre = input("Nombre del Proyecto: ").strip()
    fecha = input("Fecha Inicio (AAAA-MM-DD): ").strip()

    if not id_proy or len(id_proy) > 50 or not nombre or len(nombre) > 100 or not _fecha_valida(fecha):
        print("[Validación] Ingrese un código (máximo 50 caracteres), nombre y fecha válida (AAAA-MM-DD).")
        return

    try:
        ProyectoDAO.insertar(Proyecto(id_proyecto=id_proy, nombre=nombre, fecha_inicio=fecha))
        print("Proyecto guardado de manera exitosa.")
    except Exception as e:
        print(f"No se pudo guardar el proyecto. Error: {e}")

def listar():
    try:
        proyectos = ProyectoDAO.listar()
        if not proyectos:
            print("No hay proyectos registrados.")
            return
        for p in proyectos:
            print(f"Código: {p.id_proyecto} | Proyecto: {p.nombre} | Inicio: {p.fecha_inicio}")
    except Exception as e:
        print(f"No se pudieron listar los proyectos: {e}")

def actualizar():
    id_proy = input("Código del proyecto a actualizar: ").strip()
    if not id_proy:
        print("[Validación] El código es obligatorio.")
        return
    try:
        existente = ProyectoDAO.buscar_por_id(id_proy)
        if existente is None:
            print("Proyecto no registrado.")
            return
        nombre = input(f"Nombre [{existente.nombre}]: ").strip()
        fecha = input(f"Fecha inicio [{existente.fecha_inicio}]: ").strip()
        if not nombre or len(nombre) > 100 or not _fecha_valida(fecha):
            print("[Validación] Ingrese un nombre (máximo 100 caracteres) y una fecha válida (AAAA-MM-DD).")
            return
        actualizado = ProyectoDAO.actualizar(
            Proyecto(id_proyecto=id_proy, nombre=nombre, fecha_inicio=fecha)
        )
        print("Proyecto actualizado." if actualizado else "No se realizaron cambios.")
    except Exception as e:
        print(f"No se pudo actualizar el proyecto: {e}")

def eliminar():
    id_proy = input("Código del proyecto a eliminar: ").strip()
    if not id_proy:
        print("[Validación] El código es obligatorio.")
        return
    if input("¿Confirma la eliminación? (s/n): ").strip().lower() != "s":
        print("Eliminación cancelada.")
        return
    try:
        eliminado = ProyectoDAO.eliminar(id_proy)
        print("Proyecto eliminado." if eliminado else "Proyecto no registrado.")
    except Exception as e:
        print(f"No se pudo eliminar el proyecto: {e}")

def menu_proyecto(sesion=None):
    exigir_admin(sesion)
    while True:
        mostrar_submenu()
        opc = input("Seleccione una opción: ").strip()
        if opc == "1": crear()
        elif opc == "2": listar()
        elif opc == "3": actualizar()
        elif opc == "4": eliminar()
        elif opc == "0": break
        else: print("Opción inválida.")
