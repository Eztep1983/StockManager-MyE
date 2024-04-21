from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

class Cliente:
    def __init__(self, cedula, nombres, apellidos, direccion, telefono, correo_electronico):
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico
            
def obtener_lista_clientes():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = 'SELECT cedula, nombres, apellidos, direccion, telefono, correo_electronico FROM clientes'
    cursor.execute(sql)
    clientes = []
    for row in cursor.fetchall():
        cedula, nombres, apellidos, direccion, telefono, correo_electronico = row
        cliente = Cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico)
        clientes.append(cliente)
    cursor.close()
    return clientes


def añadir_cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO clientes (cedula, nombres, apellidos, direccion, telefono, correo_electronico) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (cedula, nombres, apellidos, direccion, telefono, correo_electronico))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al añadir cliente:", str(e))
        return False
    
def actualizr_cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nombres=%s, apellidos=%s, direccion=%s, telefono=%s, correo_electronico=%s WHERE cedula=%s"
        cursor.execute(sql, (nombres, apellidos, direccion, telefono, correo_electronico, cedula))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al actualizar cliente:", str(e))
        return False

def eliminar_cliente(cedula):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "DELETE FROM clientes WHERE cedula = %s"
        cursor.execute(sql, (cedula,))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al eliminar el Cliente", str(e))
        return False
