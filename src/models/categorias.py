from flask_mysqldb import MySQL
from config import config
from flask import logging
mysql = MySQL()
development_config = config['development']

class Categoria:
    """
    Representa una categoría de producto.

    Atributos:
        id (int): Identificador único de la categoría.
        nombre (str): Nombre de la categoría.
    """
    def __init__(self, id, nombre):
        self.id= id
        self.nombre=nombre

def ingresar_categoria(category):
    """
    Inserta una nueva categoría en la base de datos.

    Args:
        category (str): Nombre de la categoría a insertar.

    Returns:
        int: ID de la categoría recién creada si la operación fue exitosa.
        None: Si ocurre un error durante la inserción.

    Raises:
        Exception: Si ocurre un error inesperado durante la operación.
    """
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
    """
    Obtiene la lista de categorías de la base de datos.

    Returns:
        list: Una lista de objetos `Categoria` que representan las categorías existentes.

    Raises:
        Exception: Si ocurre un error durante la consulta de la base de datos.
    """
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


