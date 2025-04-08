from flask import request, jsonify, session
from models.taskModel import Task, db

# Alle Aufgaben des eingeloggten Benutzers holen
def get_all_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks])

# Neue Aufgabe erstellen
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    data = request.get_json()
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        is_completed=False,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Aufgabe erstellt', 'task': task.to_dict()}), 201

# Aufgabe aktualisieren
def update_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Aufgabe nicht gefunden'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.is_completed = data.get('is_completed', task.is_completed)

    db.session.commit()
    return jsonify({'message': 'Aufgabe aktualisiert', 'task': task.to_dict()})

# Aufgabe löschen
def delete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Aufgabe nicht gefunden'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Aufgabe gelöscht'})
