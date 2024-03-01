from models.entities.user import User
import bcrypt

class ModelUser:
    
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, identification, password, fullname 
                     FROM users 
                     WHERE identification = %s"""
            cursor.execute(sql, (user.identification,))
            row = cursor.fetchone()
            if row:
                stored_password = row[2]
                if bcrypt.checkpw(user.password.encode('utf-8'), stored_password.encode('utf-8')):
                    user = User(row[0], row[1], row[3])  # Assuming User doesn't store the password
                    return user
                else:
                    return None  # Password doesn't match
            else:
                return None  # User not found
        except Exception as ex:
            raise Exception("Error al intentar iniciar sesión: {}".format(ex))
        finally:
            cursor.close()
