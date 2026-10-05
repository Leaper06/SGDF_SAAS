import logging
from flask import Blueprint, jsonify, request, current_app, g
from database import get_db
from services.session_manager import get_user_session, create_jwt_token, ACTIVE_SESSIONS
from services.unit_members import save_unit_and_members
from services.sgdf_adherents import scrape_liste_adherents
from services.permissions import (
    login_required, forbidden, can_access_adherent, get_unit_adherent_ids, sign_upload_url,
)
import os
from werkzeug.utils import secure_filename

adherents_bp = Blueprint('adherents', __name__)

# Formats acceptés pour les fiches sanitaires (un fichier .html servi par notre domaine
# permettrait d'exécuter du code dans le navigateur des autres chefs)
ALLOWED_UPLOAD_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.webp', '.heic'}

# Code renvoyé quand la session INTRANET SGDF a expiré (le frontend redemande le mot de passe).
# Différent de 401, réservé à la session de l'application (qui déconnecte l'utilisateur).
INTRANET_LOGIN_REQUIRED = 428

@adherents_bp.route('/api/adherents', methods=['GET'])
def get_adherents():
    """
    Récupère la liste des adhérents depuis le cache Supabase (rapide, pas de scraping).
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"error": "Non autorisé"}), 401
        
    unit_id = user_data.get("unit_id")
    unit_name = user_data.get("unit_name", "Unité Inconnue")

    if not unit_id:
        return jsonify({"status": "success", "data": [], "unit_name": unit_name}), 200

    try:
        db = get_db()
        # On récupère les membres de l'unité
        members_res = db.table('unit_members').select('*').eq('unit_id', unit_id).execute()
        
        # On les formate pour le frontend actuel
        # Le frontend attend un tableau de tableaux (historiquement issu du scraping HTML)
        # Format attendu par le front: [ ["En-tête ignoré"], ["NOM Prénom", "id", "Code... 122", ...] ]
        
        raw_adherents = [["En-tête", "Code", "Statut"]]
        for m in members_res.data:
            # On reconstitue la ligne de texte pour que les regex du frontend (isJeune = 1xx, isChef = 2xx) fonctionnent.
            code_fictif = "122" if m.get("is_jeune") else "222" if m.get("is_chef") else "000"
            nom_complet = f"{m.get('last_name', '')} {m.get('first_name', '')}".strip()
            
            row = [
                nom_complet,
                m.get("adherent_id"),
                code_fictif
            ]
            raw_adherents.append(row)
            
        return jsonify({
            "status": "success", 
            "data": raw_adherents, 
            "unit_name": unit_name,
            "adherent_id": user_data.get("adherent_id")
        }), 200

    except Exception as e:
        logging.error(f"Erreur lecture adhérents Supabase : {e}")
        return jsonify({"error": "Erreur base de données"}), 500


@adherents_bp.route('/api/adherents/sync', methods=['POST'])
def sync_adherents():
    """
    Déclenche le web scraping de l'intranet SGDF en utilisant la session active 
    pour mettre à jour la table Supabase unit_members.
    Accepte optionnellement un 'password' si la session en mémoire a expiré.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"error": "Non autorisé"}), 401
        
    data = request.get_json(silent=True) or {}
    password = data.get('password')
    session_http = user_data.get("http")
    
    # Si le serveur a redémarré (session_http = None) ou si l'utilisateur envoie un password
    if (not session_http or password) and password:
        from services.sgdf_auth import get_sgdf_cookies, create_authenticated_session, ServerBusyError

        try:
            cookies = get_sgdf_cookies(user_data["email"], password)
        except ServerBusyError:
            return jsonify({"error": "Beaucoup de connexions en cours, réessayez dans une minute."}), 503
        if not cookies:
            return jsonify({"error": "Identifiants incorrects"}), INTRANET_LOGIN_REQUIRED
            
        session_http = create_authenticated_session(cookies)
        
        # On met à jour le dictionnaire en mémoire
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            if token not in ACTIVE_SESSIONS:
                ACTIVE_SESSIONS[token] = {}
            ACTIVE_SESSIONS[token]["http"] = session_http
            
    if not session_http:
        return jsonify({"error": "Session expirée, veuillez fournir votre mot de passe"}), INTRANET_LOGIN_REQUIRED
        
    try:
        adherents_info = scrape_liste_adherents(session_http)
        raw_adherents = adherents_info.get("adherents", [])
        unit_name = adherents_info.get("unit_name")
        
        if not unit_name or len(raw_adherents) <= 1:
            return jsonify({"error": "Aucun adhérent trouvé ou session expirée"}), INTRANET_LOGIN_REQUIRED
            
        unit_id = save_unit_and_members(unit_name, raw_adherents)
        response = {"status": "success", "message": "Synchronisation réussie"}

        # Si le token ne connaissait pas encore l'unité (première synchro d'une nouvelle unité),
        # on renvoie un nouveau token qui la contient, sinon les écrans resteraient vides
        if unit_id and not user_data.get("unit_id"):
            response["token"] = create_jwt_token({
                "email": user_data.get("email"),
                "unit_name": unit_name,
                "unit_id": unit_id,
                "adherent_id": user_data.get("adherent_id"),
            })
            response["unit_id"] = unit_id
            # La session intranet gardée en mémoire suit le nouveau token
            old_token = request.headers.get('Authorization', '').replace('Bearer ', '')
            ACTIVE_SESSIONS[response["token"]] = ACTIVE_SESSIONS.get(old_token, {"http": session_http})

        return jsonify(response), 200
        
    except Exception as e:
        logging.error(f"Erreur scraping/mise en cache adhérents : {e}")
        return jsonify({"error": "Erreur lors de la synchronisation (Session peut-être expirée)"}), INTRANET_LOGIN_REQUIRED

