from persistencia.conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    motor = obtener_motor()
    try:
        if motor == "sqlite":
            cursor.execute("""CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                departamento_id INTEGER REFERENCES departamento(id)
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT NOT NULL DEFAULT '',
                gerente_empleado_id INTEGER REFERENCES empleado(id)
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS proyecto (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS registro_trabajo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL REFERENCES empleado(id) ON DELETE CASCADE,
                proyecto_id TEXT NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE,
                fecha TEXT NOT NULL,
                horas REAL NOT NULL,
                descripcion TEXT NOT NULL
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                id_empleado INTEGER NOT NULL UNIQUE REFERENCES empleado(id) ON DELETE CASCADE,
                rol TEXT NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado'))
            )""")
            cursor.execute("PRAGMA table_info(usuario)")
            if "rol" not in [fila[1] for fila in cursor.fetchall()]:
                cursor.execute("""ALTER TABLE usuario ADD COLUMN rol TEXT NOT NULL
                    DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado'))""")
            cursor.execute("PRAGMA table_info(empleado)")
            if "departamento_id" not in [fila[1] for fila in cursor.fetchall()]:
                cursor.execute("ALTER TABLE empleado ADD COLUMN departamento_id INTEGER REFERENCES departamento(id)")

            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_empleado_email ON empleado(email)")
            cursor.execute("""CREATE TABLE IF NOT EXISTS indicador_api (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuente TEXT NOT NULL, codigo TEXT NOT NULL, fecha TEXT NOT NULL,
                valor REAL NOT NULL, unidad TEXT NOT NULL, verificado_en TEXT NOT NULL,
                UNIQUE(fuente, codigo, fecha)
            )""")
        elif motor == "mysql":
            cursor.execute("""CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(254) NOT NULL UNIQUE
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                descripcion TEXT NOT NULL,
                gerente_empleado_id INT NULL,
                FOREIGN KEY (gerente_empleado_id) REFERENCES empleado(id)
            )""")
            cursor.execute("SHOW COLUMNS FROM empleado LIKE 'departamento_id'")
            if cursor.fetchone() is None:
                cursor.execute("ALTER TABLE empleado ADD COLUMN departamento_id INT NULL")
            cursor.execute("ALTER TABLE empleado MODIFY COLUMN email VARCHAR(254) NOT NULL")
            cursor.execute("SHOW INDEX FROM empleado WHERE Key_name = 'uq_empleado_email'")
            if cursor.fetchone() is None:
                cursor.execute("ALTER TABLE empleado ADD UNIQUE KEY uq_empleado_email (email)")
            cursor.execute("""CREATE TABLE IF NOT EXISTS proyecto (
                id VARCHAR(50) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                fecha_inicio VARCHAR(10) NOT NULL
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS registro_trabajo (
                id INT PRIMARY KEY AUTO_INCREMENT,
                empleado_id INT NOT NULL,
                proyecto_id VARCHAR(50) NOT NULL,
                fecha VARCHAR(10) NOT NULL,
                horas DECIMAL(5,2) NOT NULL,
                descripcion TEXT NOT NULL,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
            )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS usuario (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                id_empleado INT NOT NULL UNIQUE,
                rol VARCHAR(10) NOT NULL DEFAULT 'empleado',
                FOREIGN KEY (id_empleado) REFERENCES empleado(id) ON DELETE CASCADE
            )""")
            cursor.execute("SHOW COLUMNS FROM usuario LIKE 'rol'")
            if cursor.fetchone() is None:
                cursor.execute("ALTER TABLE usuario ADD COLUMN rol VARCHAR(10) NOT NULL DEFAULT 'empleado'")
            cursor.execute("""CREATE TABLE IF NOT EXISTS indicador_api (
                id INT PRIMARY KEY AUTO_INCREMENT,
                fuente VARCHAR(100) NOT NULL,
                codigo VARCHAR(40) NOT NULL,
                fecha VARCHAR(10) NOT NULL,
                valor DOUBLE NOT NULL,
                unidad VARCHAR(40) NOT NULL,
                verificado_en VARCHAR(40) NOT NULL,
                UNIQUE KEY uq_indicador (fuente, codigo, fecha)
            )""")
        else:
            raise ValueError(f"Motor no soportado: {motor}")
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
