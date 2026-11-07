from persistencia.crear_bd import crear_tablas
from persistencia.conexion import abrir_conexion, marcador_sql

def main():
    crear_tablas()
    conexion = abrir_conexion()
    try:
        cur = conexion.cursor()
        cur.execute(f"SELECT u.id,u.rol FROM usuario u JOIN empleado e ON e.id=u.id_empleado WHERE u.nombre_usuario={marcador_sql()} AND e.email={marcador_sql()}", ("admin", "ana@ecotech.cl"))
        fila = cur.fetchone()
        if not fila:
            print("No se encontró la cuenta inicial vinculada a Ana; no se cambió nada.")
            return
        if fila[1] == "admin":
            print("La cuenta inicial ya tiene rol admin.")
            return
        if input("¿Confirmar migración de la cuenta inicial admin? (s/n): ").strip().lower() != "s":
            return
        cur.execute(f"UPDATE usuario SET rol='admin' WHERE id={marcador_sql()}", (fila[0],))
        conexion.commit()
        print("Cuenta inicial actualizada a admin.")
    finally:
        conexion.close()

if __name__ == "__main__": main()
