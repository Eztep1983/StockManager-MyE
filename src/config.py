import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))

class DevelopmentConfig(Config):
    DEBUG = os.getenv("FLASK_ENV") == "development"
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
