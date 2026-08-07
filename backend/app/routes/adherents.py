import logging
import re
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request, current_app
from database import get_db
from services.session_manager import get_user_session
from services.sgdf_adherents import scrape_liste_adherents
import os
from werkzeug.utils import secure_filename

adherents_bp = Blueprint('adherents', __name__)

@adherents_bp.route('/api/adherents', methods=['GET'])
def get_adherents():
    """
    Récupère la liste des adhérents via scraping de l'intranet SGDF,
    et met en cache les résultats dans la table 'unit_members' de Supabase.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"error": "Non autorisé"}), 401
        
    try:
        # 1. Récupération des données via l'intranet
        adherents_info = scrape_liste_adherents(user_data["http"])
        raw_adherents = adherents_info.get("adherents", [])
        unit_name = adherents_info.get("unit_name")
        
        # --- MISE EN CACHE DANS SUPABASE ---
        if unit_name and len(raw_adherents) > 1:
            db = get_db()
            
            # A. Vérifier si l'unité existe, sinon la créer
            unit_res = db.table('units').select('id').eq('name', unit_name).execute()
            
            if not unit_res.data:
                unit_res = db.table('units').insert({'name': unit_name}).execute()
                
            if unit_res.data:
                unit_id = unit_res.data[0]['id']
                members_to_upsert = []
                
                # B. Formater les données (en ignorant la ligne d'en-tête [1:])
                for row in raw_adherents[1:]:
                    # Nettoyer les colonnes vides
                    cols = [str(c).strip() for c in row if str(c).strip() != '']
                    if len(cols) < 2:
                        continue
                        
                    row_text = " ".join(cols)
                    
                    # C. Détection du type d'adhérent (logique identique à ton frontend)
                    is_jeune = bool(re.search(r'\b1\d{2}\b', row_text))
                    is_chef = bool(re.search(r'\b2\d{2}\b', row_text))
                    
                    # D. Séparation basique Nom / Prénom (ex: "DUPONT Jean")
                    raw_name = cols[0]
                    name_parts = raw_name.split(" ", 1)
                    last_name = name_parts[0]
                    first_name = name_parts[1] if len(name_parts) > 1 else ""
                    
                    adherent_id = cols[1]
                    
                    # E. Préparation de la ligne
                    members_to_upsert.append({
                        "adherent_id": adherent_id,
                        "unit_id": unit_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "is_jeune": is_jeune,
                        "is_chef": is_chef,
                        "last_synced_at": datetime.now(timezone.utc).isoformat()
                    })
                
                # F. Insertion ou mise à jour en masse
                if members_to_upsert:
                    db.table('unit_members').upsert(members_to_upsert).execute()
        # -----------------------------------

        # On retourne les données intactes pour ne pas casser ton frontend existant
        return jsonify({
            "status": "success", 
            "data": raw_adherents, 
            "unit_name": unit_name,
            "adherent_id": user_data.get("adherent_id")
        }), 200
        
    except Exception as e:
        logging.error(f"Erreur scraping/mise en cache adhérents : {e}")
        return jsonify({"error": "Erreur lors de la récupération des adhérents"}), 500

@adherents_bp.route('/api/adherents/extras', methods=['GET'])
def get_adherent_extras():
    """
    Récupère les métadonnées locales (photos, progression) des adhérents 
    stockées dans la base de données Supabase.
    """
    try:
        db = get_db()
        res = db.table('adherent_extras').select('*').execute()
        extras = {row['adherent_id']: row for row in res.data}
        return jsonify({"status": "success", "data": extras}), 200
    except Exception as e:
        logging.error(f"Erreur récupération extras : {e}")
        return jsonify({"error": "Erreur base de données"}), 500

@adherents_bp.route('/api/adherents/<adherent_id>/upload', methods=['POST'])
def upload_adherent_fiche(adherent_id):
    """
    Gère l'upload d'un fichier (ex: fiche sanitaire) pour un adhérent spécifique.
    Sauvegarde le fichier localement et met à jour l'URL dans Supabase.
    """
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400
        
    try:
        filename = secure_filename(f"{adherent_id}_{file.filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        file_url = f"{request.host_url}uploads/{filename}"
        
        db = get_db()
        existing = db.table('adherent_extras').select('id').eq('adherent_id', adherent_id).execute()
        
        if existing.data:
            db.table('adherent_extras').update({"fiche_url": file_url}).eq('adherent_id', adherent_id).execute()
        else:
            db.table('adherent_extras').insert({
                "adherent_id": adherent_id,
                "fiche_url": file_url
            }).execute()
            
        return jsonify({"status": "success", "url": file_url}), 200

    except Exception as e:
        logging.error(f"Erreur lors de l'upload de la fiche pour {adherent_id} : {e}")
        return jsonify({"error": "Erreur serveur lors de la sauvegarde"}), 500

@adherents_bp.route('/api/adherents/<adherent_id>/progression', methods=['PUT', 'OPTIONS'])
def update_adherent_progression(adherent_id):
    """
    Met à jour ou crée la progression personnelle (symbole et action)
    d'un adhérent spécifique dans Supabase.
    """
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json or {}
        progression_symbole = data.get('progression_symbole', '')
        progression_action = data.get('progression_action', '')

        db = get_db()
        existing = db.table('adherent_extras').select('id').eq('adherent_id', adherent_id).execute()

        payload = {
            "progression_symbole": progression_symbole,
            "progression_action": progression_action
        }

        if existing.data:
            # Si l'adhérent a déjà une ligne (fiche ou photo), on met à jour les champs de progression
            db.table('adherent_extras').update(payload).eq('adherent_id', adherent_id).execute()
        else:
            # Sinon, on crée la première ligne pour cet adhérent
            payload["adherent_id"] = adherent_id
            db.table('adherent_extras').insert(payload).execute()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logging.error(f"Erreur de modification de la progression pour {adherent_id} : {e}")
        return jsonify({"error": "Erreur serveur lors de la sauvegarde"}), 500