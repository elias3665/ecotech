from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registrotrabajo import RegistroTrabajo
from dominio.usuario import Usuario
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registrotrabajo_dao import RegistroTrabajoDAO
from persistencia.usuario_dao import UsuarioDAO

def _asegurar_empleado(nombre, correo):
    empleado = EmpleadoDAO.buscar_por_correo(correo)
    if empleado:
        print(f"Empleado existente: {correo}")
        return empleado
    empleado = EmpleadoDAO.insertar(Empleado(nombre, correo))
    print(f"Empleado de prueba creado: {correo}")
    return empleado

def cargar_datos_semilla():
    print("\n=== SEMILLA ECOTECH ===")
    crear_tablas()

    ana = _asegurar_empleado("Ana Torres", "ana@ecotech.cl")
    carlos = _asegurar_empleado("Carlos Ruiz", "carlos@ecotech.cl")

    departamento = DepartamentoDAO.buscar_por_nombre("Operaciones EcoTech")
    if departamento is None:
        departamento = DepartamentoDAO.insertar(
            Departamento(nombre="Operaciones EcoTech", descripcion="Departamento de prueba")
        )
        print("Departamento de prueba creado.")
    else:
        print("Departamento de prueba existente.")

    if departamento.gerente_id is None:
        DepartamentoDAO.asignar_gerente(departamento.id_dept, ana.id)
    for empleado in (ana, carlos):
        if empleado.departamento_id is None:
            DepartamentoDAO.asignar_empleado(empleado.id, departamento.id_dept)

    codigo_proyecto = "ECO-DEMO-01"
    proyecto = ProyectoDAO.buscar_por_id(codigo_proyecto)
    if proyecto is None:
        proyecto = ProyectoDAO.insertar(
            Proyecto(codigo_proyecto, "Piloto EcoTech", "2026-10-01")
        )
        print("Proyecto de prueba creado.")
    else:
        print("Proyecto de prueba existente.")

    fecha, descripcion = "2026-10-02", "Planificación del proyecto de prueba"
    if not RegistroTrabajoDAO.existe(ana.id, codigo_proyecto, fecha, descripcion):
        RegistroTrabajoDAO.insertar(
            RegistroTrabajo(empleado=ana, proyecto=proyecto, fecha=fecha,
                            horas=4, descripcion=descripcion)
        )
        print("Registro de tiempo de prueba creado.")
    else:
        print("Registro de tiempo de prueba existente.")

    admin = UsuarioDAO.buscar_por_nombre("admin")
    if admin is None:

        from servicios.autenticacion import crear_hash
        cuenta = Usuario(
            nombre_usuario="admin", password_hash=crear_hash("admin123"),
            empleado_id=ana.id, rol="admin"
        )
        UsuarioDAO.insertar(cuenta)
        print("Cuenta inicial admin creada (clave de demostración: admin123).")
    else:
        print("La cuenta admin ya existe; se conserva su contraseña y rol.")
    print("=== SEMILLA FINALIZADA ===")

if __name__ == "__main__":
    cargar_datos_semilla()
