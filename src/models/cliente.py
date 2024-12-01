from flask_mysqldb import MySQL
from config import config
import logging

mysql = MySQL()
development_config = config['development']

class Cliente:
    """
    Representa un cliente en el sistema.

    Attributes:
        cedula (str): Cédula del cliente.
        nombres (str): Nombres del cliente.
        apellidos (str): Apellidos del cliente.
        direccion (str): Dirección del cliente.
        telefono (str): Teléfono del cliente.
        correo_electronico (str): Correo electrónico del cliente.
        identificador_c (int): Identificador único del cliente.
    """
    def __init__(self, cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c):
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.identificador_c = identificador_c
            
def obtener_lista_clientes():
    """
    Obtiene la lista de todos los clientes registrados en la base de datos.

    Returns:
        list[Cliente]: Una lista de instancias de la clase `Cliente` con los datos de cada cliente.

    Raises:
        Exception: Si ocurre un error al intentar obtener la lista de clientes.
    """
    try: 
        conn = mysql.connection
        cursor = conn.cursor()
        sql = 'SELECT cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c FROM clientes'
        cursor.execute(sql)
        clientes = []
        for row in cursor.fetchall():
            cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c = row
            cliente = Cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c )
            clientes.append(cliente)
        cursor.close()
        return clientes
    except Exception as e:
        logging.error("Error al añadir cliente:", str(e))
        return None


def añadir_cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico):
    """
    Añade un nuevo cliente a la base de datos.

    Args:
        cedula (str): Cédula del cliente.
        nombres (str): Nombres del cliente.
        apellidos (str): Apellidos del cliente.
        direccion (str): Dirección del cliente.
        telefono (str): Teléfono del cliente.
        correo_electronico (str): Correo electrónico del cliente.

    Returns:
        bool: `True` si el cliente fue añadido exitosamente, `False` en caso de error.

    Raises:
        Exception: Si ocurre un error durante la inserción del cliente.
    """
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO clientes (cedula, nombres, apellidos, direccion, telefono, correo_electronico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (cedula, nombres, apellidos, direccion, telefono, correo_electronico))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        logging.error("Error al añadir cliente:", str(e))
        print("Error al añadir cliente:", str(e))
        return False
    
def actualizar_cliente(identificador_c ,nombres, apellidos, direccion, telefono, correo_electronico, cedula):
    """
    Actualiza los datos de un cliente en la base de datos.

    Args:
        identificador_c (int): Identificador único del cliente a actualizar.
        nombres (str): Nuevos nombres del cliente.
        apellidos (str): Nuevos apellidos del cliente.
        direccion (str): Nueva dirección del cliente.
        telefono (str): Nuevo teléfono del cliente.
        correo_electronico (str): Nuevo correo electrónico del cliente.
        cedula (str): Nueva cédula del cliente.

    Returns:
        bool: `True` si el cliente fue actualizado exitosamente, `False` en caso de error.

    Raises:
        Exception: Si ocurre un error durante la actualización del cliente.
    """
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nombres=%s, apellidos=%s, direccion=%s, telefono=%s, correo_electronico=%s, cedula= %s WHERE identificador_c=%s"
        cursor.execute(sql,(nombres, apellidos, direccion, telefono, correo_electronico, cedula, identificador_c))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        logging.error("Error al actualizar cliente:", str(e))
        print("Error al actualizar cliente:", str(e))
        return False


def eliminarr_client(cliente_id):
    """
    Elimina un cliente de la base de datos.

    Args:
        cliente_id (int): Identificador único del cliente a eliminar.

    Returns:
        bool: `True` si el cliente fue eliminado exitosamente, `False` en caso de error.

    Raises:
        Exception: Si ocurre un error durante la eliminación del cliente.
    """
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = "DELETE FROM clientes WHERE identificador_c = %s"
            cursor.execute(sql, (cliente_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.error("Error al eliminar el Cliente: %s", str(e))
        return False
    
    
def mostrar_compas_cliente(cliente_id):
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = """ 
                SELECT 
                    v.id_venta AS id_venta,
                    v.fecha_venta AS fecha_venta,
                    dv.id_producto AS id_producto,
                    p.nombre AS producto,
                    dv.cantidad AS cantidad_comprada,
                    dv.precio_unitario AS precio_unitario,
                    (dv.cantidad * dv.precio_unitario) AS total_por_producto
                FROM ventas v
                INNER JOIN detalles_ventas dv ON v.id_venta = dv.id_venta
                INNER JOIN productos p ON dv.id_producto = p.identificador_p
                WHERE v.id_cliente = %s
                ORDER BY v.fecha_venta ASC;
            """

            cursor.execute(sql, (cliente_id,))
            compras = cursor.fetchall()
            if not compras:
                return []

            # Formatear las compras para que tenga un formato más legible y útil
            compras_formateadas = []
            for compra in compras:
                compras_formateadas.append({
                    'id_venta': compra[0],
                    'fecha_venta': compra[1],
                    'producto': compra[3],
                    'cantidad_comprada': compra[4],
                    'precio_unitario': compra[5],
                    'total_por_producto': compra[6]
                })

            return compras_formateadas
    except Exception as e:
        logging.error("Error al obtener las compras del cliente: %s", str(e))
        return None
