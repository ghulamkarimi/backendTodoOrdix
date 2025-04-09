from flask import request, jsonify, session
from models.taskModel import Task, db
from models.listModel import List



def check_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Nicht eingeloggt'}), 401
    return None



# Alle Aufgaben des eingeloggten Benutzers (optional gefiltert nach Liste)
def get_all_tasks():
    user_id = session.get('user_id') or session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    list_id = request.args.get('list_id')  # z. B. /api/tasks?list_id=3

    query = Task.query.filter_by(user_id=user_id)
    if list_id:
        query = query.filter_by(list_id=list_id)

    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])


# Neue Aufgabe erstellen
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Nicht eingeloggt'}), 401

    data = request.get_json()

    # Überprüfen, ob list_id vorhanden ist
    list_id = data.get('list_id')
    if not list_id:
        return jsonify({'error': 'list_id fehlt'}), 400

    # Optional: prüfen, ob die Liste dem User gehört

    task_list = List.query.filter_by(id=list_id, user_id=user_id).first()
    if not task_list:
        return jsonify({'error': 'Liste nicht gefunden oder gehört nicht dir'}), 404

    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        is_completed=False,
        user_id=user_id,
        list_id=list_id  # ✅ Hier die neue Verbindung setzen
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
