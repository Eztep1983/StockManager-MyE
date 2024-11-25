from config import config
from flask_mysqldb import MySQL
import logging
mysql=MySQL()

class Producto:
    def __init__(self, identificador_p, nombre, descripcion, precio, stock, id_proveedor, id_categoria):
        self.identificador_p = identificador_p
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.id_categoria=id_categoria
        self.id_proveedor=id_proveedor

    
def obtener_lista_productos():
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

def crear_producto(nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO productos (nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(nombre, descripcion, precio, stock, fecha_ingreso, id_proveedor, id_categoria))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback() 
        cursor.close()
        print("Error al añadir el producto", str(e))
        return False 
    

def actualizar_producto(identificador_p, nombre, descripcion, precio, stock):
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
        print("Error al actualizar el producto:", e)
        return False

def eliminar_productos(prd_id):
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


def ingresar_categoria(category):
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = 'INSERT INTO categorias_productos(nombre)VALUES (%s)'
            cursor.execute(sql,(category,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.error("Error al añadir la categoria: %s", str(e))

