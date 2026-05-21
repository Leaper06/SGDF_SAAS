import os
import uuid
import logging
from flask import Flask, request, jsonify
from database import get_db
from flask_cors import CORS
from flask import request, jsonify 
import math
from werkzeug.utils import secure_filename
from flask import send_from_directory

# Import de tes services métiers
from services.sgdf_auth import get_sgdf_cookies, create_authenticated_session
from services.sgdf_adherents import get_logged_in_chef_info, scrape_liste_adherents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin (utile pour le frontend qui tourne sur un autre port)
# NOTRE BASE DE DONNÉES TEMPORAIRE (En mémoire)
# Elle va stocker les objets 'requests.Session' associés à un Token unique
ACTIVE_SESSIONS = {}
def get_user_session():
    """Vérifie le token et retourne les infos de session (http, unit_name)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return ACTIVE_SESSIONS.get(token)

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
    
    # 3. On récupère les infos du chef ET l'unité
    chef_info = get_logged_in_chef_info(session_http)
    adherents_info = scrape_liste_adherents(session_http)
    unit_name = adherents_info.get("unit_name", "Unité Inconnue")
    
    session_token = str(uuid.uuid4())
    
    # 4. On stocke tout dans la mémoire !
    ACTIVE_SESSIONS[session_token] = {
        "http": session_http,
        "unit_name": unit_name,
        "chef_adherent_id": chef_info.get("adherent_id"), # EX: 162821708
        "chef_email": chef_info.get("email") # EX: loic...gmail.com
    }
    
    logging.info(f"Connexion réussie. Token généré : {session_token}")
    
    return jsonify({
        "message": "Connexion réussie",
        "token": session_token
    }), 200

@app.route('/api/adherents', methods=['GET'])
def get_adherents():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token d'authentification manquant"}), 401
        
    token = auth_header.split(" ")[1]
    if token not in ACTIVE_SESSIONS:
        return jsonify({"error": "Token invalide ou session expirée."}), 401
        
    logging.info(f"Requête adhérents autorisée pour le token : {token}")
    user_session = ACTIVE_SESSIONS[token]["http"]
    
    # Récupération du gros dictionnaire {unit_name, adherents}
    adherents_result = scrape_liste_adherents(user_session)
    data = adherents_result.get("adherents", [])
    unit_name = adherents_result.get("unit_name", "Unité")
    
    if not data:
        return jsonify({"error": "Impossible de récupérer les données."}), 500
        
    return jsonify({
        "unit_name": unit_name,
        "count": max(0, len(data) - 1),
        "data": data
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
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
        
    unit_name = user_data["unit_name"]
    db = get_db()
    try:
        # MAGIE : On ne récupère QUE les camps de cette unité !
        response = db.table('camps').select('*').eq('unit_name', unit_name).order('start_date', desc=False).execute()
        
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/camps', methods=['POST'])
def create_camp():
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
        
    unit_name = user_data["unit_name"]
    try:
        data = request.json
        nouveau_camp = {
            "name": data.get("name"),
            "location": data.get("location"),
            "start_date": data.get("startDate"),
            "end_date": data.get("endDate"),
            "unit_name": unit_name # MAGIE : On tague le camp avec l'unité du créateur
        }
        
        response = get_db().table('camps').insert(nouveau_camp).execute()
        return jsonify({"status": "success", "data": response.data}), 201
    except Exception as e:
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
    
    # ==========================================
# --- ROUTES POUR L'INTENDANCE (RECETTES) ---
# ==========================================

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Récupère tout le catalogue de recettes depuis Supabase"""
    try:
        db = get_db()
        recipes_res = db.table('recipes').select('*').execute()
        
        return jsonify({"status": "success", "data": recipes_res.data}), 200

    except Exception as e:
        print("Erreur lors de la récupération des recettes :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/api/planning_slots/<slot_id>/meal', methods=['GET'])
def get_slot_meal(slot_id):
    """Récupère le repas associé à un créneau (ou le crée s'il n'existe pas)"""
    try:
        db = get_db()
        
        # 1. On cherche si un repas est déjà enregistré pour ce créneau de planning
        meal_res = db.table('meals').select('*').eq('planning_slot_id', slot_id).execute()
        
        if not meal_res.data:
            # Si aucun repas n'existe encore pour ce créneau, on le crée silencieusement !
            new_meal = db.table('meals').insert({
                "planning_slot_id": slot_id, 
                "additional_guests": 0
            }).execute()
            meal = new_meal.data[0]
        else:
            meal = meal_res.data[0]
            
        meal_id = meal['id']
        
        # 2. On récupère les recettes liées à ce repas grâce à la table de jointure meal_recipes
        # Supabase permet de faire la jointure directement dans le select
        jointure_res = db.table('meal_recipes').select('recipe_id, recipes(*)').eq('meal_id', meal_id).execute()
        
        # On extrait proprement la liste des recettes reçues
        recipes = []
        if jointure_res.data:
            for item in jointure_res.data:
                if item.get('recipes'):
                    recipes.append(item['recipes'])
        
        # On renvoie le tout structuré pour notre Front-end Vue.js
        return jsonify({
            "status": "success",
            "data": {
                "meal": meal,
                "recipes": recipes
            }
        }), 200

    except Exception as e:
        print("Erreur lors de la récupération du repas :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ROUTE : AJOUTER UN PLAT À UN REPAS ---
@app.route('/api/meals/<meal_id>/recipes', methods=['POST'])
def add_recipe_to_meal(meal_id):
    """Associe une recette à un repas dans la table de jointure"""
    try:
        db = get_db()
        data = request.json
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({"status": "error", "message": "ID de recette manquant"}), 400

        # On insère l'association dans la table meal_recipes
        db.table('meal_recipes').insert({
            "meal_id": meal_id,
            "recipe_id": recipe_id
        }).execute()

        return jsonify({"status": "success", "message": "Recette ajoutée au repas"}), 201

    except Exception as e:
        print("Erreur lors de l'ajout du plat :", e)
        return jsonify({"status": "error", "message": str(e)}), 500


# --- ROUTE : RETIRER UN PLAT D'UN REPAS ---
@app.route('/api/meals/<meal_id>/recipes/<recipe_id>', methods=['DELETE'])
def remove_recipe_from_meal(meal_id, recipe_id):
    """Supprime l'association entre une recette et un repas"""
    try:
        db = get_db()
        
        # On supprime la ligne correspondante dans meal_recipes
        db.table('meal_recipes').delete().eq('meal_id', meal_id).eq('recipe_id', recipe_id).execute()

        return jsonify({"status": "success", "message": "Recette retirée du repas"}), 200

    except Exception as e:
        print("Erreur lors de la suppression du plat :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# --- ROUTE : CRÉER UNE NOUVELLE RECETTE ---
@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    """Crée une nouvelle recette et ses ingrédients dans la base de données"""
    try:
        db = get_db()
        data = request.json

        # 1. On prépare les données de la recette principale
        recipe_data = {
            "name": data.get('name'),
            "dish_type": data.get('type'),  # Le front envoie 'type', la DB attend 'dish_type'
            "instructions": "", 
            "is_vegetarian": data.get('is_vegetarian', False),
            "is_eco": data.get('is_eco', False),
            # On met is_pork_free par défaut pour correspondre à ta structure de base
            "is_pork_free": True 
        }
        
        # On insère la recette et on récupère son ID généré
        recipe_res = db.table('recipes').insert(recipe_data).execute()
        new_recipe_id = recipe_res.data[0]['id']

        # 2. On boucle sur chaque ingrédient envoyé par le formulaire
        ingredients_list = data.get('ingredients', [])
        for ing in ingredients_list:
            ing_name = ing.get('name', '').strip()
            
            if not ing_name:
                continue # On ignore les lignes vides
            
            # On cherche si cet ingrédient existe déjà dans le grand catalogue
            ing_res = db.table('ingredients').select('*').eq('name', ing_name).execute()
            
            if not ing_res.data:
                # S'il n'existe pas, on le crée
                new_ing = db.table('ingredients').insert({
                    "name": ing_name,
                    "category": "Autre", # Catégorie par défaut
                    "unit_type": "g"     # Unité par défaut
                }).execute()
                ingredient_id = new_ing.data[0]['id']
            else:
                # S'il existe, on récupère juste son ID
                ingredient_id = ing_res.data[0]['id']
            
            # 3. On lie l'ingrédient à la recette avec les grammages
            db.table('recipe_ingredients').insert({
                "recipe_id": new_recipe_id,
                "ingredient_id": ingredient_id,
                "qty_child": float(ing.get('qty_child') or 0),
                "qty_adult": float(ing.get('qty_adult') or 0)
            }).execute()

        return jsonify({"status": "success", "message": "Recette créée avec succès !"}), 201

    except Exception as e:
        print("Erreur lors de la création de la recette :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# --- ROUTE : GÉNÉRER LE BORDEREAU DE COURSES D'UN REPAS ---
@app.route('/api/meals/<meal_id>/shopping-list', methods=['GET'])
def get_shopping_list(meal_id):
    """Calcule la liste de courses totale pour un repas donné"""
    try:
        db = get_db()
        
        # On récupère le nombre de convives depuis l'URL (par défaut 17 comme sur ta maquette)
        adults = int(request.args.get('adults', 17))
        children = int(request.args.get('children', 0))

        # 1. On cherche toutes les recettes associées à ce repas
        mr_res = db.table('meal_recipes').select('recipe_id').eq('meal_id', meal_id).execute()
        
        if not mr_res.data:
            return jsonify({"status": "success", "data": []}), 200

        # On extrait juste la liste des IDs des recettes (ex: [1, 4, 8])
        recipe_ids = [item['recipe_id'] for item in mr_res.data]

        # 2. On récupère tous les ingrédients de ces recettes (avec les infos de l'ingrédient)
        ing_res = db.table('recipe_ingredients').select(
            'qty_adult, qty_child, ingredients(name, unit_type, category)'
        ).in_('recipe_id', recipe_ids).execute()

        # 3. On fait les mathématiques, on fusionne les doublons et on arrondit !
        shopping_dict = {}

        for item in ing_res.data:
            ing_info = item['ingredients']
            if not ing_info:
                continue
                
            ing_name = ing_info['name']
            unit = ing_info['unit_type']
            category = ing_info['category']

            # Calcul de la quantité brute
            qty_raw = (item.get('qty_adult', 0) * adults) + (item.get('qty_child', 0) * children)
            
            # --- LA MAGIE DE L'ARRONDI AU SUPÉRIEUR ---
            qty = math.ceil(qty_raw)

            if ing_name in shopping_dict:
                # Si l'ingrédient est déjà présent (doublon), on cumule et on ré-arrondit au cas où
                shopping_dict[ing_name]['qty'] = math.ceil(shopping_dict[ing_name]['qty_raw_accumulated'] + qty_raw)
                shopping_dict[ing_name]['qty_raw_accumulated'] += qty_raw
            else:
                shopping_dict[ing_name] = {
                    'name': ing_name,
                    'qty': qty,
                    'qty_raw_accumulated': qty_raw, # On garde une trace brute pour les cumuls précis
                    'unit': unit,
                    'category': category
                }

        # On nettoie notre dictionnaire temporaire pour Vue.js
        result = []
        for key, item in shopping_dict.items():
            result.append({
                'name': item['name'],
                'qty': item['qty'],
                'unit': item['unit'],
                'category': item['category']
            })

        # Optionnel : on trie par ordre alphabétique
        result.sort(key=lambda x: x['name'])

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        print("Erreur lors du calcul des courses :", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# ==========================================
# GESTION DES FICHIERS (UPLOADS)
# ==========================================
# Dossier où seront sauvegardés les fichiers sur le serveur
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/adherents/<adherent_id>/upload', methods=['POST'])
def upload_adherent_file(adherent_id):
    """Reçoit un fichier, le sauvegarde sur le serveur et met à jour Supabase"""
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "Aucun fichier envoyé"}), 400
            
        file = request.files['file']
        doc_type = request.form.get('type') # 'photo' ou 'fiche'
        
        if file.filename == '':
            return jsonify({"status": "error", "message": "Fichier vide"}), 400

        # 1. On nettoie le nom du fichier et on le sauvegarde sur le serveur
        extension = file.filename.split('.')[-1]
        filename = secure_filename(f"{adherent_id}_{doc_type}.{extension}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 2. On génère l'URL pour y accéder plus tard
        file_url = f"http://localhost:5000/uploads/{filename}"
        
        # 3. On met à jour Supabase
        db = get_db()
        # On regarde si cet adhérent a déjà une ligne dans adherent_extras
        res = db.table('adherent_extras').select('*').eq('adherent_id', adherent_id).execute()
        
        if res.data:
            # Update
            db.table('adherent_extras').update({f"{doc_type}_url": file_url}).eq('adherent_id', adherent_id).execute()
        else:
            # Insert
            db.table('adherent_extras').insert({
                'adherent_id': adherent_id, 
                f"{doc_type}_url": file_url
            }).execute()

        return jsonify({"status": "success", "url": file_url}), 200

    except Exception as e:
        print("Erreur upload :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    """Route magique pour permettre au frontend d'afficher/télécharger l'image ou le PDF"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/adherents/extras', methods=['GET'])
def get_all_extras():
    """Récupère toutes les photos et fiches pour les fusionner avec Intranext dans le Front"""
    try:
        res = get_db().table('adherent_extras').select('*').execute()
        # On transforme la liste en dictionnaire pour que Vue.js le lise plus vite
        extras_dict = {item['adherent_id']: item for item in res.data}
        return jsonify({"status": "success", "data": extras_dict}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/api/adherents/<adherent_id>/progression', methods=['PUT'])
def update_progression(adherent_id):
    """Met à jour ou crée la progression personnelle d'un adhérent"""
    try:
        data = request.json
        symbole = data.get('progression_symbole', '')
        action = data.get('progression_action', '')

        db = get_db()
        
        # On vérifie si l'adhérent a déjà une ligne dans adherent_extras
        res = db.table('adherent_extras').select('*').eq('adherent_id', adherent_id).execute()

        if res.data:
            # S'il existe, on met à jour
            db.table('adherent_extras').update({
                'progression_symbole': symbole,
                'progression_action': action
            }).eq('adherent_id', adherent_id).execute()
        else:
            # S'il n'existe pas encore (pas de photo ni de fiche), on crée la ligne
            db.table('adherent_extras').insert({
                'adherent_id': adherent_id,
                'progression_symbole': symbole,
                'progression_action': action
            }).execute()

        return jsonify({"status": "success", "message": "Progression sauvegardée"}), 200

    except Exception as e:
        print("Erreur de sauvegarde de progression :", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # On lance le serveur Flask sur le port 5000
    logging.info("Démarrage du serveur Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)