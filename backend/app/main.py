import os
import uuid
import logging
from flask import Flask, request, jsonify
from database import get_db
from flask_cors import CORS
from flask import request, jsonify 

# Import de tes services métiers
from services.sgdf_auth import get_sgdf_cookies, create_authenticated_session
from services.sgdf_adherents import scrape_liste_adherents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin (utile pour le frontend qui tourne sur un autre port)
# NOTRE BASE DE DONNÉES TEMPORAIRE (En mémoire)
# Elle va stocker les objets 'requests.Session' associés à un Token unique
ACTIVE_SESSIONS = {}

@app.route('/api/status', methods=['GET'])
def health_check():
    """Route de test pour vérifier que l'API tourne bien."""
    return jsonify({"status": "ok", "message": "API PolyMaîtrise opérationnelle"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    """Route pour s'authentifier et récupérer un token de session."""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Identifiants manquants (username, password attendus)"}), 400

    username = data['username']
    password = data['password']

    logging.info(f"Tentative de connexion pour l'utilisateur : {username}")
    
    # 1. On lance Playwright pour récupérer les cookies
    cookies = get_sgdf_cookies(username, password)
    
    if not cookies:
        return jsonify({"error": "Échec de l'authentification. Vérifiez les identifiants."}), 401

    # 2. On crée la session HTTP rapide
    session_http = create_authenticated_session(cookies)
    
    # 3. On génère un Token unique pour cet utilisateur
    session_token = str(uuid.uuid4())
    
    # 4. On stocke la session en mémoire
    ACTIVE_SESSIONS[session_token] = session_http
    
    logging.info(f"Connexion réussie. Token généré : {session_token}")
    
    return jsonify({
        "message": "Connexion réussie",
        "token": session_token
    }), 200

@app.route('/api/adherents', methods=['GET'])
def get_adherents():
    """Route pour récupérer la liste des adhérents (nécessite un token valide)."""
    # On cherche le token dans les en-têtes de la requête (Headers)
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token d'authentification manquant ou mal formaté"}), 401
        
    # On extrait le token brut (on enlève "Bearer ")
    token = auth_header.split(" ")[1]
    
    # On vérifie si ce token existe dans notre mémoire
    if token not in ACTIVE_SESSIONS:
        return jsonify({"error": "Token invalide ou session expirée. Veuillez vous reconnecter."}), 401
        
    logging.info(f"Requête adhérents autorisée pour le token : {token}")
    
    # On récupère la session HTTP de cet utilisateur spécifique
    user_session = ACTIVE_SESSIONS[token]
    
    # On lance le scraping !
    adherents_data = scrape_liste_adherents(user_session)
    
    if not adherents_data:
        return jsonify({"error": "Impossible de récupérer les données ou liste vide."}), 500
        
    # On renvoie les données structurées en JSON
    return jsonify({
        "count": len(adherents_data) - 1, # -1 pour ne pas compter la ligne des titres
        "data": adherents_data
    }), 200

@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Route de test pour vérifier la connexion à Supabase."""
    db = get_db()
    try:
        # On tente de récupérer juste une ligne de la table 'units' pour voir si ça répond
        response = db.table('units').select('*').limit(1).execute()
        return jsonify({
            "status": "success", 
            "message": "Connexion à la base de données réussie.",
            "data": response.data
        }), 200
    except Exception as e:
        logging.error(f"Erreur de connexion DB: {e}")
        return jsonify({
            "status": "error", 
            "message": "Impossible de se connecter à la base de données."
        }), 500

@app.route('/api/camps', methods=['GET'])
def get_all_camps():
    """
    Route pour récupérer la liste de tous les camps/week-ends planifiés.
    Trié par ordre chronologique (du plus proche au plus lointain).
    """
    db = get_db()
    try:
        logging.info("Requête de récupération de la liste des camps...")
        
        # CORRECTION ICI : on utilise desc=False pour l'ordre croissant (un ordre ascendant)
        response = db.table('camps').select('*').order('start_date', desc=False).execute()
        
        return jsonify({
            "status": "success",
            "count": len(response.data),
            "data": response.data
        }), 200

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des camps : {e}")
        return jsonify({
            "status": "error",
            "message": "Impossible de charger le calendrier."
        }), 500
   

@app.route('/api/camps', methods=['POST'])
def create_camp():
    try:
        # 1. On récupère le JSON envoyé par Vue.js
        data = request.json
        
        # 2. On formate pour que ça corresponde aux colonnes de ta table Supabase
        # (J'utilise start_date car c'est ce qu'on lit dans le frontend)
        nouveau_camp = {
            "name": data.get("name"),
            "location": data.get("location"),
            "start_date": data.get("startDate"),
            "end_date": data.get("endDate") # Décommente si tu as créé cette colonne dans Supabase
            # "type": data.get("type")         # Idem, si tu veux stocker si c'est un WE ou une journée
        }
        
        # 3. On insère dans la base
        response = get_db().table('camps').insert(nouveau_camp).execute()
        
        # 4. On renvoie un signal de succès au frontend
        return jsonify({"status": "success", "data": response.data}), 201

    except Exception as e:
        print("Erreur lors de l'insertion :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/planning_slots', methods=['POST'])
def create_planning_slot():
    try:
        # 1. On récupère le JSON du frontend
        data = request.json
        
        # 2. On formate pour la table Supabase 'planning_slots'
        nouveau_creneau = {
            "camp_id": data.get("camp_id"),
            "title": data.get("title"),
            "slot_type": data.get("slot_type"),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }
        
        # 3. On insère dans la base
        response = get_db().table('planning_slots').insert(nouveau_creneau).execute()
        
        # 4. On renvoie le succès
        return jsonify({"status": "success", "data": response.data}), 201

    except Exception as e:
        print("Erreur lors de l'insertion du créneau :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/camps/<camp_id>/slots', methods=['GET'])
def get_camp_slots(camp_id):
    try:
        # On récupère les créneaux du camp_id spécifié, triés par heure de début
        response = get_db().table('planning_slots') \
            .select('*') \
            .eq('camp_id', camp_id) \
            .order('start_time', desc=False) \
            .execute()
            
        return jsonify({"status": "success", "data": response.data}), 200

    except Exception as e:
        print("Erreur de récupération du planning :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# --- ROUTE : SUPPRIMER UNE ACTIVITÉ ---
@app.route('/api/planning_slots/<slot_id>', methods=['DELETE'])
def delete_planning_slot(slot_id):
    try:
        response = get_db().table('planning_slots').delete().eq('id', slot_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        print("Erreur lors de la suppression du créneau :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ROUTE : SUPPRIMER UN WEEK-END COMPLET ---
@app.route('/api/camps/<camp_id>', methods=['DELETE'])
def delete_camp(camp_id):
    try:
        # 1. On nettoie d'abord toutes les activités liées à ce camp (sécurité relationnelle)
        get_db().table('planning_slots').delete().eq('camp_id', camp_id).execute()
        
        # 2. Maintenant on peut supprimer le camp sereinement
        response = get_db().table('camps').delete().eq('id', camp_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        print("Erreur lors de la suppression du camp :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# --- ROUTE : MODIFIER LES INFOS D'UN WEEK-END ---
@app.route('/api/camps/<camp_id>', methods=['PUT'])
def update_camp(camp_id):
    try:
        data = request.json
        
        # On prépare les données à mettre à jour dans Supabase
        infos_maj = {
            "name": data.get("name"),
            "location": data.get("location"),
            "start_date": data.get("startDate"),
            "end_date": data.get("endDate")
        }
        
        response = get_db().table('camps').update(infos_maj).eq('id', camp_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200

    except Exception as e:
        print("Erreur lors de la modification du camp :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# --- ROUTE : MODIFIER UNE ACTIVITÉ DU PLANNING ---
@app.route('/api/planning_slots/<slot_id>', methods=['PUT'])
def update_planning_slot(slot_id):
    try:
        data = request.json
        
        infos_maj = {
            "title": data.get("title"),
            "slot_type": data.get("slot_type"),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }
        
        response = get_db().table('planning_slots').update(infos_maj).eq('id', slot_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200

    except Exception as e:
        print("Erreur lors de la modification de l'activité :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# --- ROUTE : CHARGER (OU CRÉER) LA FICHE D'ACTIVITÉ ---
@app.route('/api/planning_slots/<slot_id>/activity', methods=['GET'])
def get_activity(slot_id):
    try:
        db = get_db()
        
        # 1. On cherche le créneau correspondant
        slot_res = db.table('planning_slots').select('*').eq('id', slot_id).execute()
        if not slot_res.data:
            return jsonify({"status": "error", "message": "Créneau introuvable"}), 404
        
        slot = slot_res.data[0]
        activity_id = slot.get('activity_id')

        # 2. Si aucune activité n'est liée à ce créneau, on la crée à la volée !
        if not activity_id:
            new_act = db.table('activities').insert({"title": slot.get('title')}).execute()
            activity_id = new_act.data[0]['id']
            # On met à jour le créneau pour lui attacher cette nouvelle activité
            db.table('planning_slots').update({"activity_id": activity_id}).eq('id', slot_id).execute()
            
        # 3. On récupère toutes les données associées (Activité + Étapes + Matériel)
        activity_res = db.table('activities').select('*').eq('id', activity_id).execute()
        steps_res = db.table('activity_steps').select('*').eq('activity_id', activity_id).order('order_index').execute()
        materials_res = db.table('activity_materials').select('*').eq('activity_id', activity_id).execute()

        # On rassemble tout dans un seul gros objet pour Vue.js
        data = {
            "activity": activity_res.data[0],
            "steps": steps_res.data,
            "materials": materials_res.data
        }
        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        print("Erreur de chargement de la fiche :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ROUTE : SAUVEGARDER TOUTE LA FICHE ---
@app.route('/api/activities/<activity_id>', methods=['PUT'])
def save_activity(activity_id):
    try:
        db = get_db()
        data = request.json
        
        # 1. On sauvegarde l'imaginaire
        db.table('activities').update({
            "imaginary_and_objectives": data.get('imaginary_and_objectives')
        }).eq('id', activity_id).execute()

        # 2. On met à jour le matériel (on supprime l'ancien, on insère le nouveau)
        db.table('activity_materials').delete().eq('activity_id', activity_id).execute()
        materials = data.get('materials', [])
        if materials:
            mats_to_insert = [{"activity_id": activity_id, "item_name": m['item_name'], "is_checked": m.get('is_checked', False)} for m in materials]
            db.table('activity_materials').insert(mats_to_insert).execute()

        # 3. On met à jour le déroulé (avec l'ordre précis)
        db.table('activity_steps').delete().eq('activity_id', activity_id).execute()
        steps = data.get('steps', [])
        if steps:
            steps_to_insert = []
            for i, s in enumerate(steps): # enumerate permet d'avoir l'index (i) pour la colonne order_index
                steps_to_insert.append({
                    "activity_id": activity_id,
                    "title": s['title'],
                    "description": s.get('description', ''),
                    "duration_minutes": s.get('duration_minutes', 15),
                    "order_index": i 
                })
            db.table('activity_steps').insert(steps_to_insert).execute()

        return jsonify({"status": "success", "message": "Activité sauvegardée"}), 200

    except Exception as e:
        print("Erreur lors de la sauvegarde :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
if __name__ == '__main__':
    # On lance le serveur Flask sur le port 5000
    logging.info("Démarrage du serveur Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)