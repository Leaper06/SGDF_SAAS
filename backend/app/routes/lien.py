from flask import Blueprint, request, jsonify
from database import get_db 
import logging

liens_bp = Blueprint('liens', __name__)

@liens_bp.route('/api/chef/<adherent_id>/links', methods=['GET'])
def get_links(adherent_id):
    """
    Récupère les liens favoris d'un chef spécifique via son adherent_id
    """
    try:
        db = get_db()
        
        # Filtre Supabase : on cherche uniquement les liens de ce chef
        res = db.table('favorite_links').select('*').eq('adherent_id', adherent_id).execute()
        
        return jsonify({"status": "success", "links": res.data}), 200
        
    except Exception as e:
        logging.error(f"Erreur de récupération des liens pour le chef {adherent_id} : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur"}), 500


@liens_bp.route('/api/chef/<adherent_id>/links', methods=['POST', 'OPTIONS'])
def add_link(adherent_id):
    """
    Ajoute un nouveau lien favori pour un chef spécifique
    """
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json or {}
    
    try:
        db = get_db()
        
        new_link = {
            'adherent_id': adherent_id,
            'name': data.get('nom'),
            'url': data.get('url')
        }
        
        res = db.table('favorite_links').insert(new_link).execute()
        
        # On renvoie le lien fraîchement créé (qui contient son nouvel UUID généré par Supabase)
        link_data = res.data[0] if res.data else {}
        
        return jsonify({"status": "success", "link": link_data}), 201
        
    except Exception as e:
        logging.error(f"Erreur d'ajout de lien pour le chef {adherent_id} : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur"}), 500


@liens_bp.route('/api/links/<link_id>', methods=['DELETE', 'OPTIONS'])
def delete_link(link_id):
    """
    Supprime un lien favori spécifique grâce à son UUID
    """
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        db = get_db()
        
        db.table('favorite_links').delete().eq('id', link_id).execute()
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logging.error(f"Erreur de suppression du lien {link_id} : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur"}), 500