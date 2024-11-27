from flask_mysqldb import MySQL
from config import config
from models.entities.user import User
from flask import logging
mysql = MySQL()
development_config = config['development']


def obtener_usuarios():
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
    