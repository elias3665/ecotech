from servicios.permisos import exigir_admin
from datetime import date
import math

from dominio.registrotrabajo import RegistroTrabajo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registrotrabajo_dao import RegistroTrabajoDAO

def registrar_horas():
    print("\n--- ASIGNACIÓN DE TRABAJO A PROYECTOS ---")
    id_emp_txt = input("ID del Empleado: ").strip()
    id_proy = input("Código del Proyecto: ").strip()

    if not id_emp_txt.isdigit() or not id_proy:
        print("[Validación] Datos de entrada incorrectos.")
        return
    try:
        empleado = EmpleadoDAO.buscar_por_id(int(id_emp_txt))
        proyecto = ProyectoDAO.buscar_por_id(id_proy)
    except Exception as e:
        print(f"No se pudieron consultar las entidades relacionadas: {e}")
        return

    if not empleado:
        print("Error: El empleado ingresado no existe en los registros.")
        return
    if not proyecto:
        print("Error: El proyecto ingresado no existe en los registros.")
        return

    fecha = input("Fecha del trabajo (AAAA-MM-DD): ").strip()
    try:
        if date.fromisoformat(fecha).isoformat() != fecha:
            raise ValueError
    except ValueError:
        print("[Validación] La fecha debe tener el formato AAAA-MM-DD y ser válida.")
        return
    try:
        horas = float(input("Cantidad de horas dedicadas: "))
    except ValueError:
        print("[Validación] Las horas deben ser un valor numérico válido.")
        return
    if not math.isfinite(horas) or horas <= 0:
        print("[Validación] Las horas deben ser un número mayor que cero.")
        return

    desc = input("Descripción de la tarea realizada: ").strip()
    if not desc:
        print("[Validación] La descripción es obligatoria.")
        return

    try:
        nuevo_registro = RegistroTrabajo(empleado=empleado, proyecto=proyecto,
                                            fecha=fecha, horas=horas, descripcion=desc)
        RegistroTrabajoDAO.insertar(nuevo_registro)
        print("Horas de trabajo imputadas y asociadas correctamente.")
    except Exception as e:
        print(f"Fallo en la persistencia transaccional: {e}")

def listar_registros():
    print("\n--- BITÁCORA DE TRABAJO GLOBAL ---")
    try:
        lista = RegistroTrabajoDAO.listar_completo()
        if not lista:
            print("No hay registros de horas trabajadas.")
            return
        for r in lista:
            print(r.mostrar_detalle())
    except Exception as e:
        print(f"No se pudieron listar los registros de trabajo: {e}")

def menu_registro(sesion=None):
    exigir_admin(sesion)
    while True:
        print("\n=== MENÚ REGISTROS DE TIEMPO ===")
        print("1. Imputar Horas de Trabajo (Asociar Empleado -> Proyecto)")
        print("2. Ver Bitácora de Horas Completa")
        print("0. Volver")
        opc = input("Selección: ").strip()
        if opc == "1": registrar_horas()
        elif opc == "2": listar_registros()
        elif opc == "0": break
