from werkzeug.security import check_password_hash
import bcrypt

class User:
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

