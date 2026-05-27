from flask import Blueprint, request, jsonify
from database import get_db 
import requests
locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/api/locations', methods=['GET'])
def get_locations():
    """
    Récupère les lieux de camp du groupe + les lieux marqués comme "partagés"
    """
    group_name = request.args.get('group_name')
    
    try:
        db = get_db()
        
        # Filtre Supabase : "Lieux de mon groupe" OU "Lieux partagés"
        if group_name:
            # La syntaxe .or_ de Supabase
            filtre = f"group_name.eq.{group_name},is_shared.eq.true"
            res = db.table('camp_locations').select('*').or_(filtre).execute()
        else:
            # Sécurité si le front-end n'envoie pas de groupe
            res = db.table('camp_locations').select('*').execute()
            
        return jsonify({"status": "success", "data": res.data}), 200
        
    except Exception as e:
        import logging
        logging.error(f"Erreur de récupération des lieux : {e}")
        return jsonify({"error": "Erreur serveur"}), 500

@locations_bp.route('/api/locations', methods=['POST', 'OPTIONS'])
def add_location():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json or {}
    
    # 1. On récupère l'adresse envoyée par le front-end
    address = data.get('address')
    lat = None
    lon = None
    # 2. GÉOCODAGE CÔTÉ SERVEUR (Via data.gouv.fr)
    if address:
        try:
            url = "https://api-adresse.data.gouv.fr/search/"
            params = {
                'q': address,
                'limit': 1 # On ne veut que le meilleur résultat
            }
            
            # Un timeout de 5 secondes suffit largement pour cette API très rapide
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status() 
            
            geo_data = resp.json()
            
            # L'API renvoie les données au format GeoJSON
            if geo_data.get('features') and len(geo_data['features']) > 0:
                # Attention : le format GeoJSON donne toujours [Longitude, Latitude]
                coords = geo_data['features'][0]['geometry']['coordinates']
                lon = float(coords[0])
                lat = float(coords[1])
                
        except requests.exceptions.Timeout:
            import logging
            logging.warning(f"L'API Adresse a mis trop de temps pour '{address}'")
        except Exception as e:
            import logging
            logging.warning(f"Le géocodage a échoué pour l'adresse '{address}' : {e}")
    # 3. ENREGISTREMENT EN BASE DE DONNÉES
    try:
        db = get_db()
        
        db.table('camp_locations').insert({
            'name': data.get('name'),
            'address': address,
            'contact_info': data.get('contact_info'),
            'description': data.get('description'),
            'is_shared': data.get('is_shared', False),
            'group_name': data.get('group_name'),
            'latitude': lat, # Les coordonnées trouvées par Python
            'longitude': lon
        }).execute()
        
        return jsonify({"status": "success"}), 201
        
    except Exception as e:
        import logging
        logging.error(f"Erreur d'ajout de lieu : {e}")
        return jsonify({"error": "Erreur serveur"}), 500