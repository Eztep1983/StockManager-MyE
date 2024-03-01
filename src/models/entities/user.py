from werkzeug.security import check_password_hash

class User():
    def __init__(self,id, identification, password, fullname=""):
        self.id = id
        self.identification = identification
        self.password = password
        self.fullname = fullname
        
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

