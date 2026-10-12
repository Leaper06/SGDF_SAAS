import os
import threading
import time
import jwt
from datetime import datetime, timedelta, timezone
from flask import request
import logging
from dotenv import load_dotenv

load_dotenv()

# Clé secrète pour signer les JWT. Obligatoire : sans elle, n'importe qui pourrait
# fabriquer un token valide. Générer avec : python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("Variable d'environnement JWT_SECRET manquante (voir .env)")

# Stockage en mémoire des sessions intranet SGDF (`requests.Session`), par token.
# L'intranet les fait expirer au bout de quelques heures : au-delà, on les oublie
# pour que la mémoire du serveur ne grossisse pas indéfiniment.
ACTIVE_SESSIONS = {}
INTRANET_SESSION_LIFETIME_SECONDS = 6 * 3600
_sessions_lock = threading.Lock()


def remember_intranet_session(token, session_http):
    """Garde la session intranet d'un token et oublie les sessions trop anciennes."""
    if not token or session_http is None:
        return
    now = time.time()
    with _sessions_lock:
        expired = [t for t, entry in ACTIVE_SESSIONS.items()
                   if now - entry["created_at"] > INTRANET_SESSION_LIFETIME_SECONDS]
        for t in expired:
            del ACTIVE_SESSIONS[t]
        ACTIVE_SESSIONS[token] = {"http": session_http, "created_at": now}


def get_intranet_session(token):
    """Session intranet encore valide pour ce token, ou None."""
    entry = ACTIVE_SESSIONS.get(token)
    if not entry or time.time() - entry["created_at"] > INTRANET_SESSION_LIFETIME_SECONDS:
        return None
    return entry["http"]


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
        intranet_session = get_intranet_session(token)
        
        # 3. On fusionne les deux (le payload du JWT est la source de vérité persistante)
        user_data = {
            "email": payload.get("email"),
            "unit_id": payload.get("unit_id"),
            "unit_name": payload.get("unit_name"),
            "adherent_id": payload.get("adherent_id"),
            "http": intranet_session  # None si expirée ou si le serveur a redémarré
        }
        return user_data
        
    except jwt.ExpiredSignatureError:
        logging.warning("Token JWT expiré")
        return None
    except jwt.InvalidTokenError:
        logging.warning("Token JWT invalide")
        return None