@adherents_bp.route('/api/adherents/extras', methods=['GET'])
@login_required
def get_adherent_extras():
    """
    Récupère les métadonnées locales (photos, progression) des adhérents de l'unité
    stockées dans la base de données Supabase.
    Les fichiers sont renvoyés sous forme de liens signés valables 24 h.
    """
    try:
        adherent_ids = list(get_unit_adherent_ids(g.user))
        if not adherent_ids:
            return jsonify({"status": "success", "data": {}}), 200

        db = get_db()
        res = db.table('adherent_extras').select('*').in_('adherent_id', adherent_ids).execute()
        extras = {}
        for row in res.data:
            row['fiche_url'] = sign_upload_url(row.get('fiche_url'))
            row['photo_url'] = sign_upload_url(row.get('photo_url'))
            extras[row['adherent_id']] = row
        return jsonify({"status": "success", "data": extras}), 200
    except Exception as e:
        logging.error(f"Erreur récupération extras : {e}")
        return jsonify({"error": "Erreur base de données"}), 500

@adherents_bp.route('/api/adherents/<adherent_id>/upload', methods=['POST'])
@login_required
def upload_adherent_fiche(adherent_id):
    """
    Gère l'upload d'un fichier (ex: fiche sanitaire) pour un adhérent spécifique.
    Sauvegarde le fichier localement et met à jour l'URL dans Supabase.
    """
    if not can_access_adherent(g.user, adherent_id):
        return forbidden()

    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400
        
    if os.path.splitext(file.filename)[1].lower() not in ALLOWED_UPLOAD_EXTENSIONS:
        return jsonify({"error": "Format non accepté (PDF ou image uniquement)"}), 400

    try:
        filename = secure_filename(f"{adherent_id}_{file.filename}")
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # On stocke un chemin relatif : le lien signé est généré à chaque lecture
        file_url = f"/uploads/{filename}"
        
        db = get_db()
        existing = db.table('adherent_extras').select('id').eq('adherent_id', adherent_id).execute()
        
        if existing.data:
            db.table('adherent_extras').update({"fiche_url": file_url}).eq('adherent_id', adherent_id).execute()
        else:
            db.table('adherent_extras').insert({
                "adherent_id": adherent_id,
                "fiche_url": file_url
            }).execute()
            
        return jsonify({"status": "success", "url": sign_upload_url(file_url)}), 200

    except Exception as e:
        logging.error(f"Erreur lors de l'upload de la fiche pour {adherent_id} : {e}")
        return jsonify({"error": "Erreur serveur lors de la sauvegarde"}), 500

@adherents_bp.route('/api/adherents/<adherent_id>/progression', methods=['PUT', 'OPTIONS'])
@login_required
def update_adherent_progression(adherent_id):
    """
    Met à jour ou crée la progression personnelle (symbole et action)
    d'un adhérent spécifique dans Supabase.
    """
    if not can_access_adherent(g.user, adherent_id):
        return forbidden()

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