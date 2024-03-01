import os

class Config:
    SECRET_KEY = os.urandom(24)

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1004193541"
    MYSQL_DB = "flask_login"

config = {
    'development': DevelopmentConfig
}
