import re
from datetime import datetime, timezone
from typing import List, Optional

from database import get_db


def save_unit_and_members(unit_name: str, raw_adherents: List[list]) -> Optional[str]:
    """
    Enregistre l'unité (créée si elle n'existe pas encore) et met à jour ses membres
    à partir du tableau d'adhérents récupéré sur l'intranet SGDF.
    La première ligne du tableau (en-têtes) est ignorée.
    Retourne l'identifiant de l'unité.
    """
    db = get_db()

    unit_res = db.table('units').select('id').eq('name', unit_name).execute()
    if not unit_res.data:
        unit_res = db.table('units').insert({'name': unit_name}).execute()
    if not unit_res.data:
        return None
    unit_id = unit_res.data[0]['id']

    members_to_upsert = []
    for row in raw_adherents[1:]:
        cols = [str(c).strip() for c in row if str(c).strip() != '']
        if len(cols) < 2:
            continue

        # Codes de fonction SGDF : 1xx pour les jeunes, 2xx pour les chefs
        row_text = " ".join(cols)
        name_parts = cols[0].split(" ", 1)

        members_to_upsert.append({
            "adherent_id": cols[1],
            "unit_id": unit_id,
            "first_name": name_parts[1] if len(name_parts) > 1 else "",
            "last_name": name_parts[0],
            "is_jeune": bool(re.search(r'\b1\d{2}\b', row_text)),
            "is_chef": bool(re.search(r'\b2\d{2}\b', row_text)),
            "last_synced_at": datetime.now(timezone.utc).isoformat()
        })

    if members_to_upsert:
        db.table('unit_members').upsert(members_to_upsert).execute()

    return unit_id
