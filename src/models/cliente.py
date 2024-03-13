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
