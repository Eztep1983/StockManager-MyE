import bcrypt

def hashear_contraseña(contraseña):
    # Generar un salt aleatorio
    salt = bcrypt.gensalt()
    # Hashear la contraseña utilizando el salt generado
    contraseña_hasheada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_hasheada

# Ejemplo de uso para el hashs
"""contraseña_texto_plano = "esteban"
contraseña_hasheada = hashear_contraseña(contraseña_texto_plano)
print("Contraseña hasheada:", contraseña_hasheada.decode('utf-8'))"""