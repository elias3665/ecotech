from datetime import date
import math
import requests

URL_DOLAR = "https://mindicador.cl/api/dolar"

def obtener_datos():
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    respuesta.raise_for_status()
    return respuesta.json()

def extraer_primero(datos):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada de la API.")
    if datos.get("codigo") != "dolar":
        raise ValueError("El código del indicador no corresponde al dólar.")
    if datos.get("unidad_medida") != "Pesos":
        raise ValueError("La unidad del indicador no es la esperada.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("La API no entregó valores disponibles.")
    registro = serie[0]
    if not isinstance(registro, dict):
        raise ValueError("Registro de la API inválido.")
    fecha, valor = registro.get("fecha"), registro.get("valor")
    if not isinstance(fecha, str):
        raise ValueError("Fecha del indicador inválida.")
    try:
        fecha_iso = date.fromisoformat(fecha[:10]).isoformat()
    except ValueError as error:
        raise ValueError("Fecha del indicador inválida.") from error
    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError("Valor del indicador inválido.")
    return fecha_iso, valor
