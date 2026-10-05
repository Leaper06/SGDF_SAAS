import logging
import threading
import requests
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Chaque connexion lance un navigateur Chromium (~160 Mo de RAM). On limite le nombre de
# navigateurs simultanés par processus Gunicorn pour qu'un afflux de connexions
# (ex : le jour du lancement) ne sature pas la mémoire du serveur.
MAX_CONCURRENT_BROWSERS = 4
BROWSER_WAIT_SECONDS = 45
_browser_slots = threading.BoundedSemaphore(MAX_CONCURRENT_BROWSERS)


class ServerBusyError(Exception):
    """Trop de connexions simultanées : aucun navigateur disponible à temps."""


def get_sgdf_cookies(username: str, password: str) -> Optional[List[Dict]]:
    """
    Authentifie l'utilisateur via un navigateur headless et recupere les cookies de session.
    Lève ServerBusyError si aucun navigateur ne se libère à temps.
    """
    if not _browser_slots.acquire(timeout=BROWSER_WAIT_SECONDS):
        raise ServerBusyError()
    try:
        return _login_with_browser(username, password)
    finally:
        _browser_slots.release()


def _login_with_browser(username: str, password: str) -> Optional[List[Dict]]:
    try:
        with sync_playwright() as p:
            
            browser = p.chromium.launch(headless=True, timeout=15000)
            context = browser.new_context()
            page = context.new_page()
            # Chaque action Playwright (navigation, saisie, clic) est limitée à 15 secondes
            page.set_default_timeout(15000)

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