from config import config
from flask_mysqldb import MySQL
import logging
mysql=MySQL()

class Producto:
    """
    Representa un producto en el sistema de inventario.

    Atributos:
        identificador_p (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        precio (float): Precio unitario del producto.
        stock (int): Cantidad de unidades disponibles en inventario.
        id_categoria (int): Identificador de la categoría a la que pertenece el producto.
        id_proveedor (int): Identificador del proveedor del producto.
    """

    def __init__(self, identificador_p, nombre, descripcion, precio, stock, id_proveedor, id_categoria):
        self.identificador_p = identificador_p
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.id_categoria=id_categoria
        self.id_proveedor=id_proveedor

    
def obtener_producto_id(prd_id):
    """
    Obtiene los detalles de un producto por su identificador.

    Args:
        prd_id (int): Identificador único del producto a consultar.

    Returns:
        dict: Detalles del producto si se encuentra, o None si no se encuentra.
    """
    try: 
        conn = mysql.connection
        cursor = conn.cursor()
        sql = """
        SELECT nombre, descripcion, precio, stock, id_categoria, id_proveedor 
        FROM productos 
        WHERE identificador_p = %s
        """
        cursor.execute(sql, (prd_id,))
        producto = cursor.fetchone()
    except Exception as e:
        logging.error("Error al obtener el producto con ID %s: %s", prd_id, str(e))
        producto = None
    finally:
        if cursor:
            cursor.close()
    return producto

def obtener_lista_productos():
    """
    Obtiene la lista de todos los productos en el inventario.

    Returns:
        list[Producto]: Lista de objetos Producto con los detalles de cada uno.
    """
    try:    
        conn = mysql.connection
        cursor = conn.cursor()
        sql= "SELECT identificador_p, nombre, descripcion, precio, stock, id_categoria, id_proveedor FROM productos"
        cursor.execute(sql)
        Productos=[]
        for row in cursor.fetchall():
            identificador_p, nombre, descripcion, precio, stock, id_categoria, id_provedor = row
            producto= Producto(identificador_p, nombre, descripcion, precio, stock, id_categoria, id_provedor)
            Productos.append(producto)
        cursor.close()
        return Productos
    except Exception as e:
        logging.error("Error al obtener la lista de productos", str(e))
        

def crear_producto(nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria):
    """
    Crea un nuevo producto en el inventario.

    Args:
        nombre (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        precio (float): Precio unitario del producto.
        stock (int): Cantidad inicial del producto en inventario.
        fecha_ingreso (str): Fecha en la que el producto fue ingresado al inventario.
        id_proveedor (int): Identificador del proveedor del producto.
        id_categoria (int): Identificador de la categoría del producto.

    Returns:
        bool: True si el producto fue creado con éxito, False si ocurrió un error.
    """
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "INSERT INTO productos (nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback() 
        cursor.close()
        logging.error("Error al crear el producto", str(e))
        return False 
    

def actualizar_producto(identificador_p, nombre, descripcion, precio, stock):
    """
    Actualiza los detalles de un producto existente.

    Args:
        identificador_p (int): Identificador único del producto a actualizar.
        nombre (str): Nuevo nombre del producto.
        descripcion (str): Nueva descripción del producto.
        precio (float): Nuevo precio unitario del producto.
        stock (int): Nuevo stock del producto.

    Returns:
        bool: True si el producto fue actualizado con éxito, False si ocurrió un error.
    """
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = """
        UPDATE productos 
        SET nombre= %s, descripcion= %s, precio= %s, stock= %s WHERE identificador_p = %s
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, identificador_p))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        logging.error("Error al actualizar el producto", str(e))
        return False


def eliminar_productos(prd_id):
    """
    Elimina un producto del inventario.

    Args:
        prd_id (int): Identificador único del producto a eliminar.

    Returns:
        bool: True si el producto fue eliminado con éxito, False si ocurrió un error.
    """
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = "DELETE FROM productos WHERE identificador_p = %s"
            cursor.execute(sql, (prd_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.error("Error al eliminar el Cliente: %s", str(e))
        return False