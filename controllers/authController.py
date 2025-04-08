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

    return jsonify({'message': 'Login erfolgreich.', 'user': user.to_dict()}), 200

# Benutzer ausloggen
def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout erfolgreich.'}), 200
