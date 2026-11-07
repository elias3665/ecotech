# EcoTech

EcoTech es un programa hecho en Python para llevar un registro de empleados, proyectos y trabajos realizados. También permite iniciar sesión con diferentes usuarios y consultar el valor del dólar desde una API.

La idea es que cada persona pueda usar solamente las opciones que le corresponden. Por ejemplo, el administrador puede gestionar empleados y crear cuentas, mientras que un empleado puede revisar y actualizar sus propios datos.

## Cómo abrirlo y ejecutarlo

Primero descomprime el ZIP y abre la carpeta `ecotech-eva2-main` en Visual Studio Code. Después abre la terminal desde **Terminal > Nueva terminal**.

Instala las librerías que necesita el proyecto:

```bash
python -m pip install -r requirements.txt
```

Para dejar listos los datos de prueba, ejecuta:

```bash
python src/semilla_bd.py
```

Y para iniciar el programa:

```bash
python src/main.py
```

La semilla se puede ejecutar más de una vez. Si los registros de ejemplo ya existen, los vuelve a utilizar en lugar de crearlos de nuevo.

## Qué se puede hacer en el programa

- Registrar empleados y validar sus nombres y correos antes de guardarlos.
- Crear proyectos y registrar trabajos realizados.
- Iniciar y cerrar sesión con una cuenta de usuario.
- Usar dos tipos de cuenta: administrador y empleado.
- Consultar y modificar los datos propios, sin acceder a los de otros empleados.
- Consultar el valor del dólar, guardar el resultado y ver el historial. Si la API falla, el programa intenta mostrar el último dato guardado y avisa que viene de la base de datos.

Las contraseñas se guardan con hash para que no queden escritas directamente en la base de datos.

## Usuarios de prueba

La semilla prepara una cuenta llamada `admin` si todavía no existe. Cuando la crea por primera vez, utiliza la contraseña de prueba `admin123`. Si esa cuenta ya existía, conserva la contraseña anterior.

El empleado Carlos Ruiz está incluido como dato de ejemplo, pero **no tiene una cuenta para iniciar sesión automáticamente**. Para crearla, entra como administrador y elige la opción **Registrar cuenta de empleado**. La cuenta nueva tendrá el rol de empleado.

Si una base antigua ya tenía la cuenta `admin` sin rol de administrador, puedes ejecutar `python src/migrar_admin.py` y revisar la confirmación que aparece en pantalla.

## Base de datos

El proyecto utiliza SQLite de manera predeterminada y guarda la información en `ecotech.db`. Se incluyen los datos que ya tenía el proyecto, así que conviene conservar una copia del ZIP anterior antes de hacer cambios importantes.

También hay código de conexión para MySQL, pero necesita una configuración aparte. Para probarlo de forma sencilla, puedes dejarlo con SQLite.

## Cómo comprobar que funciona

Hay pruebas en la carpeta `tests`. Para ejecutarlas desde la carpeta principal, usa:

```bash
python -m unittest discover -s tests -v
```

Estas pruebas revisan las validaciones, la base de datos, los permisos y el guardado de los indicadores. Además, puedes probar manualmente que un dato incorrecto vuelva a pedirse, que no se dupliquen los datos de la semilla y que cada usuario vea solamente sus opciones.

Con eso queda listo para seguir trabajando y agregar otras funcionalidades si hacen falta.
