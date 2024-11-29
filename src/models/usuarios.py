from flask_mysqldb import MySQL
from config import config
from models.entities.user import User
from flask import logging
mysql = MySQL()
development_config = config['development']


def obtener_usuarios():
    """
    Obtiene la lista de usuarios de la base de datos.

    Returns:
        list: Una lista de objetos `User` que representan a los usuarios existentes.
        bool: Retorna `False` si ocurre un error durante la operación.

    Raises:
        Exception: Registra y maneja cualquier error que ocurra durante la consulta.
    """
    try: 
        conn = mysql.connection
        cursor = conn.cursor()
        Usuarios= []
        sql = "SELECT id_trabajador, identification, fullname FROM users"
        cursor.execute(sql,)
        for row in cursor.fetchall():
            id_trabajador, identification, fullname = row
            usuario = User(id_trabajador, identification, fullname)
            Usuarios.append(usuario)
        cursor.close()
        return Usuarios
    except Exception as e:
        logging.error("Error al obtener la lista de usuarios", str(e))
        print("Error al obtener la lista de usuarios", str(e))
        return False
    