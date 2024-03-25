import bcrypt

# Genera una contraseña
password = "javier"

# Hashea la contraseña
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Imprime el hash
print("Contraseña hasheada:", hashed_password.decode('utf-8'))
