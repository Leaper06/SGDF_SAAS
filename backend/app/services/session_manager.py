from flask import request

# NOTRE BASE DE DONNÉES TEMPORAIRE (En mémoire)
ACTIVE_SESSIONS = {}

def get_user_session():
    """Vérifie le token et retourne les infos de session (http, unit_name)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return ACTIVE_SESSIONS.get(token)