import bcrypt
import logging
from models.entities.user import User

class ModelUser:
    @classmethod
    def login(cls, db, user):
        """
        Verifica las credenciales del usuario y devuelve el objeto User si son válidas.
        """
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_trabajador, identification, password, fullname, role 
                     FROM users 
                     WHERE identification = %s"""
            cursor.execute(sql, (user.identification,))
            row = cursor.fetchone()

            if row:
                # Crea una instancia de User con los datos obtenidos
                found_user = User(row[0], row[1], row[2], row[3], role=row[4])
                
                # Verifica la contraseña
                if bcrypt.checkpw(user.password.encode('utf-8'), found_user.password.encode('utf-8')):
                    return found_user
                else:
                    logging.warning("Contraseña incorrecta para el usuario %s", user.identification)
                    return None  # Contraseña incorrecta
            logging.info("Usuario no encontrado: %s", user.identification)
            return None  # Usuario no encontrado

        except Exception as ex:
            logging.error(f"Error during login query: {ex}, User: {user.identification}")
            raise Exception("Error al intentar iniciar sesión")


        finally:
            if 'cursor' in locals():
                cursor.close()

    @classmethod
    def get_by_id(cls, db, id_trabajador):
        """
        Obtiene un usuario por su ID.
        """
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_trabajador, identification, fullname, role, active
                    FROM users 
                    WHERE id_trabajador = %s"""

            cursor.execute(sql, (id_trabajador,))
            row = cursor.fetchone()

            if row:
                # Retorna un objeto User
                return User(row[0], row[1], None, row[2], active=row[4], role=row[3])
            logging.info("Usuario no encontrado con ID: %s", id_trabajador)
            return None  # Usuario no encontrado

        except Exception as ex:
            logging.error("Error al obtener usuario por ID: %s", str(ex))
            raise Exception("Error al obtener usuario por ID")

        finally:
            if 'cursor' in locals():
                cursor.close()

    @classmethod
    def create_user(cls, db, user):
        """
        Crea un nuevo usuario en la base de datos.
        """
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = db.connection.cursor()
            sql = """INSERT INTO users (identification, password, fullname, role, active)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (user.identification, hashed_password, user.fullname, user.role or 'user', user.active))
            db.connection.commit()
            logging.info("Usuario creado con éxito: %s", user.identification)
            return True

        except Exception as ex:
            logging.error("Error al intentar crear usuario: %s", str(ex))
            raise Exception("Error al intentar crear usuario")

        finally:
            if 'cursor' in locals():
                cursor.close()

    @classmethod
    def update_user(cls, db, user):
        """
        Actualiza la información de un usuario en la base de datos.
        """
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE users 
                     SET identification = %s, fullname = %s, role = %s, active = %s
                     WHERE id_trabajador = %s"""
            cursor.execute(sql, (user.identification, user.fullname, user.role, user.active, user.id))
            db.connection.commit()
            logging.info("Usuario actualizado con éxito: %s", user.id)
            return True

        except Exception as ex:
            logging.error("Error al intentar actualizar usuario: %s", str(ex))
            raise Exception("Error al intentar actualizar usuario")

        finally:
            if 'cursor' in locals():
                cursor.close()
