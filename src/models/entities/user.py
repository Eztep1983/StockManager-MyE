import bcrypt
from flask import logging
class User:
    """
    Representa un usuario del sistema.

    Atributos:
        id (int): Identificador único del usuario.
        identification (str): Identificación del usuario.
        password (str): Contraseña hasheada del usuario.
        fullname (str): Nombre completo del usuario. Por defecto, una cadena vacía.
        active (bool): Estado del usuario. Indica si está activo. Por defecto, True.
        role (str): Rol del usuario. Por defecto, 'user'.
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
        has_role(role_name):
            Verifica si el usuario tiene un rol específico.
        is_admin():
            Verifica si el usuario tiene el rol de administrador
        """
    def __init__(self, id, identification, password, fullname="", active=True, role="user"):
        self.id = id
        self.identification = identification
        self.password = password  # Hash de la contraseña
        self.fullname = fullname
        self.active = active
        self.role = role
        
    @classmethod
    def check_password(cls, hashed_password, password):
        # Validacion usando bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def is_admin(self):
        ROLES = {
        'ADMIN': 'admin',
        'USER': 'user',
        }
        return self.role == ROLES['ADMIN']

    def is_admin(self):
        return self.role == 'admin' 

    def has_role(self, role_name):
        return self.role == role_name

    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        return self.active   

    def get_id(self):
        return str(self.id)

    def can_delete_product(self):
        return self.is_admin() or self.is_active()
