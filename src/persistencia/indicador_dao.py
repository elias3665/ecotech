from persistencia.conexion import abrir_conexion, marcador_sql, obtener_motor
from dominio.indicador import Indicador

class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marca = marcador_sql()
            valores = (indicador.fuente, indicador.codigo, indicador.fecha, indicador.valor, indicador.unidad, indicador.verificado_en)
            if obtener_motor() == "sqlite":
                sql = f"""INSERT INTO indicador_api (fuente,codigo,fecha,valor,unidad,verificado_en)
                    VALUES ({','.join([marca]*6)}) ON CONFLICT(fuente,codigo,fecha) DO UPDATE SET
                    valor=excluded.valor, unidad=excluded.unidad, verificado_en=excluded.verificado_en"""
            else:
                sql = f"""INSERT INTO indicador_api (fuente,codigo,fecha,valor,unidad,verificado_en)
                    VALUES ({','.join([marca]*6)}) ON DUPLICATE KEY UPDATE
                    valor=VALUES(valor), unidad=VALUES(unidad), verificado_en=VALUES(verificado_en)"""
            cursor.execute(sql, valores)
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT fecha,valor,verificado_en,fuente FROM indicador_api WHERE codigo='dolar' ORDER BY fecha DESC")
            return [Indicador(fecha=f[0], valor=f[1], verificado_en=f[2], fuente=f[3]) for f in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def ultimo():
        datos = IndicadorDAO.listar()
        return datos[0] if datos else None
