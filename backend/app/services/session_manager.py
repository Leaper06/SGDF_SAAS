import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import request
import logging

# Clé secrète pour signer les JWT (en dur pour le moment si pas dans .env)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-sgdf-key-for-dev")

# Stockage en mémoire pour garder le `requests.Session` (Intranet)
ACTIVE_SESSIONS = {}

def create_jwt_token(payload_data):
    """Génère un token JWT valide 30 jours."""
    payload = {
        **payload_data,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def get_user_session():
    """
    Vérifie le token JWT et retourne les infos.
    Si une session Intranet (http) est toujours active en mémoire, on l'ajoute.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
        
    token = auth_header.split(" ")[1]
    
    try:
        # 1. Décodage et validation du JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        # 2. Récupération de la session HTTP en mémoire si elle existe encore
        memory_session = ACTIVE_SESSIONS.get(token, {})
        
        # 3. On fusionne les deux (le payload du JWT est la source de vérité persistante)
        user_data = {
            "email": payload.get("email"),
            "unit_id": payload.get("unit_id"),
            "unit_name": payload.get("unit_name"),
            "adherent_id": payload.get("adherent_id"),
            "http": memory_session.get("http") # Peut être None si le serveur a redémarré
        }
        return user_data
        
    except jwt.ExpiredSignatureError:
        logging.warning("Token JWT expiré")
        return None
    except jwt.InvalidTokenError:
        logging.warning("Token JWT invalide")
        return None