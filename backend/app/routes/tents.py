from flask import Blueprint, request, jsonify
from database import get_db

tents_bp = Blueprint('tents', __name__)

@tents_bp.route('/api/tents/<tent_id>/incident', methods=['PUT', 'OPTIONS'])
def update_tent_incident(tent_id):
    """
    Gère la déclaration d'un incident ou la réparation d'une tente
    en utilisant la table d'historique 'tent_incidents'.
    """
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json or {}
    etat_recu = data.get('etat', '')
    notes = data.get('notes_incident', '')

    try:
        db = get_db()
        
        if etat_recu == 'OK':
            # 1. RÉPARATION : On remet la tente en état
            db.table('tents').update({'status': 'operationnelle'}).eq('id', tent_id).execute()
            # On clôture les incidents ouverts pour cette tente
            db.table('tent_incidents').update({'status': 'repare'}).eq('tent_id', tent_id).eq('status', 'a_reparer').execute()
        else:
            # 2. INCIDENT : On passe la tente en abîmée
            db.table('tents').update({'status': 'abimee'}).eq('id', tent_id).execute()
            # On enregistre le détail dans la table d'historique
            db.table('tent_incidents').insert({
                'tent_id': tent_id,
                'description': notes,
                'status': 'a_reparer'
            }).execute()
            
        return jsonify({"status": "success"}), 200
    except Exception as e:
        import logging
        logging.error(f"Erreur d'incident pour la tente {tent_id}: {e}")
        return jsonify({"error": "Erreur serveur"}), 500


@tents_bp.route('/api/tents/damaged', methods=['GET'])
def get_damaged_tents():
    """
    Récupère les tentes abîmées ET va chercher la description 
    de leur problème dans la table 'tent_incidents'.
    """
    try:
        db = get_db()
        # On récupère toutes les tentes signalées comme abîmées
        tents_res = db.table('tents').select('*').eq('status', 'abimee').execute()
        tents = tents_res.data
        
        # Pour chaque tente, on va chercher son dernier incident non réparé
        for tent in tents:
            incidents_res = db.table('tent_incidents').select('description') \
                .eq('tent_id', tent['id']).eq('status', 'a_reparer') \
                .order('created_at', desc=True).limit(1).execute()
                
            if incidents_res.data:
                # On glisse la description dans l'objet tente pour que Vue.js puisse l'afficher facilement
                tent['notes_incident'] = incidents_res.data[0]['description']
            else:
                tent['notes_incident'] = "Détails non précisés."
                
        return jsonify({"status": "success", "data": tents}), 200
    except Exception as e:
        import logging
        logging.error(f"Erreur de récupération des tentes abîmées: {e}")
        return jsonify({"error": "Erreur serveur"}), 500