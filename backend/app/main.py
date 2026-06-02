import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from werkzeug.utils import secure_filename


# --- IMPORTS DES BLUEPRINTS ---
from routes.auth import auth_bp
from routes.camps import camps_bp
from routes.planning import planning_bp
from routes.intendance import intendance_bp
from routes.adherents import adherents_bp
from routes.logistique import logistique_bp
from  routes.tents import tents_bp
from routes.locations import locations_bp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# --- ENREGISTREMENT DES ROUTES ---
app.register_blueprint(auth_bp)
app.register_blueprint(camps_bp)
app.register_blueprint(planning_bp)
app.register_blueprint(intendance_bp)
app.register_blueprint(adherents_bp)
app.register_blueprint(logistique_bp)
app.register_blueprint(tents_bp)
app.register_blueprint(locations_bp)

@app.route('/api/status', methods=['GET'])
def health_check():
    """Route de supervision pour s'assurer que l'API est UP."""
    return jsonify({"status": "ok", "message": "API PolyMaîtrise opérationnelle"}), 200

# ==========================================
# GESTION DES FICHIERS STATIQUES (Uploads)
# ==========================================
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Gère l'upload de fichiers (photos de profil, etc.)."""
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    file_url = f"/uploads/{filename}"
    return jsonify({"status": "success", "url": file_url}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Sert les fichiers statiques uploadés."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)