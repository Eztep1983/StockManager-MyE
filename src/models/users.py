from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

class user:
    def __init__(self, id_trabajador, identification, fullname):
        self.id_trabajador = id_trabajador
        self.identification = identification
        self.fullname = fullname

def obtener_usuarios():
    try: 
        conn = mysql.connection
        cursor = conn.cursor()
        Usuarios= []
        sql = "SELECT id_trabajador, identification, fullname FROM users"
        cursor.execute(sql,)
        for row in cursor.fetchall():
            id_trabajador, identification, fullname = row
            usuario = user(id_trabajador, identification, fullname)
            Usuarios.append(usuario)
        cursor.close()
        return Usuarios
    except Exception as e:
        print("Error al obtener la lista de usuarios", str(e))
        return False
    