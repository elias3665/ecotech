class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6
    ROLES = ("admin", "empleado")

    @classmethod
    def validar_rol(cls, rol):
        if rol not in cls.ROLES or not isinstance(rol, str):
            raise ValueError("Rol no permitido.")
        return rol

    def __init__(self, nombre_usuario: str, password_hash: str, empleado_id: int, id=None, rol="empleado"):
        if not isinstance(empleado_id, int) or empleado_id <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        self.id = id
        self.empleado_id = empleado_id
        self.nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self.password_hash = password_hash
        self.rol = self.validar_rol(rol)

    @classmethod
    def normalizar_usuario(cls, nombre: str) -> str:
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError("Usuario fuera del largo permitido.")
        if not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre

    @classmethod
    def validar_clave(cls, clave: str) -> str:
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(f"Use al menos {cls.MIN_CLAVE} caracteres.")
        return clave
