from flask_mysqldb import MySQL
from config import config
import logging


mysql = MySQL()
development_config = config['development']


class Venta:
    def __init__(self, id, cedula_cliente, id_producto, id_usuario, cantidad, fecha_venta):
        self.id = id
        self.cedula_cliente = cedula_cliente
        self.id_producto = id_producto
        self.id_usuario = id_usuario
        self.cantidad = cantidad
        self.fecha_venta = fecha_venta


def obtener_ventas():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = "SELECT id, cedula_cliente, id_producto, id_usuario, cantidad, fecha_venta FROM ventas"
    cursor.execute(sql)
    Ventas = []
    for row in cursor.fetchall():
        id, cedula_cliente, id_producto, id_usuario, cantidad, fecha_venta = row
        ventas = Ventas(id, cedula_cliente, id_producto, id_usuario, cantidad, fecha_venta)
        Ventas.append(ventas)
    cursor.close()
    return Ventas
