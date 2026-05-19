import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logging.error("Variables d'environnement Supabase manquantes. Vérifie ton fichier .env.")
    raise ValueError("Missing Supabase credentials")

# Initialisation du client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    """
    Retourne l'instance du client Supabase.
    Utile si on veut un jour gérer un pool de connexions plus complexe.
    """
    return supabase