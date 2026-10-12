import hashlib
import hmac
import logging
import os
from flask import Blueprint, request, jsonify, g
from database import get_db
from services.slot_responsibles import load_slot_responsibles, set_slot_responsible
from services.deletion import delete_planning_slots
from services.session_manager import JWT_SECRET
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
        filled_ids = slots_with_content(slots)
        for slot in slots:
            slot_id_str = str(slot['id'])
            if slot_id_str in resps:
                slot['responsible_name'] = resps[slot_id_str]
            else:
                slot['responsible_name'] = slot.get('responsible_name', '')
            # Fiche d'activité ou menu déjà rempli : l'interface prévient avant de supprimer le créneau
            slot['has_content'] = slot['id'] in filled_ids

        return jsonify({"status": "success", "data": slots}), 200

    except Exception as e:
        logging.error(f"Erreur de récupération du planning : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


def slots_with_content(slots):
    """
    Identifiants des créneaux dont la fiche d'activité (étapes, matériel, imaginaire)
    ou le menu (recettes) a déjà été rempli.
    """
    db = get_db()
    filled = set()

    activity_to_slot = {s['activity_id']: s['id'] for s in slots if s.get('activity_id')}
    if activity_to_slot:
        activity_ids = list(activity_to_slot)
        used = {row['activity_id'] for table in ('activity_steps', 'activity_materials')
                for row in db.table(table).select('activity_id').in_('activity_id', activity_ids).execute().data}
        used |= {a['id'] for a in db.table('activities').select('id, imaginary_and_objectives').in_('id', activity_ids).execute().data
                 if (a.get('imaginary_and_objectives') or '').strip()}
        filled |= {activity_to_slot[a] for a in used}

    slot_ids = [s['id'] for s in slots]
    if slot_ids:
        meals = db.table('meals').select('id, planning_slot_id').in_('planning_slot_id', slot_ids).execute().data
        meal_to_slot = {m['id']: m['planning_slot_id'] for m in meals}
        if meal_to_slot:
            with_recipes = db.table('meal_recipes').select('meal_id').in_('meal_id', list(meal_to_slot)).execute().data
            filled |= {meal_to_slot[r['meal_id']] for r in with_recipes}
    return filled


@planning_bp.route('/api/camps/<camp_id>/slots', methods=['PUT'])
@login_required
def save_camp_structure(camp_id):
    """
    Enregistre les changements de structure faits dans l'éditeur « à la chaîne » :
      - `slots` : créneaux modifiés (avec leur id) ou nouveaux (id provisoire « nouveau-... »)
      - `deleted_ids` : créneaux supprimés explicitement par ce chef
    Un créneau absent de la requête n'est jamais supprimé : plusieurs chefs peuvent modifier
    le planning en même temps sans effacer le travail des autres.
    Fonctionne aussi pour un modèle de l'unité (les modèles communs ne sont pas modifiables).
    Retourne la correspondance id provisoire → id définitif des créneaux créés.
    """
    if not can_access_camp(g.user, camp_id):
        return forbidden()
    try:
        db = get_db()
        data = request.json or {}
        incoming = data.get('slots', [])
        existing_ids = {s['id'] for s in db.table('planning_slots').select('id').eq('camp_id', camp_id).execute().data}

        to_update = [s for s in incoming if s.get('id') in existing_ids]
        to_create = [s for s in incoming if s.get('id') not in existing_ids]

        created = []
        if to_create:
            rows = db.table('planning_slots').insert([{
                "camp_id": camp_id,
                "title": s.get('title'),
                "slot_type": s.get('slot_type'),
                "start_time": s.get('start_time'),
                "end_time": s.get('end_time')
            } for s in to_create]).execute().data
            created = [{"client_id": s.get('id'), "id": row['id']} for s, row in zip(to_create, rows)]

        for s in to_update:
            db.table('planning_slots').update({
                "title": s.get('title'),
                "start_time": s.get('start_time'),
                "end_time": s.get('end_time')
            }).eq('id', s['id']).execute()

        # Seuls les créneaux de ce camp explicitement supprimés par ce chef sont retirés
        delete_planning_slots([slot_id for slot_id in data.get('deleted_ids', []) if slot_id in existing_ids])

        return jsonify({"status": "success", "created": created}), 200
    except Exception as e:
        logging.error(f"Erreur d'enregistrement du planning : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@planning_bp.route('/api/camps/<camp_id>/realtime', methods=['GET'])
@login_required
def get_realtime_config(camp_id):
    """
    Paramètres du temps réel (Supabase Realtime) pour ce camp, réservés aux chefs autorisés.
    Le canal porte un nom secret dérivé du camp : seuls ceux à qui l'API l'a donné peuvent l'écouter.
    Les messages ne contiennent aucune donnée (seulement « le planning a changé » et la présence).
    """
    if not can_access_camp(g.user, camp_id):
        return forbidden()
    publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
    if not publishable_key:
        return jsonify({"status": "success", "enabled": False}), 200
    channel_secret = hmac.new(JWT_SECRET.encode(), f"planning:{camp_id}".encode(), hashlib.sha256).hexdigest()[:32]
    return jsonify({
        "status": "success",
        "enabled": True,
        "url": os.getenv("SUPABASE_URL"),
        "key": publishable_key,
        "channel": f"planning-{channel_secret}"
    }), 200

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