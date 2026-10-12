"""
Suppression d'un week-end ou de créneaux avec toutes leurs données rattachées.

Les clés étrangères de la base ne sont pas en ON DELETE CASCADE : il faut supprimer
les lignes « enfants » avant leurs « parents », sinon la base refuse la suppression
(ex : un créneau repas dont le menu a été ouvert possède une ligne dans meals).
"""
from typing import List

from database import get_db
from services.slot_responsibles import remove_slot_responsibles

# Tables rattachées directement à un camp par une colonne camp_id
CAMP_CHILD_TABLES = ['camp_attendance', 'camp_guests', 'camp_materials', 'camp_tents', 'shopping_lists']

# Tables rattachées à une activité (fiche d'activité d'un créneau)
ACTIVITY_CHILD_TABLES = ['activity_steps', 'activity_materials', 'activity_responsibles']


def delete_activities(activity_ids: List[str]) -> None:
    """Supprime les fiches d'activité qui ne sont plus utilisées par aucun créneau."""
    if not activity_ids:
        return
    db = get_db()
    still_used = db.table('planning_slots').select('activity_id').in_('activity_id', activity_ids).execute().data
    unused_ids = list(set(activity_ids) - {slot['activity_id'] for slot in still_used})
    if not unused_ids:
        return

    for table in ACTIVITY_CHILD_TABLES:
        db.table(table).delete().in_('activity_id', unused_ids).execute()
    db.table('activities').delete().in_('id', unused_ids).execute()


def delete_planning_slots(slot_ids: List[str]) -> None:
    """Supprime des créneaux avec leurs repas, leurs fiches d'activité et leurs responsables."""
    if not slot_ids:
        return
    db = get_db()

    # 1. Repas des créneaux (et les recettes de ces repas)
    meals = db.table('meals').select('id').in_('planning_slot_id', slot_ids).execute().data
    meal_ids = [meal['id'] for meal in meals]
    if meal_ids:
        db.table('meal_recipes').delete().in_('meal_id', meal_ids).execute()
        db.table('meals').delete().in_('id', meal_ids).execute()

    # 2. Les créneaux, puis les fiches d'activité qu'ils référençaient
    slots = db.table('planning_slots').select('activity_id').in_('id', slot_ids).execute().data
    activity_ids = [slot['activity_id'] for slot in slots if slot.get('activity_id')]
    db.table('planning_slots').delete().in_('id', slot_ids).execute()
    delete_activities(activity_ids)

    remove_slot_responsibles(slot_ids)


def delete_camp(camp_id: str):
    """Supprime un week-end (ou un modèle) et tout son contenu. Retourne les lignes supprimées."""
    db = get_db()

    slots = db.table('planning_slots').select('id').eq('camp_id', camp_id).execute().data
    delete_planning_slots([slot['id'] for slot in slots])

    for table in CAMP_CHILD_TABLES:
        db.table(table).delete().eq('camp_id', camp_id).execute()

    return db.table('camps').delete().eq('id', camp_id).execute().data
