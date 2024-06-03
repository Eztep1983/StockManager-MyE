from config import config
from flask_mysqldb import MySQL

mysql=MySQL()

class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock, id_proveedor, id_categoria):
        self.id= id
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.id_categoria=id_categoria
        self.id_proveedor=id_proveedor

    
def obtener_lista_productos():
    conn = mysql.connection
    cursor = conn.cursor()
    sql= "SELECT id, nombre, descripcion, precio, stock, id_categoria, id_proveedor FROM productos"
    cursor.execute(sql)
    Productos=[]
    for row in cursor.fetchall():
        id, nombre, descripcion, precio, stock, id_categoria, id_provedor = row
        producto= Producto(id, nombre, descripcion, precio, stock, id_categoria, id_provedor)
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

# def eliminar_products():
    #conn = mysql.connection
    #cursor = conn.cursor()
    #sql="DELETE FROM CLIENTES WHERE id = %s"
    #cursor.execute(sql)
