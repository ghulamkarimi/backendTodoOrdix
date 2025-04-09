from flask import Flask, session
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv
from config import Config
from database import db
import time
import pymysql
import os
from sqlalchemy.sql import text

# Import Blueprints
from routes.authRouter import auth_bp
from routes.taskRouter import task_bp
from routes.listRouter import list_bp

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
db.init_app(app)
app.config['SESSION_SQLALCHEMY'] = db  # Setze die SQLAlchemy-Instanz für Flask-Session
Session(app)

# Warte auf die Datenbank
def wait_for_db():
    max_attempts = 10
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    database = os.getenv("DB_NAME")

    for attempt in range(max_attempts):
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            conn.close()
            print("Datenbankverbindung erfolgreich")
            break
        except Exception as e:
            print(f"Verbindung zur Datenbank fehlgeschlagen (Versuch {attempt + 1}/{max_attempts}): {e}")
            if attempt == max_attempts - 1:
                raise Exception("Konnte keine Verbindung zur Datenbank herstellen")
            time.sleep(2)

# 🔄 Blueprints zuerst registrieren
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(list_bp, url_prefix='/api/lists')

# ✅ Warte auf die Datenbank und erstelle dann die Tabellen
with app.app_context():
    wait_for_db()
    db.create_all()

@app.route('/')
def index():
    return {'message': 'ToDo-API läuft ✅'}

@app.route('/test-session')
def test_session():
    print("🧪 Session User ID:", session.get("user_id"))
    return {'session_user_id': session.get("user_id")}



@app.route('/test-db')
def test_db():
    try:
        result = db.session.execute(text("SELECT 1")).fetchone()
        return {'message': 'Datenbankverbindung erfolgreich', 'result': str(result)}
    except Exception as e:
        return {'error': str(e), 'type': str(type(e))}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)