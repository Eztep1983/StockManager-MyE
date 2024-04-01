import bcrypt

class User:
    def __init__(self, id, identification, password, fullname):
        self.identification = identification
        self.password = password
        self.fullname = fullname

class Register:
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()
            # Hash de la contraseña antes de almacenarla en la base de datos
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

            # verifica si la identificación está vacía y asigna un valor predeterminado si se necesita
            if not user.identification:
                user.identification = None  # O asigna un valor predeterminado apropiado

            # Insertar usuario en la base de datos
            sql = "INSERT INTO users (identification, password, fullname) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.identification, hashed_password, user.fullname))
            db.connection.commit()

            # Recuperar el ID del usuario recién registrado
            user_id = cursor.lastrowid

            # Construir y devolver el objeto de usuario registrado
            registered_user = User(user_id, user.identification, user.password, user.fullname)
            return registered_user
        except Exception as ex:
            # Manejar cualquier error durante el registro
            raise Exception("Error al intentar registrar usuario: {}".format(ex))
        finally:
            # Cerrar el cursor después de la ejecución de la consulta
            cursor.close()
