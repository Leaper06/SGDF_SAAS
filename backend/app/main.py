import os
import logging
from flask import Flask, jsonify, send_from_directory, request, abort
from flask_cors import CORS



# --- IMPORTS DES BLUEPRINTS ---
from routes.auth import auth_bp
from routes.camps import camps_bp
from routes.planning import planning_bp
from routes.intendance import intendance_bp
from routes.adherents import adherents_bp
from routes.logistique import logistique_bp
from routes.tents import tents_bp
from routes.locations import locations_bp
from routes.lien import liens_bp
from routes.campPDF import campPDF_bp
from services.permissions import is_valid_upload_signature

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
app.register_blueprint(liens_bp)
app.register_blueprint(campPDF_bp)


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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Sert un fichier uploadé (fiche sanitaire, photo) uniquement via un lien signé
    et non expiré, distribué par l'API aux chefs de l'unité concernée.
    """
    if not is_valid_upload_signature(filename, request.args.get('expires'), request.args.get('signature')):
        abort(403)
    response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'private, max-age=3600'
    return response

if __name__ == '__main__':
    try:
        from seed_templates import seed_templates
        seed_templates()
    except Exception as e:
        logging.warning(f"Impossible d'exécuter le seed des templates : {e}")
    app.run(host='0.0.0.0', debug=True, port=5001)