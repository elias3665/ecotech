from persistencia.crear_bd import crear_tablas
from menu.menu_usuario import solicitar_login, menu_privado

def main():
    try:
        crear_tablas()
    except Exception as error:
        print(f"Error al inicializar la base de datos: {error}")
        return
    while True:
        sesion = solicitar_login()
        if sesion is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0": return
            continue
        opcion = menu_privado(sesion)
        sesion = None
        if opcion == "0": return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    main()
