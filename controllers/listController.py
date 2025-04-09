from flask import request, jsonify, session
from models.listModel import List, db

# Alle Listen des eingeloggten Users abrufen
def get_all_lists():
    user_id = session.get('user_id') or session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    lists = List.query.filter_by(user_id=user_id).all()
    return jsonify([liste.to_dict() for liste in lists])

# Neue Liste erstellen
def create_list():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    data = request.get_json()
    name = data.get('name')
    color = data.get('color')

    if not name:
        return jsonify({'error': 'Listenname fehlt'}), 400

    # Prüfen, ob eine Liste mit dem gleichen Namen schon existiert (für diesen User)
    existing_list = List.query.filter_by(name=name, user_id=user_id).first()
    if existing_list:
        return jsonify({'error': 'Liste mit diesem Namen existiert bereits'}), 400

    new_list = List(
        name=name,
        color=color,
        user_id=user_id
    )

    db.session.add(new_list)
    db.session.commit()
    return jsonify({'message': 'Liste erstellt', 'list': new_list.to_dict()}), 201


# Liste löschen
def delete_list(list_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    liste = List.query.filter_by(id=list_id, user_id=user_id).first()
    if not liste:
        return jsonify({'error': 'Liste nicht gefunden'}), 404

    db.session.delete(liste)
    db.session.commit()
    return jsonify({'message': 'Liste gelöscht'})
