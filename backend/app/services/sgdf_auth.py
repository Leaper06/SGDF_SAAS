import logging
import requests
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def get_sgdf_cookies(username: str, password: str) -> Optional[List[Dict]]:
    """
    Authentifie l'utilisateur via un navigateur headless et recupere les cookies de session.
    """
    try:
        with sync_playwright() as p:
            
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            logging.info("Navigation vers l'intranet SGDF...")
            page.goto("https://intranet.sgdf.fr/")

            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            page.locator("#kc-login").click()

            logging.info("Attente de la redirection post-login...")
            # Timeout augmente a 15 secondes pour les connexions lentes
            page.wait_for_url("https://intranet.sgdf.fr/**", timeout=15000)
            
            cookies = context.cookies()
            return cookies

    except PlaywrightTimeoutError:
        logging.error("Delai d'attente depasse lors de la connexion. Verifiez vos identifiants ou la lenteur du site.")
        return None
    except Exception as e:
        logging.error(f"Erreur inattendue lors de la recuperation des cookies : {e}")
        return None

def create_authenticated_session(cookies: List[Dict]) -> requests.Session:
    """
    Transforme les cookies bruts (issus de Playwright) en une session HTTP 'requests' prete a l'emploi.
    """
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return session