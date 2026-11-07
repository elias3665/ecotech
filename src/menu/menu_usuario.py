import getpass
from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario, autenticar
from servicios.permisos import exigir_admin, exigir_sesion
from servicios.mi_cuenta import mi_ficha, actualizar_mi_ficha, mis_registros
from servicios.indicadores import consultar_indicador, obtener_historial
from dominio.usuario import Usuario
from dominio.empleado import Empleado

def solicitar_login():
    print("\n====== CONTROL DE ACCESO ECOTECH ======")
    nombre = input("Usuario: ")
    clave = getpass.getpass("Contraseña: ")
    try:
        sesion = autenticar(nombre, clave)
    except (ValueError, TypeError):
        sesion = None
    print("Sesión iniciada correctamente." if sesion else "Usuario o contraseña incorrectos.")
    return sesion

def solicitar_registro(sesion):
    exigir_admin(sesion)
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass.getpass)
        if clave != getpass.getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden.")
            return
        print("Cuenta creada con ID:", registrar_usuario(empleado_id, nombre, clave, sesion))
    except (ValueError, TypeError) as error:
        print("No se pudo registrar:", error)

def menu_indicadores(sesion):
    exigir_sesion(sesion)
    while True:
        print("\n--- INDICADORES ---\n1. Consultar dólar actualizado\n2. Ver historial guardado\n0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "0": return
        if opcion == "1":
            try:
                dato, origen, mensaje = consultar_indicador(sesion)
                print(mensaje)
                if dato:
                    print(f"Dólar: {dato.valor:.2f} {dato.unidad} | Fecha: {dato.fecha} | Origen: {origen} ({dato.fuente}) | Verificado: {dato.verificado_en}")
            except Exception as error:
                print("Error al consultar indicador:", error)
        elif opcion == "2":
            try:
                historial = obtener_historial(sesion)
                if not historial: print("Todavía no hay historial.")
                for dato in historial:
                    print(f"{dato.fecha}: {dato.valor:.2f} {dato.unidad} | Fuente: {dato.fuente} | Verificado: {dato.verificado_en}")
            except Exception as error:
                print("No se pudo consultar el historial:", error)
        else: print("Opción no válida.")

def menu_privado(sesion):
    exigir_sesion(sesion)
    from menu.menu_empleado import menu_empleado
    from menu.menu_proyecto import menu_proyecto
    from menu.menu_registro import menu_registro
    while True:
        admin = sesion["rol"] == "admin"
        print(f"\n===== ECOTECH | {sesion['nombre_usuario']} ({sesion['rol']}) =====")
        print("1. Mi ficha\n2. Modificar mi nombre y correo\n3. Mis registros\n4. Indicadores (API e historial)")
        if admin:
            print("5. Administrar empleados\n6. Registrar cuenta de empleado\n7. Proyectos\n8. Registros laborales del sistema")
        print("9. Cerrar sesión\n0. Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("9", "0"): return opcion
        try:
            if opcion == "1":
                emp = mi_ficha(sesion)
                print(emp.mostrar_datos() if emp else "No se encontró su ficha.")
            elif opcion == "2":
                emp = mi_ficha(sesion)
                if emp is None: print("No se encontró su ficha."); continue
                nombre = pedir_dato(
                    f"Nombre [{emp.nombre}]: ",
                    lambda valor: Empleado.validar_nombre(valor if valor.strip() else emp.nombre)
                )
                correo = pedir_dato(
                    f"Correo [{emp.email}]: ",
                    lambda valor: Empleado.validar_correo(valor if valor.strip() else emp.email)
                )
                print("Ficha actualizada." if actualizar_mi_ficha(sesion, nombre, correo) else "Sin cambios.")
            elif opcion == "3":
                registros = mis_registros(sesion)
                if not registros: print("No tiene registros de trabajo.")
                for r in registros: print(f"{r.fecha} | {r.horas} horas | {r.descripcion}")
            elif opcion == "4": menu_indicadores(sesion)
            elif opcion == "5" and admin: menu_empleado(sesion)
            elif opcion == "6" and admin: solicitar_registro(sesion)
            elif opcion == "7" and admin: menu_proyecto(sesion)
            elif opcion == "8" and admin: menu_registro(sesion)
            else: print("Opción no permitida.")
        except (PermissionError, ValueError, TypeError) as error:
            print(error)
