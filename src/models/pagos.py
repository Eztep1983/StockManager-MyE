from flask_mysqldb import MySQL
from config import config
import logging

mysql = MySQL()
development_config= config['development']
class pagos:
    def __init__(self, id_pagos,id_venta, monto, metodo_pago, fecha_pago, id_cliente):
        self.id_pagos= id_pagos
        self.id_venta= id_venta
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago
        self.id_cliente = id_cliente

def facturacion_pago():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = ""
    cursor.execute(sql,())
    conn.commit()
    pagos = []



    