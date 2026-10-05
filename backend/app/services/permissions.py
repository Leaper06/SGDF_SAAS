"""
Contrôle d'accès de l'API.

Règle générale : un utilisateur connecté n'accède qu'aux données de son unité
(camps, adhérents) ou de son groupe (tentes, lieux), ainsi qu'aux camps
auxquels il a été invité en tant que chef.
"""
import hashlib
import hmac
import os
import time
from functools import wraps
from typing import Optional

from flask import g, jsonify, request

from database import get_db
from services.session_manager import JWT_SECRET, get_user_session

# Durée de validité d'un lien de téléchargement de fichier (fiche sanitaire, photo)
SIGNED_URL_LIFETIME_SECONDS = 24 * 3600


# ==========================================
# DÉCORATEUR D'AUTHENTIFICATION
# ==========================================

def login_required(view):
    """
    Refuse la requête (401) si aucun token valide n'est fourni.
    L'utilisateur connecté est ensuite disponible dans `g.user`.
    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        # Les requêtes de pré-vérification CORS ne portent jamais de token
        if request.method == 'OPTIONS':
            return '', 200

        user = get_user_session()
        if not user:
            return jsonify({"status": "error", "message": "Non autorisé"}), 401

        g.user = user
        return view(*args, **kwargs)
    return wrapper


def forbidden():
    """Réponse standard quand la ressource n'appartient pas à l'utilisateur."""
    return jsonify({"status": "error", "message": "Accès refusé"}), 403


# ==========================================
# IDENTITÉ DE L'UTILISATEUR
# ==========================================

def get_group_name(user: dict) -> str:
    """
    Déduit le nom du groupe à partir du nom d'unité
    (ex: "MARINS ST MALO - NOTRE DAME D'ALETH" -> "NOTRE DAME D'ALETH").
    Même règle que le frontend (authStore.groupName).
    """
    unit_name = (user.get("unit_name") or "").strip()
    parts = unit_name.split(" - ")
    return parts[1].strip() if len(parts) > 1 else unit_name


def get_user_adherent_id(user: dict) -> Optional[str]:
    """
    Numéro d'adhérent du chef connecté.
    Le token ne le contient pas si le chef s'est identifié après sa connexion :
    on le retrouve alors dans chef_mappings.
    """
    if user.get("adherent_id"):
        return str(user["adherent_id"])

    res = get_db().table('chef_mappings').select('adherent_id').eq('email', user.get("email")).execute()
    if res.data and res.data[0].get('adherent_id'):
        return str(res.data[0]['adherent_id'])
    return None


# ==========================================
# CAMPS ET ÉLÉMENTS RATTACHÉS À UN CAMP
# ==========================================

def can_access_camp(user: dict, camp_id, allow_global_template: bool = False) -> bool:
    """
    Vrai si le camp appartient à l'unité de l'utilisateur ou s'il y est invité.
    Les modèles globaux (sans unité) sont lisibles par tous si `allow_global_template`.
    """
    if not camp_id:
        return False

    db = get_db()
    res = db.table('camps').select('id, unit_id, unit_name, is_template').eq('id', camp_id).execute()
    if not res.data:
        return False
    camp = res.data[0]

    if camp.get('unit_name') and camp['unit_name'] == user.get("unit_name"):
        return True
    if user.get("unit_id") and camp.get('unit_id') == user["unit_id"]:
        return True
    if allow_global_template and camp.get('is_template') and camp.get('unit_id') is None:
        return True

    adherent_id = get_user_adherent_id(user)
    if adherent_id:
        guest = db.table('camp_guests').select('id').eq('camp_id', camp_id).eq('adherent_id', adherent_id).execute()
        if guest.data:
            return True
    return False


def get_camp_id_of_slot(slot_id) -> Optional[str]:
    res = get_db().table('planning_slots').select('camp_id').eq('id', slot_id).execute()
    return res.data[0]['camp_id'] if res.data else None


def get_camp_id_of_activity(activity_id) -> Optional[str]:
    res = get_db().table('planning_slots').select('camp_id').eq('activity_id', activity_id).limit(1).execute()
    return res.data[0]['camp_id'] if res.data else None


def get_camp_id_of_meal(meal_id) -> Optional[str]:
    res = get_db().table('meals').select('planning_slot_id').eq('id', meal_id).execute()
    if not res.data:
        return None
    return get_camp_id_of_slot(res.data[0]['planning_slot_id'])


# ==========================================
# ADHÉRENTS, TENTES, LIENS
# ==========================================

def get_unit_adherent_ids(user: dict) -> set:
    """Numéros d'adhérent des membres de l'unité de l'utilisateur (et le sien)."""
    ids = set()
    if user.get("unit_id"):
        res = get_db().table('unit_members').select('adherent_id').eq('unit_id', user["unit_id"]).execute()
        ids = {str(m['adherent_id']) for m in res.data if m.get('adherent_id')}

    own_id = get_user_adherent_id(user)
    if own_id:
        ids.add(own_id)
    return ids


def can_access_adherent(user: dict, adherent_id) -> bool:
    return str(adherent_id) in get_unit_adherent_ids(user)


def can_access_tent(user: dict, tent_id) -> bool:
    res = get_db().table('tents').select('group_name').eq('id', tent_id).execute()
    return bool(res.data) and res.data[0].get('group_name') == get_group_name(user)


# ==========================================
# LIENS SIGNÉS POUR LES FICHIERS UPLOADÉS
# ==========================================
# Les fichiers sont ouverts directement par le navigateur (<img>, nouvel onglet),
# qui n'envoie pas le token. L'API distribue donc des liens signés et temporaires.

def _signature(filename: str, expires: int) -> str:
    message = f"{filename}:{expires}".encode()
    return hmac.new(JWT_SECRET.encode(), message, hashlib.sha256).hexdigest()


def sign_upload_url(stored_url: Optional[str]) -> Optional[str]:
    """Transforme l'URL stockée en base en lien signé valable 24 h."""
    if not stored_url:
        return None
    filename = os.path.basename(stored_url.split('?')[0])
    expires = int(time.time()) + SIGNED_URL_LIFETIME_SECONDS
    return f"/uploads/{filename}?expires={expires}&signature={_signature(filename, expires)}"


def is_valid_upload_signature(filename: str, expires: str, signature: str) -> bool:
    try:
        expires_ts = int(expires)
    except (TypeError, ValueError):
        return False
    if expires_ts < time.time():
        return False
    return hmac.compare_digest(_signature(filename, expires_ts), signature or "")
