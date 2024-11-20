import bcrypt
from models.entities.user import User

class Register:
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()

            # Verificar si la identificación ya existe
            sql_check = "SELECT id_trabajador FROM users WHERE identification = %s"
            cursor.execute(sql_check, (user.identification,))
            if cursor.fetchone():
                raise ValueError("La identificación ya está registrada.")

            # Hash de la contraseña antes de almacenarla
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insertar usuario
            sql_insert = "INSERT INTO users (identification, password, fullname) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (user.identification, hashed_password, user.fullname))
            db.connection.commit()

            # Retornar usuario registrado
            user_id = cursor.lastrowid
            return User(user_id, user.identification, None, user.fullname)

        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"Error al intentar registrar usuario: {str(ex)}")

        finally:
            if 'cursor' in locals():
                cursor.close()

