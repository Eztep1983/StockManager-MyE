from flask import abort
from flask_login import current_user
def role_required(role_name):
    """
    Decorador para restringir el acceso basado en roles.
    """
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                abort(403)  # Prohibido
            return f(*args, **kwargs)
        return decorated_function
    return decorator