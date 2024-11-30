from flask_mysqldb import MySQL
from config import config
from flask import logging

mysql = MySQL()
development_config = config['development']

#CLASE PARA VENTAS DE LA EMPRESA 

class Venta:
    """
    Representa una venta realizada en el sistema.

    Attributes:
        id_venta (int): Identificador único de la venta.
        id_usuario (int): Identificador del usuario que realizó la venta.
        fecha_venta (str): Fecha en la que se realizó la venta.
        id_cliente (int): Identificador del cliente asociado a la venta.
        hora (str): Hora en la que se realizó la venta.
    """
    def __init__(self, id_venta, id_usuario, fecha_venta, id_cliente, hora_venta):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.fecha_venta = fecha_venta
        self.id_cliente = id_cliente
        self.hora = hora_venta
# METODO PARA OBTENER VENTAS
def obtener_ventas():
    """
    Obtiene todas las ventas registradas en el sistema, incluyendo información
    adicional sobre los clientes y usuarios asociados.

    Returns:
        list[dict]: Una lista de diccionarios que representan las ventas. 
        Cada diccionario contiene:
            - id_venta: ID de la venta.
            - id_usuario: ID del usuario que realizó la venta.
            - fecha_venta: Fecha de la venta.
            - id_cliente: ID del cliente asociado.
            - nombre_cliente: Nombre del cliente asociado.
            - nombre_usuario: Nombre del usuario que realizó la venta.
            - hora: Hora de la venta.

    Raises:
        Exception: Si ocurre algún error durante la consulta.

    Notes:
        - Se realiza un JOIN para obtener los nombres de clientes y usuarios 
          relacionados con cada venta.
    """
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        sql = """
                SELECT 
                    v.id_venta, 
                    v.id_usuario, 
                    v.fecha_venta, 
                    v.hora_venta, 
                    c.identificador_c AS id_cliente, 
                    c.nombres AS nombre_cliente, 
                    u.fullname AS nombre_usuario
                FROM 
                    ventas v
                JOIN 
                    clientes c ON v.id_cliente = c.identificador_c
                JOIN 
                    users u ON v.id_usuario = u.id_trabajador;

        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Depuración: imprime cuántas filas se obtuvieron
        print(f"Filas obtenidas: {len(rows)}")  # Depurar cantidad de ventas obtenidas

        ventas = []
        for row in rows:
            id_venta, id_usuario, fecha_venta, id_cliente, nombre_cliente, nombre_usuario, hora = row
            venta = {
                'id_venta': id_venta,
                'id_usuario': id_usuario,
                'fecha_venta': fecha_venta,
                'id_cliente': id_cliente,
                'nombre_cliente': nombre_cliente,
                'nombre_usuario': nombre_usuario,
                'hora': hora
            }
            ventas.append(venta)

        cursor.close()
        return ventas
    except Exception as e:
        logging.error("Error al mostrar las ventas", str(e))
        print(f"Error al mostrar las ventas: {e}")  
        return []


def eliminar_venta(id_venta):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "DELETE FROM ventas WHERE id = %s"
        cursor.execute(sql, (id_venta,))
        conn.commit()  
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()  
        cursor.close()
        logging.error("Error al eliminar la venta", str(e))
        print(f"Error al eliminar la venta: {str(e)}")
        return False
