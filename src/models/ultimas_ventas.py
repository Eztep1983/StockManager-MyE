from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

def obtener_ultimas_ventas():
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
                    p.precio AS precio_producto, -- Precio del producto desde la tabla productos
                    dv.descripcion,
                    pa.fecha_pago,
                    pa.hora_pago,
                    pa.monto,
                    v.id_cliente,
                    v.fecha_venta,
                    v.hora_venta
                FROM detalles_ventas dv
                JOIN ventas v ON dv.id_venta = v.id_venta
                JOIN pagos pa ON v.id_venta = pa.id_venta
                JOIN productos p ON dv.id_producto = p.identificador_p -- Reemplazar con el nombre correcto
                ORDER BY pa.fecha_pago DESC, pa.hora_pago DESC
                LIMIT 10;

        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Depuración: verifica la cantidad de filas obtenidas
        print(f"Filas obtenidas: {len(rows)}")

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
                "precio_producto": row[6],  # Agregar el precio del producto
                "descripcion": row[7],
                "fecha_pago": row[8],
                "hora_pago": row[9],
                "monto": row[10],
                "id_cliente": row[11],
                "fecha_venta": row[12],
                "hora_venta": row[13],
            })
        
        return ultimas_ventas

    except Exception as e:
        print(f"No se ha podido obtener las últimas ventas: {e}")
        return []

    finally:
        cursor.close()
