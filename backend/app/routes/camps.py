import logging
import threading
from flask import Blueprint, request, jsonify
from database import get_db
from services.session_manager import get_user_session


camps_bp = Blueprint('camps', __name__)



@camps_bp.route('/api/camps', methods=['GET'])
def get_all_camps():
    """
    Récupère la liste des camps de l'unité de l'utilisateur (hors templates).
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
        
    unit_name = user_data["unit_name"]
    adherent_id = user_data.get("adherent_id")
    db = get_db()
    
    try:
        response_unit = db.table('camps').select('*').eq('unit_name', unit_name).or_('is_template.eq.false,is_template.is.null').execute()
        camps_list = response_unit.data

        if adherent_id:
            response_guests = db.table('camp_guests').select('camp_id').eq('adherent_id', adherent_id).execute()
            guest_camp_ids = [item['camp_id'] for item in response_guests.data]

            if guest_camp_ids:
                response_invited = db.table('camps').select('*').in_('id', guest_camp_ids).or_('is_template.eq.false,is_template.is.null').execute()
                
                existing_ids = {c['id'] for c in camps_list}
                for c in response_invited.data:
                    if c['id'] not in existing_ids:
                        camps_list.append(c)

        camps_list.sort(key=lambda x: x['start_date'])

        return jsonify({"status": "success", "data": camps_list}), 200
    except Exception as e:
        logging.error(f"Erreur récupération camps : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500

@camps_bp.route('/api/camps/templates', methods=['GET'])
def get_templates():
    """
    Récupère les templates globaux (unit_id IS NULL) et ceux de l'unité (unit_id).
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
    
    unit_id = user_data.get("unit_id")
    try:
        db = get_db()
        # "unit_id.is.null" = global templates, "unit_id.eq.XXX" = unit templates
        res = db.table('camps').select('*').eq('is_template', True).or_(f'unit_id.is.null,unit_id.eq.{unit_id}').execute()
        templates_list = res.data or []
        # Tri: templates globaux en premier, puis alphabétique
        templates_list.sort(key=lambda x: (x.get('unit_id') is not None, x.get('name', '')))
        
        return jsonify({"status": "success", "data": templates_list}), 200
    except Exception as e:
        logging.error(f"Erreur récupération templates : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500
    

@camps_bp.route('/api/camps', methods=['POST'])
def create_camp():
    """
    Crée un nouveau camp et copie les créneaux si un template_id est fourni.
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401
        
    unit_name = user_data["unit_name"]
    unit_id = user_data.get("unit_id")
    db = get_db()
    try:
        data = request.json
        nouveau_camp = {
            "name": data.get("name"),
            "location": data.get("location"),
            "start_date": data.get("startDate") or data.get("start_date"),
            "end_date": data.get("endDate") or data.get("end_date"),
            "unit_name": unit_name,
            "unit_id": data.get("unit_id") or unit_id,
            "is_template": False
        }
        
        response = db.table('camps').insert(nouveau_camp).execute()
        nouveau_camp_obj = response.data[0]
        nouveau_camp_id = nouveau_camp_obj['id']
        
        template_id = data.get("template_id")
        if template_id:
            from datetime import datetime, timedelta
            
            # Fetch template start_date pour le calcul du décalage
            tmpl_res = db.table('camps').select('start_date').eq('id', template_id).execute()
            if tmpl_res.data:
                from zoneinfo import ZoneInfo
                PARIS_TZ = ZoneInfo("Europe/Paris")
                UTC_TZ = ZoneInfo("UTC")
                
                tmpl_dt = datetime.fromisoformat(tmpl_res.data[0]['start_date']).astimezone(PARIS_TZ)
                new_dt = datetime.fromisoformat(nouveau_camp_obj['start_date']).astimezone(PARIS_TZ)
                
                # Alignement à minuit local (Europe/Paris)
                tmpl_base_day = tmpl_dt.date()
                new_base_day = new_dt.date()
                
                # Fetch tous les slots du template
                slots_res = db.table('planning_slots').select('*').eq('camp_id', template_id).execute()
                slots_to_copy = []
                
                for slot in (slots_res.data or []):
                    old_start_local = datetime.fromisoformat(slot['start_time']).astimezone(PARIS_TZ)
                    old_end_local = datetime.fromisoformat(slot['end_time']).astimezone(PARIS_TZ)
                    
                    slot_day_offset = (old_start_local.date() - tmpl_base_day).days
                    target_start_day = new_base_day + timedelta(days=slot_day_offset)
                    slot_duration = old_end_local - old_start_local
                    
                    # Reconstruction en heure locale murale exacte (Europe/Paris) pour éviter les décalages été/hiver (DST)
                    new_start_local = datetime(
                        target_start_day.year, target_start_day.month, target_start_day.day,
                        old_start_local.hour, old_start_local.minute, old_start_local.second,
                        tzinfo=PARIS_TZ
                    )
                    new_end_local = new_start_local + slot_duration
                    
                    slots_to_copy.append({
                        "camp_id": nouveau_camp_id,
                        "title": slot.get('title'),
                        "slot_type": slot.get('slot_type'),
                        "start_time": new_start_local.astimezone(UTC_TZ).isoformat(),
                        "end_time": new_end_local.astimezone(UTC_TZ).isoformat()
                        # activity_id N'EST PAS COPIÉ (les fiches restent vierges)
                    })
                
                if slots_to_copy:
                    db.table('planning_slots').insert(slots_to_copy).execute()


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
    
@camps_bp.route('/api/camps/<camp_id>/roster', methods=['GET'])
def get_camp_roster(camp_id):
    """
    Récupère la liste de tous les membres (jeunes et chefs) 
    appartenant à l'unité de ce camp spécifique, 
    ainsi que les chefs invités (guests) enregistrés pour ce camp.
    """
    try:
        db = get_db()
        
        # 1. On trouve à quelle unité appartient ce camp
        camp_res = db.table('camps').select('unit_id').eq('id', camp_id).execute()
        if not camp_res.data:
            return jsonify({"error": "Camp introuvable"}), 404
            
        unit_id = camp_res.data[0].get('unit_id')
        roster_members = []
        
        # 2. On récupère tous les membres de cette unité depuis unit_members
        if unit_id:
            members_res = db.table('unit_members').select('*').eq('unit_id', unit_id).execute()
            if members_res.data:
                roster_members = members_res.data
        
        # 3. On récupère les chefs invités (guests) pour ce camp
        guests_res = db.table('camp_guests').select('adherent_id').eq('camp_id', camp_id).execute()
        if guests_res.data:
            guest_ids = [str(item['adherent_id']).strip() for item in guests_res.data if item.get('adherent_id')]
            
            existing_ids = {str(m['adherent_id']).strip() for m in roster_members if m.get('adherent_id')}
            missing_guest_ids = [gid for gid in guest_ids if gid not in existing_ids]
            
            if missing_guest_ids:
                guest_members_res = db.table('unit_members').select('*').in_('adherent_id', missing_guest_ids).execute()
                found_guests = guest_members_res.data if guest_members_res.data else []
                roster_members.extend(found_guests)
                
                found_ids = {str(g['adherent_id']).strip() for g in found_guests if g.get('adherent_id')}
                still_missing = [gid for gid in missing_guest_ids if gid not in found_ids]
                
                for missing_id in still_missing:
                    mapping = db.table('chef_mappings').select('*').eq('adherent_id', missing_id).execute()
                    unit_label = f" ({mapping.data[0]['unit_name']})" if mapping.data and mapping.data[0].get('unit_name') else ""
                    
                    roster_members.append({
                        "adherent_id": missing_id,
                        "first_name": "Chef",
                        "last_name": f"Invité{unit_label}",
                        "is_jeune": False,
                        "is_chef": True,
                        "unit_id": None
                    })
        
        return jsonify({"status": "success", "data": roster_members}), 200
        
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du roster : {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@camps_bp.route('/api/camps/<camp_id>/make-template', methods=['POST'])
def make_template(camp_id):
    """
    Transforme un week-end existant en modèle personnalisé pour l'unité.
    Les créneaux sont copiés (sans le contenu des fiches d'activité/repas).
    """
    user_data = get_user_session()
    if not user_data:
        return jsonify({"status": "error", "message": "Non autorisé"}), 401

    try:
        db = get_db()
        data = request.json
        template_name = data.get("name", "Nouveau modèle")
        
        # 1. Fetch l'original
        camp_res = db.table('camps').select('*').eq('id', camp_id).execute()
        if not camp_res.data:
            return jsonify({"status": "error", "message": "Camp introuvable"}), 404
            
        original_camp = camp_res.data[0]
        
        # 2. Créer le nouveau template camp
        nouveau_template = {
            "name": template_name,
            "location": original_camp.get('location'),
            "start_date": original_camp.get('start_date'),
            "end_date": original_camp.get('end_date'),
            "unit_name": original_camp.get('unit_name'),
            "unit_id": original_camp.get('unit_id'),
            "is_template": True
        }
        
        res = db.table('camps').insert(nouveau_template).execute()
        nouveau_template_id = res.data[0]['id']
        
        # 3. Copier les créneaux sans l'activity_id
        slots_res = db.table('planning_slots').select('*').eq('camp_id', camp_id).execute()
        slots_to_copy = []
        for slot in (slots_res.data or []):
            slots_to_copy.append({
                "camp_id": nouveau_template_id,
                "title": slot.get('title'),
                "slot_type": slot.get('slot_type'),
                "start_time": slot.get('start_time'),
                "end_time": slot.get('end_time')
            })
            
        if slots_to_copy:
            db.table('planning_slots').insert(slots_to_copy).execute()
            
        return jsonify({"status": "success", "message": "Modèle créé avec succès"}), 201
    except Exception as e:
        logging.error(f"Erreur création template : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500