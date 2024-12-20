from models.entities.user import User

class ModelUser:
    @classmethod
    def login(cls, db, user):
        """
        Inicia sesión de un usuario verificando su identificación y contraseña.

        Este método realiza una consulta a la base de datos para verificar las credenciales del usuario. Si se encuentra un 
        usuario con la identificación proporcionada, devuelve una instancia de la clase `User` con la información del usuario.

        Args:
            db: Instancia de la base de datos para realizar la consulta.
            user: Un objeto que contiene la información del usuario (identificación, etc.).

        Returns:
            User: Un objeto `User` con la información del usuario si las credenciales son correctas.
            None: Si no se encuentra un usuario con la identificación proporcionada.

        Raises:
            Exception: Si ocurre un error al realizar la consulta a la base de datos.
        """
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
        Obtiene un usuario de la base de datos a través de su ID.

        Este método consulta la base de datos utilizando el ID del trabajador para recuperar los datos del usuario. Si el 
        usuario existe, se devuelve una instancia de la clase `User` con la información disponible.

        Args:
            db: Instancia de la base de datos para realizar la consulta.
            id_trabajador: El ID del trabajador cuyo usuario se desea obtener.

        Returns:
            User: Un objeto `User` con la información del usuario si el ID es válido.
            None: Si no se encuentra un usuario con el ID proporcionado.

        Raises:
            Exception: Si ocurre un error al realizar la consulta a la base de datos.
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


            
