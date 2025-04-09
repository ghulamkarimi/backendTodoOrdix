from flask import request, jsonify, session
from models.userModel import User, db

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