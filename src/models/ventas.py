from flask_mysqldb import MySQL
from config import config
import logging


mysql = MySQL()
development_config = config['development']


class Venta:
    def __init__(self, id, id_usuario, cantidad, fecha_venta, id_cliente):
        self.id = id
        self.id_usuario = id_usuario
        self.cantidad = cantidad
        self.fecha_venta = fecha_venta
        self.id_cliente = id_cliente


def obtener_ventas():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = "SELECT id, id_usuario, cantidad, fecha_venta, id_cliente FROM ventas"
    cursor.execute(sql)
    Ventas = []
    for row in cursor.fetchall():
        id, id_producto, id_usuario, cantidad, fecha_venta, id_cliente = row
        ventas = Ventas(id, id_producto, id_usuario, cantidad, fecha_venta, id_cliente)
        Ventas.append(ventas)
    cursor.close()
    return Ventas
