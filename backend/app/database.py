import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logging.error("Variables d'environnement Supabase manquantes. Vérifie ton fichier .env.")
    raise ValueError("Missing Supabase credentials")

# Délai max (en secondes) d'une requête Supabase. Doit rester bien en dessous
# du timeout de Nginx (60 s) pour qu'une lenteur de Supabase ne bloque pas les threads.
SUPABASE_TIMEOUT = 15

# Initialisation du client Supabase
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(postgrest_client_timeout=SUPABASE_TIMEOUT),
)

def get_db():
    """
    Retourne l'instance du client Supabase.
    Utile si on veut un jour gérer un pool de connexions plus complexe.
    """
    return supabase