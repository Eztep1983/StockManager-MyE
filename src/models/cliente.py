from flask_mysqldb import MySQL
from config import config
import logging

mysql = MySQL()
development_config = config['development']

class Cliente:
    def __init__(self, cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c):
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.identificador_c = identificador_c
            
def obtener_lista_clientes():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = 'SELECT cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c FROM clientes'
    cursor.execute(sql)
    clientes = []
    for row in cursor.fetchall():
        cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c = row
        cliente = Cliente(cedula, nombres, apellidos, direccion, telefono, correo_electronico, identificador_c )
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
    
def actualizar_cliente(identificador_c ,nombres, apellidos, direccion, telefono, correo_electronico, cedula):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nombres=%s, apellidos=%s, direccion=%s, telefono=%s, correo_electronico=%s, cedula= %s WHERE identificador_c=%s"
        cursor.execute(sql, (nombres, apellidos, direccion, telefono, correo_electronico, cedula, identificador_c))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al actualizar cliente:", str(e))
        return False


def eliminarr_client(cliente_id):
    try:
        conn = mysql.connection
        with conn.cursor() as cursor:
            sql = "DELETE FROM clientes WHERE identificador_c = %s"
            cursor.execute(sql, (cliente_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.error("Error al eliminar el Cliente: %s", str(e))
        return False