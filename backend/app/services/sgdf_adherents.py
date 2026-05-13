
from bs4 import BeautifulSoup
import requests

import logging
from typing import List, Dict
def scrape_liste_adherents(session: requests.Session) -> List[List[str]]:
    """
    Recupere et parse la liste des adherents depuis l'intranet.
    Retourne une liste de lignes (chaque ligne etant une liste de chaines de caracteres).
    """
    url_adherents = "https://intranet.sgdf.fr/Specialisation/Sgdf/adherents/ListeAdherents.aspx"
    data_adherents = []

    try:
        logging.info(f"Requete GET vers {url_adherents}")
        response = session.get(url_adherents, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            logging.warning("Aucun tableau HTML trouve sur la page des adherents.")
            return data_adherents

        # Extraction du tableau avec le plus de lignes
        tableau_principal = max(tables, key=lambda t: len(t.find_all('tr')))
        lignes = tableau_principal.find_all('tr')
        
        for ligne in lignes:
            cellules = [cellule.get_text(strip=True) for cellule in ligne.find_all(['th', 'td'])]
            if cellules:
                data_adherents.append(cellules)

        logging.info(f"{len(data_adherents)} lignes d'adherents recuperees.")
        return data_adherents

    except requests.RequestException as e:
        logging.error(f"Erreur reseau lors du scraping des adherents : {e}")
        return data_adherents
    except Exception as e:
        logging.error(f"Erreur lors du parsing des donnees : {e}")
        return data_adherents