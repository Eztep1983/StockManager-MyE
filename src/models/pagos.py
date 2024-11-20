from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

def añadir_facturacion(usuario, cliente, fecha_venta, hora_venta, productos, total, fecha_pago, hora_pago):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Iniciar transacción
        cursor.execute("START TRANSACTION;")

        # Paso 1: Insertar los datos en la tabla `ventas`
        sql_venta = """
            INSERT INTO ventas (id_usuario, id_cliente, fecha_venta, hora_venta)
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

        # Paso 3: Insertar los datos en la tabla `pagos`
        sql_pago = """
            INSERT INTO pagos (id_venta, monto, fecha_pago, id_cliente, hora_pago)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(sql_pago, (id_venta, total, fecha_pago, cliente, hora_pago))

        # Confirmar la transacción
        conn.commit()
        return {"status": "success", "message": "Factura procesada correctamente"}
    except Exception as e:
        conn.rollback()  # Revertir la transacción en caso de error
        print("Error al procesar la facturación:", str(e))
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
