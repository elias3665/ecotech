from servicios.permisos import exigir_admin
from dominio.empleado import Empleado
from entradas import pedir_dato
from servicios import gestion_empleados

def mostrar_menu():
    print("\n--- GESTIÓN DE EMPLEADOS ---")
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado por ID")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("0. Volver al menú principal")

def _id_positivo(valor):
    numero = int(valor)
    if numero <= 0:
        raise ValueError("El ID debe ser positivo.")
    return numero

def registrar(sesion):
    exigir_admin(sesion)

    nombre = pedir_dato("Nombre: ", Empleado.validar_nombre)
    correo = pedir_dato("Correo: ", Empleado.validar_correo)
    try:
        emp = gestion_empleados.crear(sesion, Empleado(nombre, correo))
        print(f"Empleado registrado correctamente. ID: {emp.id}")
    except Exception as error:
        print(f"No fue posible guardar el empleado: {error}")

def listar(sesion):
    exigir_admin(sesion)
    try:
        empleados = gestion_empleados.listar_todos(sesion)
        if not empleados:
            print("No hay empleados registrados.")
        for empleado in empleados:
            print(f"ID: {empleado.id} | {empleado.mostrar_datos()}")
    except Exception as error:
        print(f"No se pudieron listar los empleados: {error}")

def buscar(sesion):
    exigir_admin(sesion)
    empleado_id = pedir_dato("Ingrese ID a buscar: ", _id_positivo)
    try:
        empleado = gestion_empleados.buscar(sesion, empleado_id)
        if empleado:
            print(f"Encontrado -> Nombre: {empleado.nombre}, Email: {empleado.email}")
        else:
            print("Empleado no registrado.")
    except Exception as error:
        print(f"No se pudo buscar el empleado: {error}")

def actualizar(sesion):
    exigir_admin(sesion)
    empleado_id = pedir_dato("ID del empleado a actualizar: ", _id_positivo)
    try:
        existente = gestion_empleados.buscar(sesion, empleado_id)
        if existente is None:
            print("Empleado no registrado.")
            return
    except Exception as error:
        print(f"No se pudo buscar el empleado: {error}")
        return

    nombre = pedir_dato(
        f"Nombre [{existente.nombre}]: ",
        lambda dato: Empleado.validar_nombre(dato if dato.strip() else existente.nombre)
    )
    correo = pedir_dato(
        f"Correo [{existente.email}]: ",
        lambda dato: Empleado.validar_correo(dato if dato.strip() else existente.email)
    )
    try:
        actualizado = gestion_empleados.actualizar(
            sesion, Empleado(nombre=nombre, email=correo,
                            id=existente.id, departamento_id=existente.departamento_id)
        )
        print("Empleado actualizado." if actualizado else "No se realizaron cambios.")
    except Exception as error:
        print(f"No fue posible guardar la actualización: {error}")

def eliminar(sesion):
    exigir_admin(sesion)
    empleado_id = pedir_dato("ID del empleado a eliminar: ", _id_positivo)
    if input("¿Confirma la eliminación? (s/n): ").strip().lower() != "s":
        print("Eliminación cancelada.")
        return
    try:
        eliminado = gestion_empleados.eliminar(sesion, empleado_id)
        print("Empleado eliminado." if eliminado else "Empleado no registrado.")
    except Exception as error:
        print(f"No se pudo eliminar el empleado: {error}")

def menu_empleado(sesion=None):
    exigir_admin(sesion)
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar(sesion)
        elif opcion == "2":
            listar(sesion)
        elif opcion == "3":
            buscar(sesion)
        elif opcion == "4":
            actualizar(sesion)
        elif opcion == "5":
            eliminar(sesion)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
