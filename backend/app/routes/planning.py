import logging
from flask import Blueprint, request, jsonify, g
from database import get_db
from services.slot_responsibles import load_slot_responsibles, set_slot_responsible
from services.deletion import delete_planning_slots
from services.replace_rows import replace_rows
from services.permissions import (
    login_required, forbidden, can_access_camp,
    get_camp_id_of_slot, get_camp_id_of_activity,
)

planning_bp = Blueprint('planning', __name__)

@planning_bp.route('/api/planning_slots', methods=['POST'])
@login_required
def create_planning_slot():
    """
    Crée un nouveau créneau dans le planning d'un camp.
    """
    try:
        data = request.json
        if not can_access_camp(g.user, data.get("camp_id")):
            return forbidden()
        responsible_name = data.get("responsible_name")
        nouveau_creneau = {
            "camp_id": data.get("camp_id"),
            "title": data.get("title"),
            "slot_type": data.get("slot_type"),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }
        
        response = get_db().table('planning_slots').insert(nouveau_creneau).execute()
        if response.data and responsible_name:
            slot_id = response.data[0]['id']
            set_slot_responsible(slot_id, responsible_name)

        return jsonify({"status": "success", "data": response.data}), 201

    except Exception as e:
        logging.error(f"Erreur lors de l'insertion du créneau : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/camps/<camp_id>/slots', methods=['GET'])
@login_required
def get_camp_slots(camp_id):
    """
    Récupère l'intégralité des créneaux d'un camp, triés chronologiquement.
    """
    # Les modèles globaux sont consultables par tous (aperçu avant création d'un camp)
    if not can_access_camp(g.user, camp_id, allow_global_template=True):
        return forbidden()
    try:
        db = get_db()
        response = db.table('planning_slots') \
            .select('*') \
            .eq('camp_id', camp_id) \
            .order('start_time', desc=False) \
            .execute()
            
        slots = response.data
        resps = load_slot_responsibles()
        for slot in slots:
            slot_id_str = str(slot['id'])
            if slot_id_str in resps:
                slot['responsible_name'] = resps[slot_id_str]
            else:
                slot['responsible_name'] = slot.get('responsible_name', '')

        return jsonify({"status": "success", "data": slots}), 200

    except Exception as e:
        logging.error(f"Erreur de récupération du planning : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/planning_slots/<slot_id>', methods=['DELETE'])
@login_required
def delete_planning_slot(slot_id):
    """
    Supprime un créneau spécifique du planning.
    """
    if not can_access_camp(g.user, get_camp_id_of_slot(slot_id)):
        return forbidden()
    try:
        # Supprime aussi le repas, la fiche d'activité et le responsable du créneau
        delete_planning_slots([slot_id])
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du créneau : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/planning_slots/<slot_id>', methods=['PUT'])
@login_required
def update_planning_slot(slot_id):
    """
    Met à jour les informations d'un créneau existant.
    """
    if not can_access_camp(g.user, get_camp_id_of_slot(slot_id)):
        return forbidden()
    try:
        data = request.json
        infos_maj = {
            "title": data.get("title"),
            "slot_type": data.get("slot_type"),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }
        
        response = get_db().table('planning_slots').update(infos_maj).eq('id', slot_id).execute()
        
        if "responsible_name" in data:
            set_slot_responsible(slot_id, data.get("responsible_name"))

        return jsonify({"status": "success", "data": response.data}), 200

    except Exception as e:
        logging.error(f"Erreur lors de la modification de l'activité : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/planning_slots/<slot_id>/activity', methods=['GET'])
@login_required
def get_activity(slot_id):
    """
    Charge la fiche détaillée d'une activité. 
    Si aucune activité n'est associée au créneau, une entité vide est générée et liée automatiquement.
    """
    if not can_access_camp(g.user, get_camp_id_of_slot(slot_id)):
        return forbidden()
    try:
        db = get_db()
        slot_res = db.table('planning_slots').select('*').eq('id', slot_id).execute()
        if not slot_res.data:
            return jsonify({"status": "error", "message": "Créneau introuvable"}), 404
        
        slot = slot_res.data[0]
        activity_id = slot.get('activity_id')

        # Création à la volée de l'activité si elle n'existe pas encore pour ce créneau
        if not activity_id:
            new_act = db.table('activities').insert({"title": slot.get('title')}).execute()
            activity_id = new_act.data[0]['id']
            db.table('planning_slots').update({"activity_id": activity_id}).eq('id', slot_id).execute()
            
        activity_res = db.table('activities').select('*').eq('id', activity_id).execute()
        steps_res = db.table('activity_steps').select('*').eq('activity_id', activity_id).order('order_index').execute()
        materials_res = db.table('activity_materials').select('*').eq('activity_id', activity_id).execute()

        data = {
            "activity": activity_res.data[0],
            "steps": steps_res.data,
            "materials": materials_res.data
        }
        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        logging.error(f"Erreur de chargement de la fiche : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/activities/<activity_id>', methods=['PUT'])
@login_required
def save_activity(activity_id):
    """
    Sauvegarde l'intégralité d'une fiche d'activité (imaginaire, matériel et étapes de déroulé).
    Opère par remplacement destructif sur les collections liées (matériel et étapes).
    """
    if not can_access_camp(g.user, get_camp_id_of_activity(activity_id)):
        return forbidden()
    try:
        db = get_db()
        data = request.json
        
        db.table('activities').update({
            "imaginary_and_objectives": data.get('imaginary_and_objectives')
        }).eq('id', activity_id).execute()

        materials = [
            {"activity_id": activity_id, "item_name": m['item_name'], "is_checked": m.get('is_checked', False)}
            for m in data.get('materials', [])
        ]
        replace_rows('activity_materials', 'activity_id', activity_id, materials)

        steps = [
            {
                "activity_id": activity_id,
                "title": s['title'],
                "description": s.get('description', ''),
                "duration_minutes": s.get('duration_minutes', 15),
                "order_index": i
            }
            for i, s in enumerate(data.get('steps', []))
        ]
        replace_rows('activity_steps', 'activity_id', activity_id, steps)

        return jsonify({"status": "success", "message": "Activité sauvegardée"}), 200

    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/activities/<activity_id>/responsibles', methods=['GET', 'POST'])
@login_required
def manage_activity_responsibles(activity_id):
    """
    Gère l'assignation des chefs responsables pour une activité donnée.
    """
    if not can_access_camp(g.user, get_camp_id_of_activity(activity_id)):
        return forbidden()
    db = get_db()
    
    if request.method == 'GET':
        try:
            res = db.table('activity_responsibles').select('adherent_id').eq('activity_id', activity_id).execute()
            ids = [row['adherent_id'] for row in res.data if row.get('adherent_id')]
            return jsonify({"status": "success", "data": ids}), 200
        except Exception as e:
            logging.error(f"Erreur GET responsibles : {e}")
            return jsonify({"status": "error", "message": "Erreur serveur"}), 500
        
    if request.method == 'POST':
        try:
            data = request.json
            adherent_ids = data.get('adherent_ids', [])
            
            inserts = [{"activity_id": activity_id, "adherent_id": str(aid)} for aid in adherent_ids]
            replace_rows('activity_responsibles', 'activity_id', activity_id, inserts, key='adherent_id')
                
            return jsonify({"status": "success", "message": "Responsables mis à jour"}), 200
        except Exception as e:
            logging.error(f"Erreur POST responsibles : {e}")
            return jsonify({"status": "error", "message": "Erreur serveur"}), 500