from flask import jsonify
from config import config
from flask_mysqldb import MySQL

mysql=MySQL()

class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock, id_categoria):
        self.id= id
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.id_categoria=id_categoria

    
def obtener_lista_productos():
    conn = mysql.connection
    cursor = conn.cursor()
    sql= "SELECT id, nombre, descripcion, precio, stock, id_categoria FROM productos"
    cursor.execute(sql)
    Productos=[]
    for row in cursor.fetchall():
        id, nombre, descripcion, precio, stock,id_categoria = row
        producto= Producto(id, nombre, descripcion, precio, stock, id_categoria)
        Productos.append(producto)
    cursor.close()
    return Productos
