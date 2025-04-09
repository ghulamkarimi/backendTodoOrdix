from flask import Blueprint
from controllers.taskController import (
    get_all_tasks,
    create_task,
    update_task,
    delete_task
)

task_bp = Blueprint('task_bp', __name__)

# Alle Aufgaben holen
task_bp.route('/all', methods=['GET'])(get_all_tasks)

# Neue Aufgabe erstellen
task_bp.route('/', methods=['POST'])(create_task)

# Aufgabe aktualisieren
task_bp.route('/<int:task_id>', methods=['PUT'])(update_task)

# Aufgabe löschen
task_bp.route('/<int:task_id>', methods=['DELETE'])(delete_task)