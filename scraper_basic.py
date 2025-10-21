"""
Basis webscraper voor pagina's met login functionaliteit.
Gebruikt requests en BeautifulSoup voor statische pagina's.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import time
from urllib.parse import urljoin


class BasicLoginScraper:
    """
    Een webscraper die kan inloggen op websites en pagina's kan scrapen.
    Geschikt voor statische websites zonder veel JavaScript.
    """

    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        """
        Initialiseer de scraper.

        Args:
            base_url: De basis URL van de website
            headers: Optionele HTTP headers
        """
        self.base_url = base_url
        self.session = requests.Session()

        # Standaard headers om een echte browser na te bootsen
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

        if headers:
            default_headers.update(headers)

        self.session.headers.update(default_headers)
        self.logged_in = False

    def login_form(self, login_url: str, credentials: Dict[str, str],
                   form_data: Optional[Dict] = None) -> bool:
        """
        Log in via een HTML formulier.

        Args:
            login_url: URL van de login pagina
            credentials: Dictionary met username/password
            form_data: Extra formulier velden (bijv. CSRF tokens)

        Returns:
            True als login succesvol was
        """
        try:
            # Haal eerst de login pagina op om eventuele CSRF tokens te krijgen
            response = self.session.get(urljoin(self.base_url, login_url))
            response.raise_for_status()

            # Parse de pagina voor CSRF tokens of andere hidden fields
            soup = BeautifulSoup(response.text, 'lxml')
            login_form = soup.find('form')

            # Bouw de POST data
            post_data = {}

            # Voeg hidden fields toe
            if login_form:
                for hidden in login_form.find_all('input', type='hidden'):
                    name = hidden.get('name')
                    value = hidden.get('value', '')
                    if name:
                        post_data[name] = value

            # Voeg credentials toe
            post_data.update(credentials)

            # Voeg extra form data toe als die er is
            if form_data:
                post_data.update(form_data)

            # Probeer in te loggen
            response = self.session.post(
                urljoin(self.base_url, login_url),
                data=post_data,
                allow_redirects=True
            )
            response.raise_for_status()

            # Controleer of we ingelogd zijn (dit is site-specifiek)
            # Als de response tekst geen login form meer bevat, zijn we waarschijnlijk ingelogd
            self.logged_in = 'login' not in response.url.lower()

            return self.logged_in

        except requests.RequestException as e:
            print(f"Login fout: {e}")
            return False

    def login_basic_auth(self, username: str, password: str) -> bool:
        """
        Log in met HTTP Basic Authentication.

        Args:
            username: Gebruikersnaam
            password: Wachtwoord

        Returns:
            True als login succesvol was
        """
        try:
            self.session.auth = (username, password)
            response = self.session.get(self.base_url)
            response.raise_for_status()
            self.logged_in = True
            return True
        except requests.RequestException as e:
            print(f"Basic auth fout: {e}")
            return False

    def login_with_token(self, token: str, token_type: str = "Bearer") -> bool:
        """
        Log in met een API token.

        Args:
            token: De API token
            token_type: Type token (Bearer, Token, etc.)

        Returns:
            True als login succesvol was
        """
        try:
            self.session.headers['Authorization'] = f"{token_type} {token}"
            response = self.session.get(self.base_url)
            response.raise_for_status()
            self.logged_in = True
            return True
        except requests.RequestException as e:
            print(f"Token auth fout: {e}")
            return False

    def scrape_page(self, url: str, wait_time: float = 0) -> Optional[BeautifulSoup]:
        """
        Scrape een enkele pagina.

        Args:
            url: URL van de pagina (kan relatief zijn)
            wait_time: Tijd in seconden om te wachten tussen requests

        Returns:
            BeautifulSoup object of None bij een fout
        """
        if wait_time > 0:
            time.sleep(wait_time)

        try:
            full_url = urljoin(self.base_url, url)
            response = self.session.get(full_url)
            response.raise_for_status()

            return BeautifulSoup(response.text, 'lxml')

        except requests.RequestException as e:
            print(f"Scraping fout voor {url}: {e}")
            return None

    def scrape_multiple_pages(self, urls: List[str],
                             wait_time: float = 1.0) -> Dict[str, BeautifulSoup]:
        """
        Scrape meerdere pagina's.

        Args:
            urls: Lijst van URLs om te scrapen
            wait_time: Tijd om te wachten tussen requests

        Returns:
            Dictionary met URLs als keys en BeautifulSoup objecten als values
        """
        results = {}

        for url in urls:
            soup = self.scrape_page(url, wait_time)
            if soup:
                results[url] = soup

        return results

    def extract_data(self, soup: BeautifulSoup, selector: str,
                     attribute: Optional[str] = None) -> List[str]:
        """
        Extraheer data van een pagina met CSS selectors.

        Args:
            soup: BeautifulSoup object van de pagina
            selector: CSS selector voor de elementen
            attribute: Optioneel attribuut om te extracten (bijv. 'href', 'src')

        Returns:
            Lijst met geëxtraheerde tekst of attributen
        """
        elements = soup.select(selector)

        if attribute:
            return [elem.get(attribute, '') for elem in elements if elem.get(attribute)]
        else:
            return [elem.get_text(strip=True) for elem in elements]

    def save_to_file(self, content: str, filename: str) -> None:
        """
        Sla content op naar een bestand.

        Args:
            content: De content om op te slaan
            filename: Naam van het bestand
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_cookies(self) -> Dict:
        """
        Haal de huidige cookies op.

        Returns:
            Dictionary met cookies
        """
        return self.session.cookies.get_dict()

    def set_cookies(self, cookies: Dict) -> None:
        """
        Stel cookies in.

        Args:
            cookies: Dictionary met cookies
        """
        self.session.cookies.update(cookies)

    def logout(self) -> None:
        """
        Log uit en reset de sessie.
        """
        self.session.close()
        self.session = requests.Session()
        self.logged_in = False


# Voorbeeld gebruik
if __name__ == "__main__":
    # Voorbeeld 1: Login via formulier
    scraper = BasicLoginScraper("https://example.com")

    # Login
    credentials = {
        'username': 'gebruikersnaam',
        'password': 'wachtwoord'
    }

    if scraper.login_form('/login', credentials):
        print("Succesvol ingelogd!")

        # Scrape een pagina
        soup = scraper.scrape_page('/dashboard')
        if soup:
            # Extracteer data
            titles = scraper.extract_data(soup, 'h1.title')
            print(f"Gevonden titels: {titles}")

            # Scrape meerdere pagina's
            pages = ['/page1', '/page2', '/page3']
            results = scraper.scrape_multiple_pages(pages)
            print(f"Gescraped {len(results)} pagina's")

        scraper.logout()
    else:
        print("Login mislukt!")
