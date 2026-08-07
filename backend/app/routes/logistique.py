import logging
from flask import Blueprint, request, jsonify
from database import get_db

logistique_bp = Blueprint('logistique', __name__)

@logistique_bp.route('/api/tents', methods=['GET'])
def get_tents():
    """
    Récupère le catalogue des tentes d'un groupe.
    Filtre automatiquement les tentes déjà réservées si un camp_id est fourni.
    """
    group_name = request.args.get('group_name')
    camp_id = request.args.get('camp_id')
    
    if not group_name:
        return jsonify({"error": "Nom de groupe manquant"}), 400

    try:
        db = get_db()
        tents_res = db.table('tents').select('*').eq('group_name', group_name).execute()
        tentes = tents_res.data

        if camp_id and camp_id != 'undefined':
            camp_res = db.table('camps').select('start_date, end_date').eq('id', camp_id).execute()
            
            if camp_res.data:
                mon_debut = camp_res.data[0]['start_date']
                ma_fin = camp_res.data[0]['end_date'] if camp_res.data[0].get('end_date') else mon_debut

                autres_camps_res = db.table('camps').select('id, start_date, end_date').neq('id', camp_id).execute()
                
                camps_en_meme_temps = []
                for c in autres_camps_res.data:
                    son_debut = c['start_date']
                    sa_fin = c['end_date'] if c.get('end_date') else son_debut
                    
                    if mon_debut <= sa_fin and ma_fin >= son_debut:
                        camps_en_meme_temps.append(c['id'])

                if camps_en_meme_temps:
                    reserv_res = db.table('camp_tents').select('tent_id').in_('camp_id', camps_en_meme_temps).execute()
                    tentes_prises = [r['tent_id'] for r in reserv_res.data]

                    for t in tentes:
                        if t['id'] in tentes_prises:
                            t['status'] = 'deja_reservee'
                            
        return jsonify({"status": "success", "data": tentes}), 200
    except Exception as e:
        logging.error(f"Erreur récupération tentes : {e}")
        return jsonify({"error": "Erreur serveur"}), 500


@logistique_bp.route('/api/camps/<camp_id>/tents', methods=['GET', 'POST'])
def manage_camp_tents(camp_id):
    """
    Gère la sélection des tentes pour un camp spécifique.
    """
    db = get_db()
    
    if request.method == 'GET':
        res = db.table('camp_tents').select('tent_id').eq('camp_id', camp_id).execute()
        selected = [row['tent_id'] for row in res.data]
        return jsonify({"status": "success", "selected": selected}), 200
        
    if request.method == 'POST':
        data = request.json
        selected_tents = data.get('tents', [])
        
        db.table('camp_tents').delete().eq('camp_id', camp_id).execute()
        inserts = [{"camp_id": camp_id, "tent_id": t_id} for t_id in selected_tents]
        if inserts:
            db.table('camp_tents').insert(inserts).execute()
            
        return jsonify({"status": "success", "message": "Tentes mises à jour"}), 200


@logistique_bp.route('/api/incidents', methods=['GET', 'POST'])
def manage_incidents():
    """
    Gère la déclaration et le suivi du matériel abîmé.
    """
    db = get_db()
    
    if request.method == 'GET':
        res = db.table('tent_incidents').select('*, tents(name)').eq('status', 'a_reparer').execute()
        return jsonify({"status": "success", "data": res.data}), 200
        
    if request.method == 'POST':
        data = request.json
        tent_id = data.get('tent_id')
        
        db.table('tent_incidents').insert({
            "tent_id": tent_id,
            "camp_id": data.get('camp_id'),
            "description": data.get('description')
        }).execute()
        
        db.table('tents').update({"status": "abimee"}).eq('id', tent_id).execute()
        return jsonify({"status": "success", "message": "Incident déclaré"}), 200


@logistique_bp.route('/api/camps/<camp_id>/attendance', methods=['GET', 'POST'])
def manage_attendance(camp_id):
    """
    Gère le registre de présence (jeunes et maîtrise) pour un camp.
    """
    db = get_db()
    
    if request.method == 'GET':
        res = db.table('camp_attendance').select('adherent_id').eq('camp_id', camp_id).execute()
        present_ids = [row['adherent_id'] for row in res.data]
        return jsonify({"status": "success", "present": present_ids}), 200
        
    if request.method == 'POST':
        data = request.json
        present_ids = data.get('present_ids', [])
        
        db.table('camp_attendance').delete().eq('camp_id', camp_id).execute()
        inserts = [{"camp_id": camp_id, "adherent_id": str(p_id)} for p_id in present_ids]
        if inserts:
            db.table('camp_attendance').insert(inserts).execute()
            
        return jsonify({"status": "success", "message": "Présences mises à jour"}), 200


