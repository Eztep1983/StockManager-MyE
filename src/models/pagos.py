from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

def añadir_facturacion(usuario, cliente, fecha_venta, hora_venta, productos, total, fecha_pago, hora_pago, nota):
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

        # Paso 2: Insertar en `detalles_ventas` y verificar stock
        sql_detalles = """
            INSERT INTO detalles_ventas (id_venta, id_producto, cantidad, precio_unitario, descripcion)
            VALUES (%s, %s, %s, %s, %s);
        """
        
        for producto in productos:
            # Verificar si hay suficiente stock
            cursor.execute("SELECT nombre, stock FROM productos WHERE identificador_p = %s", (producto['id_producto'],))
            producto_data = cursor.fetchone()

            if not producto_data:
                return {"status": "error", "message": f"Producto con ID {producto['id_producto']} no encontrado."}
            
            nombre_producto, stock_disponible = producto_data

            if producto['cantidad'] > stock_disponible:
                return {"status": "error", "message": f"Stock insuficiente para el producto {nombre_producto} (ID: {producto['id_producto']}). Stock disponible: {stock_disponible}."}

            # Insertar en `detalles_ventas`
            cursor.execute(sql_detalles, (
                id_venta,
                producto['id_producto'],
                producto['cantidad'],
                producto['precio_unitario'],
                producto.get('descripcion', '')  # Valor por defecto si no hay descripción
            ))

            # Actualizar el stock del producto
            nuevo_stock = stock_disponible - producto['cantidad']
            cursor.execute("UPDATE productos SET stock = %s WHERE identificador_p = %s", (nuevo_stock, producto['id_producto']))

        # Paso 3: Insertar los datos en la tabla `pagos`
        sql_pago = """
            INSERT INTO pagos (id_venta, monto, fecha_pago, id_cliente, hora_pago, nota)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql_pago, (id_venta, total, fecha_pago, cliente, hora_pago, nota))

        # Confirmar la transacción
        conn.commit()
        return {"status": "success", "message": "Factura procesada correctamente"}
    except Exception as e:
        conn.rollback()  # Revertir la transacción en caso de error
        print(f"Error al procesar la facturación. Venta: {usuario}, Cliente: {cliente}, Total: {total}")
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
