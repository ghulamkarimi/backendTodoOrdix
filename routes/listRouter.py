from flask import Blueprint
from controllers.listController import (
    get_all_lists,
    create_list,
    delete_list
)

list_bp = Blueprint('list_bp', __name__)

# Alle Listen abrufen
list_bp.route('/', methods=['GET'])(get_all_lists)

# Neue Liste erstellen
list_bp.route('/', methods=['POST'])(create_list)

# Liste löschen
list_bp.route('/<int:list_id>', methods=['DELETE'])(delete_list)
