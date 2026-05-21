from bs4 import BeautifulSoup
import requests
import logging
from typing import Dict
import re
from urllib.parse import urljoin

def scrape_liste_adherents(session: requests.Session) -> Dict:
    """
    Récupère la liste des adhérents ET le nom de la structure.
    Retourne un dictionnaire : {"unit_name": str, "adherents": list}
    """
    url_adherents = "https://intranet.sgdf.fr/Specialisation/Sgdf/adherents/ListeAdherents.aspx"
    data_adherents = []
    unit_name = "Unité Inconnue" # Valeur par défaut

    try:
        logging.info(f"Requete GET vers {url_adherents}")
        response = session.get(url_adherents, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 1. SCRAPING DU NOM DE L'UNITÉ ---
        select_element = soup.find('select', id='ctl00_MainContent__navigateur__ddStructure')
        if select_element:
            selected_option = select_element.find('option', selected=True)
            if selected_option:
                raw_name = selected_option.get_text(strip=True)
                # On coupe au niveau du tiret pour enlever le numéro (ex: "702211721 - MOUSSES...")
                if " - " in raw_name:
                    unit_name = raw_name.split(" - ", 1)[1]
                else:
                    unit_name = raw_name

        # --- 2. SCRAPING DU TABLEAU ---
        tables = soup.find_all('table')
        if not tables:
            logging.warning("Aucun tableau HTML trouve sur la page des adherents.")
            return {"unit_name": unit_name, "adherents": data_adherents}

        tableau_principal = max(tables, key=lambda t: len(t.find_all('tr')))
        lignes = tableau_principal.find_all('tr')
        
        for ligne in lignes:
            cellules = [cellule.get_text(strip=True) for cellule in ligne.find_all(['th', 'td'])]
            if cellules:
                data_adherents.append(cellules)

        logging.info(f"{len(data_adherents)} lignes d'adherents recuperees.")
        return {"unit_name": unit_name, "adherents": data_adherents}

    except requests.RequestException as e:
        logging.error(f"Erreur reseau : {e}")
        return {"unit_name": unit_name, "adherents": data_adherents}
    except Exception as e:
        logging.error(f"Erreur de parsing : {e}")
        return {"unit_name": unit_name, "adherents": data_adherents}
import re
import logging
from bs4 import BeautifulSoup
import requests

def scrape_details_adherent(session: requests.Session, url_fiche: str) -> dict:
    """
    Visite la page ResumeAdherent.aspx d'un membre et extrait ses infos de contact.
    """
    details = {
        "adherent_id": None,
        "email": None,
        "telephone": None
    }
    
    # MAGIE : urljoin gère tous les cas (avec ou sans slash, absolu ou relatif)
    url_fiche = urljoin("https://intranet.sgdf.fr/", url_fiche)

    try:
        logging.info(f"Recherche de la fiche détaillée sur : {url_fiche}")
        response = session.get(url_fiche, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Récupération du Code adhérent
        lbl_code = soup.find(string=re.compile("Code adhérent", re.IGNORECASE))
        if lbl_code:
            details['adherent_id'] = lbl_code.find_next(['td', 'span', 'div']).get_text(strip=True)

        # 2. Récupération de l'Email
        lbl_email = soup.find(string=re.compile("Courriel personnel", re.IGNORECASE))
        if lbl_email:
            details['email'] = lbl_email.find_next(['td', 'span', 'div']).get_text(strip=True)

        # 3. Récupération du Téléphone
        lbl_tel = soup.find(string=re.compile("Portable :", re.IGNORECASE))
        if lbl_tel:
            tel_text = lbl_tel.find_next(['td', 'span', 'div']).get_text(strip=True)
            if tel_text:
                details['telephone'] = tel_text

        return details

    except Exception as e:
        logging.error(f"Erreur lors du scraping de la fiche détaillée : {e}")
        return details
    
def get_logged_in_chef_info(session: requests.Session) -> dict:
    """
    Trouve la page de profil du chef actuellement connecté et scrape ses infos.
    """
    try:
        # On charge la page d'accueil de l'intranet
        rep = session.get("https://intranet.sgdf.fr/")
        soup = BeautifulSoup(rep.text, 'html.parser')
        
        # Sur l'intranet, le lien vers le profil est souvent caché dans le menu haut 
        # (souvent sous la forme d'un lien contenant "ResumeAdherent.aspx")
        lien_profil = soup.find('a', href=re.compile("ResumeAdherent.aspx"))
        
        if lien_profil and 'href' in lien_profil.attrs:
            url_profil = lien_profil['href']
            # On lance notre super scraper sur cette URL !
            return scrape_details_adherent(session, url_profil)
            
    except Exception as e:
        logging.error(f"Impossible de trouver le profil du chef : {e}")
        
    return {"adherent_id": None, "email": None, "telephone": None}