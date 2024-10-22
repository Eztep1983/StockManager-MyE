from flask_mysqldb import MySQL
from config import config


mysql = MySQL()
development_config = config['development']

#CLASE PARA VENTAS DE LA EMPRESA 

class Venta:
    def __init__(self, id_venta, id_usuario, fecha_venta, id_cliente):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.fecha_venta = fecha_venta
        self.id_cliente = id_cliente

# METODO PARA OBTENER VENTAS
def obtener_ventas():
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        sql = """
            SELECT v.id_venta, v.id_usuario, v.fecha_venta, c.identificador_c AS id_cliente, c.nombres AS nombre_cliente, u.fullname AS nombre_usuario
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.identificador_c
            JOIN users u ON v.id_usuario = u.id_trabajador;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Depuración: imprime cuántas filas se obtuvieron
        print(f"Filas obtenidas: {len(rows)}")  # Depurar cantidad de ventas obtenidas

        ventas = []
        for row in rows:
            id_venta, id_usuario, fecha_venta, id_cliente, nombre_cliente, nombre_usuario = row
            venta = {
                'id_vemta': id_venta,
                'id_usuario': id_usuario,
                'fecha_venta': fecha_venta,
                'id_cliente': id_cliente,
                'nombre_cliente': nombre_cliente,
                'nombre_usuario': nombre_usuario
            }
            ventas.append(venta)

        cursor.close()
        return ventas
    except Exception as e:
        print(f"Error al mostrar las ventas: {e}")  # Agregar este mensaje de error
        return []


def eliminar_venta(id_venta):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        # Consulta SQL correcta para eliminar una venta
        sql = "DELETE FROM ventas WHERE id = %s"
        cursor.execute(sql, (id_venta,))

        conn.commit()  # Confirmar los cambios en la base de datos
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()  # Revertir cambios en caso de error
        cursor.close()
        print(f"Error al eliminar la venta: {str(e)}")
        return False
