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
    # Add session configuration
    SESSION_TYPE = "filesystem"  # Use filesystem for simplicity
    SESSION_PERMANENT = False    # Sessions expire when the browser closes
    SESSION_USE_SIGNER = True    # Sign session cookies for security
    SECRET_KEY = os.getenv("SECRET_KEY") or "a-very-secret-key"  # Required for secure sessions