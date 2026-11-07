from datetime import date, datetime
import math

class Indicador:
    def __init__(self, fecha, valor, verificado_en=None, fuente="mindicador.cl"):
        if not isinstance(fecha, str):
            raise ValueError("Fecha inválida.")
        try:
            fecha = date.fromisoformat(fecha[:10]).isoformat()
        except ValueError as error:
            raise ValueError("Fecha inválida.") from error
        if type(valor) not in (float, int) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("Valor inválido.")
        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en or datetime.now().isoformat(timespec="seconds")
