import os

class Config:
    SECRET_KEY = os.urandom(24)

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "87067480"
    MYSQL_DB = "seteco"

config = {
    'development': DevelopmentConfig
}
