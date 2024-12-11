import os
from dotenv import load_dotenv
import openai
# Carga las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Si SECRET_KEY está en .env, úsala; si no, genera una clave aleatoria.
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    openai.api_key = os.environ["OPENAI_API_KEY"] = "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"

class DevelopmentConfig(Config):
    DEBUG = os.getenv("FLASK_ENV") == "development"
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

config = {
    'development': DevelopmentConfig
}
