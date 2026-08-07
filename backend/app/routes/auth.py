import uuid
from flask import Blueprint, request, jsonify
from database import get_db
from services.sgdf_auth import get_sgdf_cookies, create_authenticated_session
from services.sgdf_adherents import scrape_liste_adherents
from services.session_manager import ACTIVE_SESSIONS, get_user_session

# On crée le "mini-routeur" pour l'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cookies = get_sgdf_cookies(username, password)
    if not cookies:
        return jsonify({"error": "Échec de l'authentification."}), 401

    session_http = create_authenticated_session(cookies)
    adherents_info = scrape_liste_adherents(session_http)
    unit_name = adherents_info.get("unit_name", "Unité Inconnue")
    
    db = get_db()
    mapping_res = db.table('chef_mappings').select('*').eq('email', username).execute()
    
    session_token = str(uuid.uuid4())
    chef_adherent_id = None
    needs_identification = True 
    unit_id = None

    if mapping_res.data:
        chef_adherent_id = mapping_res.data[0]['adherent_id']
        needs_identification = False
        unit_id = mapping_res.data[0].get('unit_id')

    # Recherche de l'unit_id dans la table units si non présent dans chef_mappings
    if not unit_id and unit_name:
        unit_res = db.table('units').select('id').eq('name', unit_name).execute()
        if unit_res.data:
            unit_id = unit_res.data[0]['id']

    ACTIVE_SESSIONS[session_token] = {
        "http": session_http,
        "unit_name": unit_name,
        "unit_id": unit_id,
        "email": username,
        "adherent_id": chef_adherent_id
    }
    
    return jsonify({
        "message": "Connexion réussie",
        "token": session_token,
        "needs_identification": needs_identification,
        "email": username,
        "unit_name": unit_name,
        "unit_id": unit_id
    }), 200


@auth_bp.route('/api/chef/identify', methods=['POST'])
def identify_chef():
    user_data = get_user_session()
    if not user_data:
        return jsonify({"error": "Non autorisé"}), 401
        
    data = request.json
    adherent_id = data.get('adherent_id')
    email = user_data['email']
    unit_name = user_data['unit_name']

    try:
        get_db().table('chef_mappings').insert({
            'email': email,
            'adherent_id': adherent_id,
            'unit_name': unit_name
        }).execute()
        
        user_data['adherent_id'] = adherent_id
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500