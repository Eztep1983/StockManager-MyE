from flask import jsonify
from config import config
from flask_mysqldb import MySQL

mysql=MySQL()

class producto:
    def __init__(self, id, nombre, descripcion, precio, stock, id_categoria):
        self.id= id
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.id_categoria=id_categoria
        return
    
def obtener_lista_productos():
    conn = mysql.connection
    cursor = conn.cursor()
    sql= "SELECT id, nombre, descripcion, precio, stock, id_categoria FROM Productos"
    cursor.execute(sql)
    Productos=[]
    for row in cursor.fetchall():
        id, nombre, descripcion, precio, stock,id_categoria = row
        producto=producto(id, nombre, descripcion, precio, stock, id_categoria)
        Productos.append(producto)
        return
    
def obtener_productos_disponibles():
    productos = obtener_lista_productos()
    # Convertimos la lista de productos en un formato JSON y la devolvemos como respuesta
    return jsonify({"productos": [producto.__dict__ for producto in productos]})