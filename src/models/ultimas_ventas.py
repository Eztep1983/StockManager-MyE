from flask_mysqldb import MySQL
from config import config
from flask import logging
mysql = MySQL()
development_config = config['development']

def obtener_ultimas_ventas():
    """
    Obtiene las últimas 10 ventas realizadas desde la base de datos, incluyendo los detalles de cada venta, 
    como el nombre del producto, cantidad, monto total de la venta, el cliente y la fecha/hora de pago.

    Returns:
        list[dict]: Lista de diccionarios con los detalles de las últimas 10 ventas.
    """
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = """
                SELECT 
                    dv.id_detalles,
                    v.id_venta,
                    dv.id_producto,
                    p.nombre AS nombre_producto,
                    dv.cantidad,
                    dv.precio_unitario,
                    dv.descripcion,
                    pa.fecha_pago,
                    pa.hora_pago,
                    pa.monto,
                    v.id_cliente,
                    c.nombres AS nombre_cliente, -- Agregamos el nombre del cliente
                    v.fecha_venta,
                    v.hora_venta
                FROM detalles_ventas dv
                JOIN ventas v ON dv.id_venta = v.id_venta
                JOIN pagos pa ON v.id_venta = pa.id_venta
                JOIN productos p ON dv.id_producto = p.identificador_p -- Reemplazar con el nombre correcto
                JOIN clientes c ON v.id_cliente = c.identificador_c -- Relacionar con la tabla de clientes
                ORDER BY pa.fecha_pago DESC, pa.hora_pago DESC
                LIMIT 10; -- Limitar a las últimas 10 ventas
        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Procesar los resultados
        ultimas_ventas = []
        for row in rows:
            ultimas_ventas.append({
                "id_detalles": row[0],
                "id_venta": row[1],
                "id_producto": row[2],
                "nombre_producto": row[3],
                "cantidad": row[4],
                "precio_unitario": row[5],
                "descripcion": row[6],
                "fecha_pago": row[7],
                "hora_pago": row[8],
                "monto": row[9],
                "id_cliente": row[10],
                "nombre_cliente": row[11],
                "fecha_venta": row[12],
                "hora_venta": row[13],
            })
        
        return ultimas_ventas

    except Exception as e:
        print(f"No se ha podido obtener las últimas ventas: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
