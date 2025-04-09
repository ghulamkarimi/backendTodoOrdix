from flask import Blueprint
from controllers.authController import register_user, login_user, logout_user, get_users,get_logged_in_user, request_password_reset, reset_password_by_code

# Erstelle ein Blueprint für alle Auth-Routen
auth_bp = Blueprint('auth_bp', __name__)

# POST /api/auth/register → Benutzer registrieren
auth_bp.route('/register', methods=['POST'])(register_user)

# GET /api/auth/users → Alle Benutzer abrufen
auth_bp.route('/users', methods=['GET'])(get_users)

# POST /api/auth/login → Benutzer einloggen
auth_bp.route('/login', methods=['POST'])(login_user)

auth_bp.route('/request-reset', methods=['POST'])(request_password_reset)
auth_bp.route('/reset-password', methods=['POST'])(reset_password_by_code)

# GET /api/auth/user → Eingeloggten Benutzer abrufen
auth_bp.route('/user', methods=['GET'])(get_logged_in_user)

# POST /api/auth/logout → Benutzer ausloggen
auth_bp.route('/logout', methods=['POST'])(logout_user)
