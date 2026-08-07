import sys
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Permet d'importer le module backend depuis le dossier app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from database import get_db

PARIS_TZ = ZoneInfo("Europe/Paris")
UTC_TZ = ZoneInfo("UTC")

def seed_templates():
    db = get_db()
    json_path = os.path.join(os.path.dirname(__file__), 'templates_config.json')
    
    if not os.path.exists(json_path):
        print(f"Fichier de configuration non trouvé : {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        templates_config = json.load(f)

    print(f"Chargement de {len(templates_config)} modèles depuis templates_config.json...")
    
    # Nettoyage des anciens templates globaux absents du fichier JSON
    valid_names = [t.get('name') for t in templates_config if t.get('name')]
    existing_globals = db.table('camps').select('id, name').eq('is_template', True).is_('unit_id', 'null').execute()
    
    for g_tmpl in (existing_globals.data or []):
        if g_tmpl['name'] not in valid_names:
            print(f"Suppression de l'ancien template obsolète : '{g_tmpl['name']}'...")
            db.table('planning_slots').delete().eq('camp_id', g_tmpl['id']).execute()
            db.table('camps').delete().eq('id', g_tmpl['id']).execute()

    # Date de référence canonique pour Day 0 = Samedi 3 Janvier 2026 en heure de Paris
    base_date = datetime(2026, 1, 3, 0, 0, 0, tzinfo=PARIS_TZ)
    
    for tmpl in templates_config:
        tmpl_name = tmpl.get('name')
        location = tmpl.get('location', 'Local')
        slots = tmpl.get('slots', [])
        
        if not tmpl_name or not slots:
            continue
            
        max_offset = max(s.get('day_offset', 0) for s in slots)
        
        start_date_obj = base_date
        end_date_obj = (base_date + timedelta(days=max_offset)).replace(hour=23, minute=59, second=59)

        # Recherche si le template existe déjà
        existing = db.table('camps').select('id').eq('name', tmpl_name).eq('is_template', True).is_('unit_id', 'null').execute()
        
        if existing.data:
            camp_id = existing.data[0]['id']
            print(f"Mise à jour du template '{tmpl_name}' (ID: {camp_id})...")
            db.table('planning_slots').delete().eq('camp_id', camp_id).execute()
        else:
            # Création du camp template
            new_camp = {
                "name": tmpl_name,
                "location": location,
                "start_date": start_date_obj.astimezone(UTC_TZ).isoformat(),
                "end_date": end_date_obj.astimezone(UTC_TZ).isoformat(),
                "unit_name": "SGDF",
                "unit_id": None,
                "is_template": True
            }
            res = db.table('camps').insert(new_camp).execute()
            camp_id = res.data[0]['id']
            print(f"Nouveau template '{tmpl_name}' créé avec succès (ID: {camp_id}).")

        # Insertion des créneaux en converting l'heure locale Europe/Paris vers UTC ISO
        slots_to_insert = []
        for slot in slots:
            offset_days = slot.get('day_offset', 0)
            slot_day = base_date + timedelta(days=offset_days)
            
            h_s, m_s = map(int, slot.get('start_time').split(':'))
            h_e, m_e = map(int, slot.get('end_time').split(':'))
            
            slot_start_local = datetime(slot_day.year, slot_day.month, slot_day.day, h_s, m_s, tzinfo=PARIS_TZ)
            slot_end_local = datetime(slot_day.year, slot_day.month, slot_day.day, h_e, m_e, tzinfo=PARIS_TZ)
            
            s_time = slot_start_local.astimezone(UTC_TZ).isoformat()
            e_time = slot_end_local.astimezone(UTC_TZ).isoformat()
            
            slots_to_insert.append({
                "camp_id": camp_id,
                "title": slot.get('title'),
                "slot_type": slot.get('slot_type', 'jeu'),
                "start_time": s_time,
                "end_time": e_time
            })
            
        if slots_to_insert:
            db.table('planning_slots').insert(slots_to_insert).execute()
            print(f"  -> {len(slots_to_insert)} créneaux resynchronisés pour le template.")

if __name__ == '__main__':
    seed_templates()
