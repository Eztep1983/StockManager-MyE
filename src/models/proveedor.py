from flask_mysqldb import MySQL
from config import config

mysql = MySQL()
development_config = config['development']

class Proveedor:
    def __init__(self, nombre_empresa, direccion, telefono, correo_electronico, id_proveedor):
        self.nombre_empresa = nombre_empresa
        self.direccion = direccion
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.id_proveedor = id_proveedor  

def obtener_proveedores():
    conn = mysql.connection
    cursor = conn.cursor()
    sql = "SELECT id_proveedor, nombre_empresa, direccion, telefono, correo_electronico FROM proveedores"
    cursor.execute(sql)
    proveedores = []
    for row in cursor.fetchall():
        id_proveedor, nombre_empresa, direccion, telefono, correo_electronico = row
        proveedor = Proveedor(nombre_empresa, direccion, telefono, correo_electronico, id_proveedor)
        proveedores.append(proveedor)
    cursor.close()
    return proveedores



def añadir_proveedor(nombre_empresa, direccion, telefono, correo_electronico):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO proveedores (nombre_empresa, direccion, telefono, correo_electronico) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre_empresa, direccion, telefono, correo_electronico))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al añadadir el proveedor:", str(e))
        return False
    
def eliminar_proveedor(id_proveedor):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        print("SQL:", sql)  # Agregar esta línea para imprimir la consulta SQL
        cursor.execute(sql, (id_proveedor))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al eliminar el proveedor:", str(e))
        return False
 
def actualizar_proveedore(nombre_empresa, direccion, telefono, correo_electronico, id_proveedor):
    try:
        conn=mysql.connection
        cursor=conn.cursor()
        sql="UPDATE proveedores SET nombre_empresa=%s, direccion=%s, telefono=%s, correo_electronico=%s WHERE id_proveedor=%s"
        cursor.execute(sql,(nombre_empresa, direccion, telefono, correo_electronico, id_proveedor))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        print("Error al actualizar cliente:", str(e))
        return False