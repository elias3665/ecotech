from typing import Optional

class Empleado:

    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_CORREO = 6
    MAX_CORREO = 254

    def __init__(self, nombre: str, email: str, id: Optional[int] = None,
                 departamento_id: Optional[int] = None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.departamento_id = departamento_id

    @classmethod
    def validar_nombre(cls, nombre: str) -> str:
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError(
                f"El nombre debe tener entre {cls.MIN_NOMBRE} y {cls.MAX_NOMBRE} caracteres."
            )
        return nombre

    @classmethod
    def validar_correo(cls, correo: str) -> str:
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto.")
        correo = correo.strip()
        if not cls.MIN_CORREO <= len(correo) <= cls.MAX_CORREO:
            raise ValueError("Correo fuera del largo permitido.")
        if any(c.isspace() for c in correo):
            raise ValueError("El correo no debe contener espacios.")
        if correo.count("@") != 1:
            raise ValueError("El correo debe contener un solo @.")
        usuario, dominio = correo.split("@")
        if not usuario or "." not in dominio:
            raise ValueError("Use un correo como nombre@empresa.cl.")
        if any(not parte for parte in dominio.split(".")):
            raise ValueError("El dominio contiene puntos inválidos.")
        return correo

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        if value is not None and (type(value) is not int or value <= 0):
            raise ValueError("El ID del empleado debe ser un número entero positivo.")
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        self._nombre = self.validar_nombre(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = self.validar_correo(value)

    @property
    def departamento_id(self) -> Optional[int]:
        return self._departamento_id

    @departamento_id.setter
    def departamento_id(self, value: Optional[int]) -> None:
        if value is not None and (type(value) is not int or value <= 0):
            raise ValueError("El ID del departamento debe ser positivo.")
        self._departamento_id = value

    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.email}"
