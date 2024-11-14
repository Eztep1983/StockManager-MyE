from flask_mysqldb import MySQL
from config import config


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

def metodo_pago():  # Obtener los métodos de pago únicos para facturación
    try: 
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "SELECT DISTINCT metodo_pago FROM pagos"
        cursor.execute(sql)
        Metodo = [row[0] for row in cursor.fetchall()]  # Extraer el primer elemento de cada fila (el método de pago)
        cursor.close()
        return Metodo
    except Exception as e:
        print("Error al obtener el metodo de pago", str(e))
        return []
