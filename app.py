from flask import Flask
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv
from config import Config
from database import db

# Import Blueprints
from routes.authRouter import auth_bp
from routes.taskRouter import task_bp
from routes.listRouter import list_bp

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
CORS(app, supports_credentials=True)
Session(app)
db.init_app(app)

# 🔄 Blueprints zuerst registrieren
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(list_bp, url_prefix='/api/lists')

# ✅ Dann create_all aufrufen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return {'message': 'ToDo-API läuft ✅'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
