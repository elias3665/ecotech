from typing import Optional
from datetime import datetime
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto

class RegistroTrabajo:
    def __init__(
        self,
        empleado: Empleado,
        proyecto: Proyecto,
        fecha: str,
        horas: float,
        descripcion: str,
        id_registro: Optional[int] = None,
    ):
        self.id = id_registro
        self.empleado = empleado
        self.proyecto = proyecto
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError("El ID de registro debe ser un número entero positivo.")
        self._id = value

    @property
    def empleado(self) -> Empleado:
        return self._empleado

    @empleado.setter
    def empleado(self, value: Empleado) -> None:
        if not isinstance(value, Empleado):
            raise TypeError("El campo empleado debe ser una instancia de la clase Empleado.")
        self._empleado = value

    @property
    def proyecto(self) -> Proyecto:
        return self._proyecto

    @proyecto.setter
    def proyecto(self, value: Proyecto) -> None:
        if not isinstance(value, Proyecto):
            raise TypeError("El campo proyecto debe ser una instancia de la clase Proyecto.")
        self._proyecto = value

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD.")
        self._fecha = value

    @property
    def horas(self) -> float:
        return self._horas

    @horas.setter
    def horas(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Las horas trabajadas deben ser un número mayor a cero.")
        if value > 24:
            raise ValueError("No se pueden registrar más de 24 horas de trabajo en un solo día.")
        self._horas = float(value)

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("La descripción del trabajo no puede estar vacía.")
        self._descripcion = value.strip()

    def mostrar_detalle(self) -> str:
        return f"[{self.fecha}] {self.empleado.nombre} -> {self.proyecto.nombre}: {self.horas} hrs ({self.descripcion})"