# ==========================================
# GESTION DU MATÉRIEL DE CAMP & TEMPLATES
# ==========================================

@logistique_bp.route('/api/camps/<camp_id>/materials', methods=['GET', 'POST'])
def manage_camp_materials(camp_id):
    """
    Gère la checklist de matériel à emporter pour un camp.
    GET: retourne la liste des éléments.
    POST: met à jour la liste des éléments (remplacement / upsert).
    """
    db = get_db()
    
    if request.method == 'GET':
        try:
            res = db.table('camp_materials').select('*').eq('camp_id', camp_id).execute()
            return jsonify({"status": "success", "data": res.data or []}), 200
        except Exception as e:
            logging.error(f"Erreur GET camp materials : {e}")
            return jsonify({"error": "Erreur serveur"}), 500
            
    if request.method == 'POST':
        try:
            data = request.json
            items = data.get('items', [])
            
            # Remplacement destructif de la liste du camp
            db.table('camp_materials').delete().eq('camp_id', camp_id).execute()
            
            if items:
                inserts = [{
                    "camp_id": camp_id,
                    "name": item['name'],
                    "is_checked": item.get('is_checked', False)
                } for item in items if item.get('name')]
                
                if inserts:
                    db.table('camp_materials').insert(inserts).execute()
                    
            res = db.table('camp_materials').select('*').eq('camp_id', camp_id).execute()
            return jsonify({"status": "success", "data": res.data or []}), 200
        except Exception as e:
            logging.error(f"Erreur POST camp materials : {e}")
            return jsonify({"error": "Erreur serveur"}), 500


@logistique_bp.route('/api/material_templates', methods=['GET', 'POST'])
def manage_material_templates():
    """
    GET: Récupère la liste des modèles de matériel.
    POST: Crée un nouveau modèle de matériel.
    """
    db = get_db()
    
    if request.method == 'GET':
        try:
            res = db.table('material_templates').select('*').execute()
            return jsonify({"status": "success", "data": res.data or []}), 200
        except Exception as e:
            logging.error(f"Erreur GET material templates : {e}")
            return jsonify({"error": "Erreur serveur"}), 500
            
    if request.method == 'POST':
        try:
            data = request.json
            tmpl_name = data.get('name', 'Nouveau modèle matériel')
            items = data.get('items', []) # Liste de noms de matériels ex: ["Malle pharma", "Bâche"]
            unit_id = data.get('unit_id')
            
            new_tmpl = {
                "name": tmpl_name,
                "unit_id": unit_id,
                "items": items
            }
            
            res = db.table('material_templates').insert(new_tmpl).execute()
            return jsonify({"status": "success", "data": res.data}), 201
        except Exception as e:
            logging.error(f"Erreur POST material templates : {e}")
            return jsonify({"error": "Erreur serveur"}), 500


@logistique_bp.route('/api/camps/<camp_id>/materials/apply-template', methods=['POST'])
def apply_material_template(camp_id):
    """
    Injecte les éléments d'un modèle de matériel dans la checklist d'un camp.
    """
    db = get_db()
    try:
        data = request.json
        template_id = data.get('template_id')
        
        if not template_id:
            return jsonify({"error": "template_id requis"}), 400
            
        tmpl_res = db.table('material_templates').select('*').eq('id', template_id).execute()
        if not tmpl_res.data:
            return jsonify({"error": "Modèle introuvable"}), 404
            
        items = tmpl_res.data[0].get('items', [])
        
        # Insère les nouveaux éléments sans supprimer les existants (ou cumule)
        inserts = [{
            "camp_id": camp_id,
            "name": name,
            "is_checked": False
        } for name in items if name]
        
        if inserts:
            db.table('camp_materials').insert(inserts).execute()
            
        res = db.table('camp_materials').select('*').eq('camp_id', camp_id).execute()
        return jsonify({"status": "success", "data": res.data or []}), 200
    except Exception as e:
        logging.error(f"Erreur application template matériel : {e}")
        return jsonify({"error": "Erreur serveur"}), 500


@logistique_bp.route('/api/material_templates/<template_id>', methods=['DELETE'])
def delete_material_template(template_id):
    """
    Supprime un modèle de matériel par son ID.
    """
    try:
        db = get_db()
        db.table('material_templates').delete().eq('id', template_id).execute()
        return jsonify({"status": "success", "message": "Modèle matériel supprimé avec succès"}), 200
    except Exception as e:
        logging.error(f"Erreur suppression modèle matériel : {e}")
        return jsonify({"error": "Erreur serveur"}), 500