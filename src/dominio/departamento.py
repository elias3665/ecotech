from typing import Optional

class Departamento:

    def __init__(self, nombre: str, descripcion: str = "", gerente_id: Optional[int] = None,
                 id_dept: Optional[int] = None):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del departamento es obligatorio.")
        if not isinstance(descripcion, str):
            raise TypeError("La descripción del departamento debe ser texto.")
        if gerente_id is not None and (type(gerente_id) is not int or gerente_id <= 0):
            raise ValueError("El ID del gerente debe ser positivo.")
        if id_dept is not None and (type(id_dept) is not int or id_dept <= 0):
            raise ValueError("El ID del departamento debe ser positivo.")
        self.id_dept = id_dept
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.gerente_id = gerente_id
