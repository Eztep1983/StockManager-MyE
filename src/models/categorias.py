from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

class Categoria:
    def __init__(self, id, nombre):
        self.id= id
        self.nombre=nombre

def añadir_categoria(nombre):
    conn=mysql.connection
    cursor=conn.cursor()
    try:
        sql="INSERT INTO categorias_productos (nombre) VALUES (%s) "
        cursor.execute(sql, (nombre))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al añadadir el proveedor:", str(e))
        return False

def obtener_categorias():
    conn=mysql.connection
    cursor=conn.cursor()
    try:
        sql="SELECT id, nombre FROM categorias_productos"
        cursor.execute(sql)
        categorias=[]
        for row in cursor.fetchall():
            id, nombre = row
            categoria= Categoria(id, nombre)
            categorias.append(categoria)
            cursor.close()
        return categorias
    except Exception as e:
        print("Error al obtener la lista de categorias")


