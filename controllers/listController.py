from flask import request, jsonify, session
from models.listModel import TaskList, db

# Alle Listen des eingeloggten Users abrufen
def get_all_lists():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    lists = TaskList.query.filter_by(user_id=user_id).all()
    return jsonify([liste.to_dict() for liste in lists])

# Neue Liste erstellen
def create_list():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    data = request.get_json()
    new_list = TaskList(
        name=data.get('name'),
        color=data.get('color'),
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

    liste = TaskList.query.filter_by(id=list_id, user_id=user_id).first()
    if not liste:
        return jsonify({'error': 'Liste nicht gefunden'}), 404

    db.session.delete(liste)
    db.session.commit()
    return jsonify({'message': 'Liste gelöscht'})
