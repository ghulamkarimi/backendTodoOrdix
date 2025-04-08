from flask import Blueprint
from controllers.authController import register_user, login_user, logout_user

# Erstelle ein Blueprint für alle Auth-Routen
auth_bp = Blueprint('auth_bp', __name__)

# POST /api/auth/register → Benutzer registrieren
auth_bp.route('/register', methods=['POST'])(register_user)

# POST /api/auth/login → Benutzer einloggen
auth_bp.route('/login', methods=['POST'])(login_user)

# POST /api/auth/logout → Benutzer ausloggen
auth_bp.route('/logout', methods=['POST'])(logout_user)
