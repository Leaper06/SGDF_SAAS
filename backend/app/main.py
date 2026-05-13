import os
import uuid
import logging
from flask import Flask, request, jsonify

# Import de tes services métiers
from services.sgdf_auth import get_sgdf_cookies, create_authenticated_session
from services.sgdf_adherents import scrape_liste_adherents

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# NOTRE BASE DE DONNÉES TEMPORAIRE (En mémoire)
# Elle va stocker les objets 'requests.Session' associés à un Token unique
ACTIVE_SESSIONS = {}

@app.route('/api/status', methods=['GET'])
def health_check():
    """Route de test pour vérifier que l'API tourne bien."""
    return jsonify({"status": "ok", "message": "API PolyMaîtrise opérationnelle"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    """Route pour s'authentifier et récupérer un token de session."""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Identifiants manquants (username, password attendus)"}), 400

    username = data['username']
    password = data['password']

    logging.info(f"Tentative de connexion pour l'utilisateur : {username}")
    
    # 1. On lance Playwright pour récupérer les cookies
    cookies = get_sgdf_cookies(username, password)
    
    if not cookies:
        return jsonify({"error": "Échec de l'authentification. Vérifiez les identifiants."}), 401

    # 2. On crée la session HTTP rapide
    session_http = create_authenticated_session(cookies)
    
    # 3. On génère un Token unique pour cet utilisateur
    session_token = str(uuid.uuid4())
    
    # 4. On stocke la session en mémoire
    ACTIVE_SESSIONS[session_token] = session_http
    
    logging.info(f"Connexion réussie. Token généré : {session_token}")
    
    return jsonify({
        "message": "Connexion réussie",
        "token": session_token
    }), 200

@app.route('/api/adherents', methods=['GET'])
def get_adherents():
    """Route pour récupérer la liste des adhérents (nécessite un token valide)."""
    # On cherche le token dans les en-têtes de la requête (Headers)
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token d'authentification manquant ou mal formaté"}), 401
        
    # On extrait le token brut (on enlève "Bearer ")
    token = auth_header.split(" ")[1]
    
    # On vérifie si ce token existe dans notre mémoire
    if token not in ACTIVE_SESSIONS:
        return jsonify({"error": "Token invalide ou session expirée. Veuillez vous reconnecter."}), 401
        
    logging.info(f"Requête adhérents autorisée pour le token : {token}")
    
    # On récupère la session HTTP de cet utilisateur spécifique
    user_session = ACTIVE_SESSIONS[token]
    
    # On lance le scraping !
    adherents_data = scrape_liste_adherents(user_session)
    
    if not adherents_data:
        return jsonify({"error": "Impossible de récupérer les données ou liste vide."}), 500
        
    # On renvoie les données structurées en JSON
    return jsonify({
        "count": len(adherents_data) - 1, # -1 pour ne pas compter la ligne des titres
        "data": adherents_data
    }), 200

if __name__ == '__main__':
    # On lance le serveur Flask sur le port 5000
    logging.info("Démarrage du serveur Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)