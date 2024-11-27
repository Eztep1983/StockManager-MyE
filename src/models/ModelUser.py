from models.entities.user import User

class ModelUser:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_trabajador, identification, password, fullname 
                     FROM users 
                     WHERE identification = %s"""
            cursor.execute(sql, (user.identification,))
            row = cursor.fetchone()

            if row:
                # Crea el usuario encontrado
                return User(row[0], row[1], row[2], row[3])  # Incluye la contraseña hasheada para validación
            return None  # Usuario no encontrado

        except Exception as ex:
            raise Exception(f"Error al intentar iniciar sesión: {str(ex)}")

        finally:
            if 'cursor' in locals():
                cursor.close()
                
    #Obtener usuario por medio de id
    @classmethod
    def get_by_id(cls, db, id_trabajador):
        """
        Obtiene un usuario por su ID.
        """
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_trabajador, identification, fullname FROM users WHERE id_trabajador = %s"
            cursor.execute(sql, (id_trabajador,))
            row = cursor.fetchone()

            if row:
                return User(row[0], row[1], None, row[2])
            return None  # Usuario no encontrado

        except Exception as ex:
            raise Exception(f"Error al obtener usuario por ID: {str(ex)}")

        finally:
            if 'cursor' in locals():
                cursor.close()


            
