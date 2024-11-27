from flask_mysqldb import MySQL
from config import config
from flask import logging
mysql = MySQL()
development_config = config['development']

class Categoria:
    def __init__(self, id, nombre):
        self.id= id
        self.nombre=nombre

def ingresar_categoria(category):
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = 'INSERT INTO categorias_productos(nombre) VALUES (%s)'
            cursor.execute(sql, (category,))
            categoria_id = cursor.lastrowid  
        conn.commit()
        return categoria_id 
    except Exception as e:
        conn.rollback()
        logging.error("Error al añadir la categoría: %s", str(e))
        return None  


def obtener_categorias():
    conn=mysql.connection
    cursor=conn.cursor()
    try:
        sql="SELECT id_categoria, nombre FROM categorias_productos"
        cursor.execute(sql)
        categorias=[]
        for row in cursor.fetchall():
            id, nombre = row
            categoria= Categoria(id, nombre)
            categorias.append(categoria)
            cursor.close()
        return categorias
    except Exception as e:
        logging.error("Error al obtener las categorias", str(e))
        print("Error al obtener la lista de categorias")


