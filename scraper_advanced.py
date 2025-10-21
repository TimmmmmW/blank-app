"""
Geavanceerde webscraper voor pagina's met login functionaliteit.
Gebruikt Playwright voor JavaScript-heavy websites.
"""

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Dict, Optional, List, Callable
import time
from pathlib import Path
import json


class AdvancedLoginScraper:
    """
    Een geavanceerde webscraper die Playwright gebruikt voor JavaScript-heavy websites.
    Kan omgaan met dynamische content, AJAX requests, en complexe login flows.
    """

    def __init__(self, base_url: str, headless: bool = True, browser_type: str = "chromium"):
        """
        Initialiseer de scraper.

        Args:
            base_url: De basis URL van de website
            headless: Of de browser in headless mode moet draaien
            browser_type: Type browser (chromium, firefox, webkit)
        """
        self.base_url = base_url
        self.headless = headless
        self.browser_type = browser_type
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.logged_in = False

    def __enter__(self):
        """Context manager support."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()

    def start(self) -> None:
        """Start de browser."""
        if not self.playwright:
            self.playwright = sync_playwright().start()

            # Kies browser type
            if self.browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(headless=self.headless)
            elif self.browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(headless=self.headless)
            else:
                self.browser = self.playwright.chromium.launch(headless=self.headless)

            # Maak een context met standaard settings
            self.context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='nl-NL'
            )

            self.page = self.context.new_page()

    def close(self) -> None:
        """Sluit de browser en cleanup."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
        self.logged_in = False

    def login_form(self, login_url: str, selectors: Dict[str, str],
                   credentials: Dict[str, str],
                   submit_selector: str,
                   success_check: Optional[Callable[[Page], bool]] = None) -> bool:
        """
        Log in via een HTML formulier.

        Args:
            login_url: URL van de login pagina
            selectors: Dictionary met field names als keys en CSS selectors als values
                      bijv. {'username': '#username', 'password': '#password'}
            credentials: Dictionary met field names als keys en waarden
                        bijv. {'username': 'user', 'password': 'pass'}
            submit_selector: CSS selector voor de submit button
            success_check: Optionele functie om te checken of login succesvol was

        Returns:
            True als login succesvol was
        """
        if not self.page:
            self.start()

        try:
            # Ga naar login pagina
            self.page.goto(f"{self.base_url}{login_url}")
            self.page.wait_for_load_state('networkidle')

            # Vul formulier in
            for field, value in credentials.items():
                if field in selectors:
                    selector = selectors[field]
                    self.page.fill(selector, value)

            # Klik op submit button
            self.page.click(submit_selector)

            # Wacht op navigatie
            self.page.wait_for_load_state('networkidle')

            # Check of login succesvol was
            if success_check:
                self.logged_in = success_check(self.page)
            else:
                # Simpele check: zijn we weggenavigeerd van de login pagina?
                self.logged_in = login_url not in self.page.url

            return self.logged_in

        except Exception as e:
            print(f"Login fout: {e}")
            return False

    def login_with_cookies(self, cookies: List[Dict]) -> bool:
        """
        Log in met cookies.

        Args:
            cookies: Lijst met cookie dictionaries

        Returns:
            True als login succesvol was
        """
        if not self.context:
            self.start()

        try:
            self.context.add_cookies(cookies)
            self.page.goto(self.base_url)
            self.page.wait_for_load_state('networkidle')
            self.logged_in = True
            return True
        except Exception as e:
            print(f"Cookie login fout: {e}")
            return False

    def wait_for_login_manual(self, login_url: str, timeout: int = 300000) -> bool:
        """
        Open een browser window en wacht tot gebruiker handmatig inlogt.
        Nuttig voor complexe login flows (OAuth, 2FA, etc.)

        Args:
            login_url: URL van de login pagina
            timeout: Maximum tijd om te wachten (in milliseconden)

        Returns:
            True als succesvol ingelogd
        """
        if not self.page:
            # Start in non-headless mode
            original_headless = self.headless
            self.headless = False
            self.start()
            self.headless = original_headless

        try:
            self.page.goto(f"{self.base_url}{login_url}")

            print(f"Wachten op handmatige login... (timeout: {timeout/1000}s)")
            print("Klik in de browser en log in. De scraper wacht tot je klaar bent.")

            # Wacht tot URL verandert (indicatie van succesvolle login)
            self.page.wait_for_url(lambda url: login_url not in url, timeout=timeout)

            self.logged_in = True
            return True

        except Exception as e:
            print(f"Handmatige login fout: {e}")
            return False

    def scrape_page(self, url: str, wait_time: float = 0,
                   wait_for_selector: Optional[str] = None) -> str:
        """
        Scrape een enkele pagina.

        Args:
            url: URL van de pagina (kan relatief zijn)
            wait_time: Extra tijd om te wachten na laden
            wait_for_selector: Optionele selector om op te wachten

        Returns:
            HTML content van de pagina
        """
        if not self.page:
            self.start()

        try:
            full_url = url if url.startswith('http') else f"{self.base_url}{url}"
            self.page.goto(full_url)
            self.page.wait_for_load_state('networkidle')

            # Wacht op specifieke selector indien opgegeven
            if wait_for_selector:
                self.page.wait_for_selector(wait_for_selector)

            # Extra wachttijd
            if wait_time > 0:
                time.sleep(wait_time)

            return self.page.content()

        except Exception as e:
            print(f"Scraping fout voor {url}: {e}")
            return ""

    def scrape_with_scroll(self, url: str, scroll_count: int = 5,
                          scroll_delay: float = 1.0) -> str:
        """
        Scrape een pagina met infinite scroll.

        Args:
            url: URL van de pagina
            scroll_count: Aantal keer scrollen
            scroll_delay: Delay tussen scrolls in seconden

        Returns:
            HTML content van de pagina
        """
        if not self.page:
            self.start()

        try:
            full_url = url if url.startswith('http') else f"{self.base_url}{url}"
            self.page.goto(full_url)
            self.page.wait_for_load_state('networkidle')

            # Scroll naar beneden meerdere keren
            for i in range(scroll_count):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(scroll_delay)
                self.page.wait_for_load_state('networkidle')

            return self.page.content()

        except Exception as e:
            print(f"Scroll scraping fout voor {url}: {e}")
            return ""

    def extract_data_js(self, selector: str, attribute: Optional[str] = None) -> List[str]:
        """
        Extraheer data met JavaScript.

        Args:
            selector: CSS selector voor de elementen
            attribute: Optioneel attribuut om te extracten

        Returns:
            Lijst met geëxtraheerde tekst of attributen
        """
        if not self.page:
            return []

        try:
            if attribute:
                # Haal attribuut op
                return self.page.eval_on_selector_all(
                    selector,
                    f"elements => elements.map(e => e.{attribute})"
                )
            else:
                # Haal tekst op
                return self.page.eval_on_selector_all(
                    selector,
                    "elements => elements.map(e => e.textContent.trim())"
                )
        except Exception as e:
            print(f"Data extractie fout: {e}")
            return []

    def click_and_scrape(self, click_selector: str,
                        wait_selector: Optional[str] = None,
                        wait_time: float = 1.0) -> str:
        """
        Klik op een element en scrape de resulterende pagina.

        Args:
            click_selector: Selector voor het element om op te klikken
            wait_selector: Selector om op te wachten na klikken
            wait_time: Extra wachttijd

        Returns:
            HTML content na klikken
        """
        if not self.page:
            return ""

        try:
            self.page.click(click_selector)

            if wait_selector:
                self.page.wait_for_selector(wait_selector)
            else:
                self.page.wait_for_load_state('networkidle')

            time.sleep(wait_time)
            return self.page.content()

        except Exception as e:
            print(f"Click and scrape fout: {e}")
            return ""

    def take_screenshot(self, filename: str, full_page: bool = False) -> None:
        """
        Maak een screenshot van de huidige pagina.

        Args:
            filename: Bestandsnaam voor de screenshot
            full_page: Of de hele pagina gescreenshot moet worden
        """
        if self.page:
            self.page.screenshot(path=filename, full_page=full_page)

    def save_cookies(self, filename: str) -> None:
        """
        Sla cookies op naar een bestand.

        Args:
            filename: Bestandsnaam voor cookies
        """
        if self.context:
            cookies = self.context.cookies()
            with open(filename, 'w') as f:
                json.dump(cookies, f, indent=2)

    def load_cookies(self, filename: str) -> bool:
        """
        Laad cookies van een bestand.

        Args:
            filename: Bestandsnaam met cookies

        Returns:
            True als succesvol geladen
        """
        try:
            with open(filename, 'r') as f:
                cookies = json.load(f)
            return self.login_with_cookies(cookies)
        except Exception as e:
            print(f"Cookie laden fout: {e}")
            return False

    def intercept_requests(self, url_pattern: str, callback: Callable) -> None:
        """
        Intercepteer network requests.

        Args:
            url_pattern: Regex pattern voor URLs om te intercepteren
            callback: Functie die wordt aangeroepen voor elke request
        """
        if self.page:
            self.page.route(url_pattern, callback)


# Voorbeeld gebruik
if __name__ == "__main__":
    # Voorbeeld met context manager
    with AdvancedLoginScraper("https://example.com", headless=False) as scraper:
        # Login via formulier
        selectors = {
            'username': '#username',
            'password': '#password'
        }

        credentials = {
            'username': 'gebruikersnaam',
            'password': 'wachtwoord'
        }

        if scraper.login_form('/login', selectors, credentials, '#submit'):
            print("Succesvol ingelogd!")

            # Scrape een pagina
            content = scraper.scrape_page('/dashboard')
            print(f"Content lengte: {len(content)}")

            # Extracteer data
            titles = scraper.extract_data_js('h1.title')
            print(f"Gevonden titels: {titles}")

            # Screenshot maken
            scraper.take_screenshot('dashboard.png', full_page=True)

            # Cookies opslaan voor latere sessies
            scraper.save_cookies('cookies.json')
        else:
            print("Login mislukt!")
