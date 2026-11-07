import requests
from servicios.permisos import exigir_sesion
from servicios.api_dolar import obtener_datos
from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicador_dao import IndicadorDAO

def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        dato = DeserializadorIndicador.desde_api(obtener_datos())
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        respaldo = IndicadorDAO.ultimo()
        if respaldo is None:
            return None, "Sin respaldo", "API no disponible o respuesta inválida; no hay datos guardados."
        return respaldo, "BD local", "API no disponible o respuesta inválida; mostrando último respaldo."
    try:
        IndicadorDAO.guardar(dato)
        mensaje = "Dato guardado o actualizado correctamente."
    except Exception as error:
        mensaje = f"Dato obtenido de API, pero no pudo guardarse en BD: {error}"
    return dato, "API", mensaje

def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()
