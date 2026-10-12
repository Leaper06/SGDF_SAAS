from typing import List, Optional

from database import get_db


def replace_rows(table: str, parent_column: str, parent_id, new_rows: List[dict], key: Optional[str] = None) -> None:
    """
    Remplace toutes les lignes d'une liste rattachée à un parent
    (ex : les étapes d'une activité, les présents d'un camp).

    Les nouvelles lignes sont insérées AVANT de supprimer les anciennes :
    si l'insertion échoue (Supabase lent, coupure), l'ancien contenu est intact.
    Au pire, si la suppression échoue ensuite, il reste des doublons, jamais une perte.

    `key` : colonne qui identifie un élément de la liste (ex : adherent_id pour les présents).
    Indispensable quand la table interdit les doublons (contrainte d'unicité) : on n'insère
    alors que les nouveaux éléments et on ne supprime que ceux qui ont disparu.
    """
    db = get_db()
    columns = f'id, {key}' if key else 'id'
    old_rows = db.table(table).select(columns).eq(parent_column, parent_id).execute().data

    if key:
        existing_keys = {str(row[key]) for row in old_rows}
        new_keys = {str(row[key]) for row in new_rows}
        rows_to_insert = [row for row in new_rows if str(row[key]) not in existing_keys]
        ids_to_delete = [row['id'] for row in old_rows if str(row[key]) not in new_keys]
    else:
        rows_to_insert = new_rows
        ids_to_delete = [row['id'] for row in old_rows]

    if rows_to_insert:
        db.table(table).insert(rows_to_insert).execute()
    if ids_to_delete:
        db.table(table).delete().in_('id', ids_to_delete).execute()
