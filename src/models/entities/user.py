from werkzeug.security import check_password_hash
import bcrypt

class User:
    """
    Representa un usuario del sistema.

    Atributos:
        id (int): Identificador único del usuario.
        identification (str): Identificación del usuario.
        password (str): Contraseña hasheada del usuario.
        fullname (str): Nombre completo del usuario. Por defecto, una cadena vacía.
        active (bool): Estado del usuario. Indica si está activo. Por defecto, True.

    Métodos:
        check_password(hashed_password, password):
            Verifica si una contraseña en texto plano coincide con su versión hasheada.

        is_active():
            Determina si el usuario está activo.

        is_authenticated():
            Retorna True, indicando que el usuario está autenticado.

        get_id():
            Retorna el identificador único del usuario como cadena.

        can_delete_product():
            Verifica si el usuario puede eliminar productos. Todos los usuarios activos tienen este permiso.
    """
    def __init__(self, id, identification, password, fullname="", active=True):
        self.id = id
        self.identification = identification
        self.password = password  # Hash de la contraseña
        self.fullname = fullname
        self.active = active
        
    @classmethod
    def check_password(cls, hashed_password, password):
        # Validacion usando bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        return True  

    def get_id(self):
        return str(self.id)

    def can_delete_product(self):
        # En este caso porque no manejamos roles aun, todos los usuarios activos pueden eliminar productos
        return self.is_active()

