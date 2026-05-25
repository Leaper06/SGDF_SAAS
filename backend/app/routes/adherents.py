import logging
from flask import Blueprint, jsonify
from database import get_db
from services.session_manager import get_user_session
from services.sgdf_adherents import scrape_liste_adherents
import os
from werkzeug.utils import secure_filename
from flask import request, current_app

adherents_bp = Blueprint('adherents', __name__)

@adherents_bp.route('/api/adherents', methods=['GET'])
def get_adherents():
    """
    Récupère la liste des adhérents via scraping de l'intranet SGDF 
    en utilisant la session HTTP active de l'utilisateur.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"error": "Non autorisé"}), 401
        
    try:
        adherents_info = scrape_liste_adherents(user_data["http"])
        return jsonify({
            "status": "success", 
            "data": adherents_info.get("adherents", []), 
            "unit_name": adherents_info.get("unit_name"),
            "adherent_id": user_data.get("adherent_id")
        }), 200
    except Exception as e:
        logging.error(f"Erreur scraping adhérents : {e}")
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
    # 1. Vérification de la présence du fichier dans la requête
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400
        
    try:
        # 2. Sauvegarde physique du fichier sur le serveur
        # On préfixe le nom du fichier par l'ID de l'adhérent pour éviter les doublons
        filename = secure_filename(f"{adherent_id}_{file.filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 3. Génération de l'URL publique
        file_url = f"http://localhost:5000/uploads/{filename}"
        
        # 4. Mise à jour de la base de données (Table adherent_extras)
        db = get_db()
        existing = db.table('adherent_extras').select('id').eq('adherent_id', adherent_id).execute()
        
        if existing.data:
            # L'adhérent a déjà des métadonnées, on met à jour la fiche
            db.table('adherent_extras').update({"fiche_url": file_url}).eq('adherent_id', adherent_id).execute()
        else:
            # Création de l'entrée pour cet adhérent
            db.table('adherent_extras').insert({
                "adherent_id": adherent_id,
                "fiche_url": file_url
            }).execute()
            
        return jsonify({"status": "success", "url": file_url}), 200

    except Exception as e:
        logging.error(f"Erreur lors de l'upload de la fiche pour {adherent_id} : {e}")
        return jsonify({"error": "Erreur serveur lors de la sauvegarde"}), 500