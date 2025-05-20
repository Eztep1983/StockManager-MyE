import bcrypt
from models.entities.user import User

#Clase para registrar a los usuarios 
class Register:
    """
    Registra un nuevo usuario en la base de datos.

    Args:
        db: La conexión activa a la base de datos.
        user (User): Un objeto `User` que contiene los datos del usuario a registrar.

    Returns:
        User: Un objeto `User` que representa al usuario registrado.

    Raises:
        ValueError: Si la identificación ya está registrada.
        Exception: Si ocurre un error durante el proceso de registro.

    Notes:
        - La contraseña proporcionada por el usuario se hashea antes de almacenarse en la base de datos.
        - Se realiza una verificación previa para evitar registros duplicados basados en la identificación.
    """
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()

            # Verificar si la identificación ya existe
            sql_check = "SELECT id_trabajador FROM users WHERE identification = %s"
            cursor.execute(sql_check, (user.identification,))
            if cursor.fetchone():
                raise ValueError("La identificación ya está registrada.")

            # Hashear la contraseña
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insertar todos los campos relevantes
            sql_insert = """
                INSERT INTO users (identification, password, fullname, role, active)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (
                user.identification,
                hashed_password,
                user.fullname,
                user.role,
                user.active
            ))

            db.connection.commit()

            user_id = cursor.lastrowid
            return User(user_id, user.identification, None, user.fullname, user.role, user.active)

        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"Error al intentar registrar usuario: {str(ex)}")

        finally:
            if 'cursor' in locals():
                cursor.close()
