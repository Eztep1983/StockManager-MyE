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
                    return None  # Si la contraseña no coincide
            else:
                return None  # Si el usuario no se encuentra
        except Exception as ex:
            raise Exception("Error al intentar iniciar sesión: {}".format(ex))
        finally:
            cursor.close()
            
            
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, identification, fullname FROM users WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception("Error fetching user by ID: {}".format(ex))
        finally:
            cursor.close()


            
