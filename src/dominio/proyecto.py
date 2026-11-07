from datetime import datetime

class Proyecto:
    def __init__(self, id_proyecto: str, nombre: str, fecha_inicio: str):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio

    @property
    def id_proyecto(self) -> str:
        return self._id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("El ID del proyecto no puede estar vacío.")
        self._id_proyecto = str(value).strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")

        nombre_limpio = value.strip()

        if len(nombre_limpio) < 2 or len(nombre_limpio) > 20:
            raise ValueError("El nombre del proyecto debe tener entre 2 y 20 caracteres.")

        self._nombre = nombre_limpio

    @property
    def fecha_inicio(self) -> str:
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value: str) -> None:
        try:
            fecha_dt = datetime.strptime(value, "%Y-%m-%d")
            if fecha_dt.year < 2000 or fecha_dt.year > 2030:
                raise ValueError("El año de la fecha debe estar en un rango actual válido (entre el 2000 y 2030).")

        except ValueError as e:
            if "rango actual" in str(e):
                raise e
            raise ValueError("La fecha de inicio debe tener el formato YYYY-MM-DD y ser una fecha válida.")

        self._fecha_inicio = value
