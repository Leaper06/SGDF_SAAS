import logging
from flask import Blueprint, request, jsonify
from database import get_db
from services.session_manager import get_user_session

camps_bp = Blueprint('camps', __name__)

@camps_bp.route('/api/camps', methods=['GET'])
def get_all_camps():
    """
    Récupère la liste des camps de l'unité de l'utilisateur.
    Inclut également les camps d'autres unités où l'utilisateur est invité.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
        
    unit_name = user_data["unit_name"]
    adherent_id = user_data.get("adherent_id")
    db = get_db()
    
    try:
        response_unit = db.table('camps').select('*').eq('unit_name', unit_name).execute()
        camps_list = response_unit.data

        if adherent_id:
            response_guests = db.table('camp_guests').select('camp_id').eq('adherent_id', adherent_id).execute()
            guest_camp_ids = [item['camp_id'] for item in response_guests.data]

            if guest_camp_ids:
                response_invited = db.table('camps').select('*').in_('id', guest_camp_ids).execute()
                
                existing_ids = {c['id'] for c in camps_list}
                for c in response_invited.data:
                    if c['id'] not in existing_ids:
                        camps_list.append(c)

        camps_list.sort(key=lambda x: x['start_date'])

        return jsonify({"status": "success", "data": camps_list}), 200
    except Exception as e:
        logging.error(f"Erreur récupération camps : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500
    

@camps_bp.route('/api/camps', methods=['POST'])
def create_camp():
    """
    Crée un nouveau camp et l'associe automatiquement à l'unité du créateur.
    """
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
            "unit_name": unit_name
        }
        
        response = get_db().table('camps').insert(nouveau_camp).execute()
        return jsonify({"status": "success", "data": response.data}), 201
    except Exception as e:
        logging.error(f"Erreur création camp : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@camps_bp.route('/api/camps/<camp_id>', methods=['PUT'])
def update_camp(camp_id):
    """
    Met à jour les informations générales d'un camp existant.
    """
    try:
        data = request.json
        infos_maj = {
            "name": data.get("name"),
            "location": data.get("location"),
            "start_date": data.get("startDate"),
            "end_date": data.get("endDate")
        }
        
        response = get_db().table('camps').update(infos_maj).eq('id', camp_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        logging.error(f"Erreur modification camp : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@camps_bp.route('/api/camps/<camp_id>', methods=['DELETE'])
def delete_camp(camp_id):
    """
    Supprime un camp. 
    Nécessite la suppression préalable des activités associées pour respecter l'intégrité référentielle.
    """
    try:
        db = get_db()
        db.table('planning_slots').delete().eq('camp_id', camp_id).execute()
        response = db.table('camps').delete().eq('id', camp_id).execute()
        return jsonify({"status": "success", "data": response.data}), 200
    except Exception as e:
        logging.error(f"Erreur suppression camp : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@camps_bp.route('/api/camps/<camp_id>/guests', methods=['POST'])
def invite_guest(camp_id):
    """
    Ajoute un chef externe à la liste des invités d'un camp spécifique via son numéro d'adhérent.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401

    data = request.json
    adherent_id_invite = data.get('adherent_id')

    if not adherent_id_invite:
        return jsonify({"status": "error", "message": "Numéro d'adhérent requis"}), 400

    try:
        db = get_db()
        existing = db.table('camp_guests').select('*').eq('camp_id', camp_id).eq('adherent_id', adherent_id_invite).execute()
        
        if not existing.data:
            db.table('camp_guests').insert({
                'camp_id': camp_id,
                'adherent_id': adherent_id_invite
            }).execute()

        return jsonify({"status": "success", "message": "Chef invité avec succès"}), 200
    except Exception as e:
        logging.error(f"Erreur invitation chef : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500