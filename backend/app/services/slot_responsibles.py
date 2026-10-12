"""
Noms des chefs responsables de chaque créneau, stockés dans un fichier JSON partagé
par tous les processus Gunicorn (volume Docker api_data).

Plusieurs requêtes peuvent écrire en même temps (ex : le bouton « +15 min » envoie une
requête par créneau). Chaque modification se fait donc sous verrou exclusif, et le fichier
est remplacé d'un bloc (écriture dans un fichier temporaire puis renommage) : un lecteur
ne voit jamais un fichier à moitié écrit.
"""
import fcntl
import json
import logging
import os
import tempfile
from contextlib import contextmanager
from typing import Dict, Iterable

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RESPONSIBLES_FILE = os.path.join(DATA_DIR, 'slot_responsibles.json')
LOCK_FILE = RESPONSIBLES_FILE + '.lock'


@contextmanager
def _file_lock(exclusive: bool):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOCK_FILE, 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _read() -> Dict[str, str]:
    if not os.path.exists(RESPONSIBLES_FILE):
        return {}
    with open(RESPONSIBLES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write(data: Dict[str, str]) -> None:
    fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix='.tmp')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, RESPONSIBLES_FILE)


def load_slot_responsibles() -> Dict[str, str]:
    """Lecture seule : en cas de fichier illisible, on affiche le planning sans responsables."""
    try:
        with _file_lock(exclusive=False):
            return _read()
    except (OSError, ValueError) as e:
        logging.error(f"Lecture des responsables de créneaux impossible : {e}")
        return {}


def set_slot_responsible(slot_id, responsible_names) -> None:
    """
    Enregistre (ou efface si vide) le responsable d'un créneau.
    En cas de fichier illisible, l'erreur est levée : on ne réécrit jamais un fichier
    vide par-dessus les responsables des autres créneaux.
    """
    if not slot_id:
        return
    if isinstance(responsible_names, list):
        value = ", ".join(str(n).strip() for n in responsible_names if str(n).strip())
    else:
        value = str(responsible_names).strip() if responsible_names else ''

    with _file_lock(exclusive=True):
        data = _read()
        if value:
            data[str(slot_id)] = value
        else:
            data.pop(str(slot_id), None)
        _write(data)


def remove_slot_responsibles(slot_ids: Iterable) -> None:
    """Retire les responsables de créneaux supprimés."""
    ids = {str(slot_id) for slot_id in slot_ids}
    if not ids:
        return
    with _file_lock(exclusive=True):
        data = _read()
        for slot_id in ids:
            data.pop(slot_id, None)
        _write(data)
