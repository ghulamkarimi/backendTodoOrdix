from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
    }
    SESSION_TYPE = "sqlalchemy"  # Speichere Sessions in der Datenbank
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_SQLALCHEMY = None  # Wird in app.py gesetzt
    SESSION_SQLALCHEMY_TABLE = "sessions"  # Name der Tabelle für Sessions
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SAMESITE = "lax"
    SESSION_COOKIE_SECURE = False
    # SESSION_COOKIE_DOMAIN = "localhost"
    SECRET_KEY = os.getenv("SECRET_KEY") or "a-very-secret-key"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")        
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")         
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")   
