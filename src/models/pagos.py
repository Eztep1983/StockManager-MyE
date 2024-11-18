from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

def añadir_facturacion(usuario, cliente, fecha_venta, hora_venta, productos, total, metodo_pago, fecha_pago, hora_pago):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Iniciar transacción
        cursor.execute("START TRANSACTION;")

        # Paso 1: Insertar en `ventas`
        sql_venta = """
            INSERT INTO ventas (id_usuario, id_cliente, fecha_venta, hora)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql_venta, (usuario, cliente, fecha_venta, hora_venta))
        id_venta = cursor.lastrowid  # Obtener el ID de la venta recién creada

        # Paso 2: Insertar en `detalles_ventas`
        sql_detalles = """
            INSERT INTO detalles_ventas (id_venta, id_producto, cantidad, precio_unitario, descripcion)
            VALUES (%s, %s, %s, %s, %s);
        """
        for producto in productos:
            cursor.execute(sql_detalles, (
                id_venta,
                producto['id_producto'],
                producto['cantidad'],
                producto['precio_unitario'],
                producto.get('descripcion', '')  # Valor por defecto si no hay descripción
            ))

        # Paso 3: Insertar en `pagos`
        sql_pago = """
            INSERT INTO pagos (id_venta, monto, metodo_pago, fecha_pago, id_cliente, hora)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql_pago, (id_venta, total, metodo_pago, fecha_pago, cliente, hora_pago))

        # Confirmar la transacción
        conn.commit()
        return {"status": "success", "message": "Factura procesada correctamente"}
    except Exception as e:
        conn.rollback()  # Revertir la transacción en caso de error
        print("Error al procesar la facturación:", str(e))
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()


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
