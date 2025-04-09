 
from datetime import datetime, timedelta
from flask import request, jsonify, session, url_for
from flask_mail import Message
from extention.extention import mail
from models.userModel import User, db
import random




# Registrierung eines neuen Benutzers
def register_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Eingaben validieren
    if not email or not username or not password:
        return jsonify({'error': 'Alle Felder (E-Mail, Benutzername, Passwort) sind erforderlich.'}), 400

    # Prüfen ob Benutzer schon existiert
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'E-Mail ist bereits registriert.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Benutzername ist bereits vergeben.'}), 400

    # Neuen Benutzer erstellen und speichern
    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Benutzer erfolgreich registriert.'}), 201

# Benutzerinformationen abrufen
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Benutzer einloggen
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Falsche E-Mail oder Passwort.'}), 401

    # Session speichern
    session['user_id'] = user.id
    print(f"Session-ID: {session.sid}, User-ID: {session['user_id']}")
    return jsonify({'message': 'Login erfolgreich.', 'user': user.to_dict()}), 200


# Passwort zurücksetzen
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'E-Mail ist erforderlich'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Kein Benutzer mit dieser E-Mail gefunden'}), 404

    code = generate_reset_code()
    user.reset_code = code
    user.reset_code_expiration = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

  
    subject = "Passwort zurücksetzen"
    body = f"Hier ist dein Bestätigungscode zum Zurücksetzen deines Passworts: {code}\n\nDieser Code ist 10 Minuten gültig."

    try:
        msg = Message(subject=subject, recipients=[email], body=body)
        mail.send(msg)
        return jsonify({'message': 'Code per E-Mail gesendet '})
    except Exception as e:
        return jsonify({'error': f'E-Mail-Fehler: {str(e)}'}), 500
    
    
# zahl generieren für Passwort zurücksetzen    
def generate_reset_code():
    return str(random.randint(100000, 999999))    
    
# Passwort zurücksetzen (Token validieren und neues Passwort setzen)    
    
def reset_password_by_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('new_password')

    if not email or not code or not new_password:
        return jsonify({'error': 'Alle Felder sind erforderlich'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or user.reset_code != code:
        return jsonify({'error': 'Ungültiger Code'}), 400

    if user.reset_code_expiration < datetime.utcnow():
        return jsonify({'error': 'Code ist abgelaufen'}), 400

    user.set_password(new_password)
    user.reset_code = None
    user.reset_code_expiration = None
    db.session.commit()

    return jsonify({'message': 'Passwort erfolgreich zurückgesetzt ✅'}), 200


# Benutzer ausloggen
def logout_user():
    print(f"Session vor Logout: {session}")  # Debug-Ausgabe
    session.pop('user_id', None)
    print(f"Session nach Logout: {session}")  # Debug-Ausgabe
    return jsonify({'message': 'Logout erfolgreich.'}), 200

# Eingeloggten Benutzer abrufen
def get_logged_in_user():
    print(f"Session in get_logged_in_user: {session}")  # Debug-Ausgabe
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt.'}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Benutzer nicht gefunden.'}), 404
    return jsonify({'user': user.to_dict()}), 200