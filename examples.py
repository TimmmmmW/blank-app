"""
Voorbeelden voor het gebruik van de webscrapers.
"""

from scraper_basic import BasicLoginScraper
from scraper_advanced import AdvancedLoginScraper
from bs4 import BeautifulSoup
import json


def voorbeeld_basis_scraper_formulier_login():
    """
    Voorbeeld: Basis scraper met formulier login.
    Geschikt voor eenvoudige websites zonder JavaScript.
    """
    print("=== Voorbeeld 1: Basis Scraper met Formulier Login ===\n")

    # Initialiseer scraper
    scraper = BasicLoginScraper("https://example.com")

    # Login credentials
    credentials = {
        'username': 'mijn_gebruikersnaam',
        'password': 'mijn_wachtwoord'
    }

    # Probeer in te loggen
    if scraper.login_form('/login', credentials):
        print("✓ Succesvol ingelogd!")

        # Scrape een enkele pagina
        soup = scraper.scrape_page('/dashboard')
        if soup:
            print(f"✓ Dashboard gescraped: {len(str(soup))} karakters")

            # Extracteer specifieke data
            titles = scraper.extract_data(soup, 'h2.article-title')
            print(f"✓ Gevonden {len(titles)} artikeltitels:")
            for title in titles[:5]:  # Toon eerste 5
                print(f"  - {title}")

            # Haal links op
            links = scraper.extract_data(soup, 'a.article-link', 'href')
            print(f"✓ Gevonden {len(links)} artikel links")

        # Scrape meerdere pagina's
        pages = ['/category/tech', '/category/news', '/category/sports']
        results = scraper.scrape_multiple_pages(pages, wait_time=1.0)
        print(f"✓ Gescraped {len(results)} categorie pagina's")

        # Cookies opslaan voor latere sessies
        cookies = scraper.get_cookies()
        print(f"✓ Opgeslagen {len(cookies)} cookies")

        # Logout
        scraper.logout()
        print("✓ Uitgelogd")
    else:
        print("✗ Login mislukt!")


def voorbeeld_basis_scraper_api_token():
    """
    Voorbeeld: Basis scraper met API token authenticatie.
    """
    print("\n=== Voorbeeld 2: Basis Scraper met API Token ===\n")

    scraper = BasicLoginScraper("https://api.example.com")

    # Login met API token
    if scraper.login_with_token("your-api-token-here", "Bearer"):
        print("✓ Succesvol ingelogd met API token")

        # Scrape API endpoint
        soup = scraper.scrape_page('/api/v1/data')
        if soup:
            # Voor API responses kun je ook de raw text gebruiken
            # en als JSON parsen
            data_text = soup.get_text()
            print(f"✓ Data opgehaald: {len(data_text)} karakters")

        scraper.logout()
    else:
        print("✗ API token login mislukt!")


def voorbeeld_geavanceerd_scraper_javascript():
    """
    Voorbeeld: Geavanceerde scraper voor JavaScript-heavy sites.
    """
    print("\n=== Voorbeeld 3: Geavanceerde Scraper voor JavaScript Sites ===\n")

    # Gebruik context manager voor automatische cleanup
    with AdvancedLoginScraper("https://modern-app.example.com", headless=True) as scraper:
        # Login met specifieke selectors
        selectors = {
            'username': 'input[name="email"]',
            'password': 'input[type="password"]'
        }

        credentials = {
            'username': 'user@example.com',
            'password': 'secure_password'
        }

        # Custom success check functie
        def check_logged_in(page):
            # Check of user menu zichtbaar is
            return page.is_visible('.user-menu')

        if scraper.login_form(
            '/login',
            selectors,
            credentials,
            'button[type="submit"]',
            success_check=check_logged_in
        ):
            print("✓ Succesvol ingelogd!")

            # Scrape een pagina met wachten op specifieke content
            content = scraper.scrape_page(
                '/dashboard',
                wait_for_selector='.dashboard-loaded'
            )
            print(f"✓ Dashboard gescraped: {len(content)} karakters")

            # Extracteer data met JavaScript
            titles = scraper.extract_data_js('h2.article-title')
            print(f"✓ Gevonden {len(titles)} titels met JavaScript")

            # Scrape pagina met infinite scroll
            content = scraper.scrape_with_scroll('/feed', scroll_count=5)
            print(f"✓ Feed gescraped met scrolling: {len(content)} karakters")

            # Maak een screenshot
            scraper.take_screenshot('dashboard.png', full_page=True)
            print("✓ Screenshot opgeslagen als dashboard.png")

            # Cookies opslaan
            scraper.save_cookies('session_cookies.json')
            print("✓ Cookies opgeslagen")

        else:
            print("✗ Login mislukt!")


def voorbeeld_geavanceerd_scraper_cookies():
    """
    Voorbeeld: Geavanceerde scraper met opgeslagen cookies.
    """
    print("\n=== Voorbeeld 4: Hergebruik Sessie met Cookies ===\n")

    with AdvancedLoginScraper("https://example.com") as scraper:
        # Laad eerder opgeslagen cookies
        if scraper.load_cookies('session_cookies.json'):
            print("✓ Ingelogd met opgeslagen cookies")

            # Scrape direct zonder opnieuw in te loggen
            content = scraper.scrape_page('/profile')
            print(f"✓ Profiel gescraped: {len(content)} karakters")
        else:
            print("✗ Cookies laden mislukt")


def voorbeeld_interactieve_scraping():
    """
    Voorbeeld: Klikken en scrapen voor interactieve content.
    """
    print("\n=== Voorbeeld 5: Interactieve Scraping ===\n")

    with AdvancedLoginScraper("https://example.com") as scraper:
        scraper.start()

        # Ga naar pagina
        scraper.page.goto("https://example.com/products")
        scraper.page.wait_for_load_state('networkidle')

        # Klik op "Toon meer" button meerdere keren
        for i in range(3):
            content = scraper.click_and_scrape(
                'button.load-more',
                wait_selector='.product-item',
                wait_time=1.0
            )
            print(f"✓ Ronde {i+1}: {len(content)} karakters")

        # Extracteer alle product namen
        products = scraper.extract_data_js('.product-name')
        print(f"✓ Gevonden {len(products)} producten:")
        for product in products[:10]:  # Toon eerste 10
            print(f"  - {product}")


def voorbeeld_handmatige_login():
    """
    Voorbeeld: Handmatige login voor complexe flows (2FA, OAuth, etc.)
    """
    print("\n=== Voorbeeld 6: Handmatige Login (voor 2FA/OAuth) ===\n")

    # Start in non-headless mode
    with AdvancedLoginScraper("https://secure-site.example.com", headless=False) as scraper:
        print("Browser wordt geopend...")
        print("Log handmatig in (je hebt 5 minuten)...")

        # Wacht tot gebruiker handmatig inlogt
        if scraper.wait_for_login_manual('/login', timeout=300000):
            print("✓ Handmatige login gedetecteerd!")

            # Nu kunnen we verder scrapen
            content = scraper.scrape_page('/dashboard')
            print(f"✓ Dashboard gescraped: {len(content)} karakters")

            # Sla cookies op voor volgende keer
            scraper.save_cookies('manual_session.json')
            print("✓ Sessie opgeslagen!")
        else:
            print("✗ Timeout tijdens wachten op login")


def voorbeeld_data_extractie_en_opslaan():
    """
    Voorbeeld: Complete workflow van login tot data opslaan.
    """
    print("\n=== Voorbeeld 7: Complete Data Extractie Workflow ===\n")

    scraper = BasicLoginScraper("https://example.com")

    credentials = {'username': 'user', 'password': 'pass'}

    if scraper.login_form('/login', credentials):
        print("✓ Ingelogd")

        # Scrape lijst met artikelen
        soup = scraper.scrape_page('/articles')

        # Extracteer gestructureerde data
        data = []
        articles = soup.select('article.post')

        for article in articles:
            item = {
                'title': article.select_one('h2.title').get_text(strip=True),
                'author': article.select_one('.author').get_text(strip=True),
                'date': article.select_one('.date').get_text(strip=True),
                'url': article.select_one('a.read-more')['href']
            }
            data.append(item)

        print(f"✓ Geëxtraheerd: {len(data)} artikelen")

        # Sla op als JSON
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("✓ Data opgeslagen als articles.json")

        # Sla ook op als CSV
        import csv
        with open('articles.csv', 'w', newline='', encoding='utf-8') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        print("✓ Data opgeslagen als articles.csv")

        scraper.logout()


def voorbeeld_error_handling():
    """
    Voorbeeld: Goede error handling bij scraping.
    """
    print("\n=== Voorbeeld 8: Error Handling ===\n")

    scraper = BasicLoginScraper("https://example.com")

    try:
        # Probeer in te loggen
        credentials = {'username': 'user', 'password': 'pass'}

        if not scraper.login_form('/login', credentials):
            raise Exception("Login mislukt")

        print("✓ Ingelogd")

        # Scrape meerdere pagina's met error handling
        urls = ['/page1', '/page2', '/page3', '/non-existent']

        for url in urls:
            try:
                soup = scraper.scrape_page(url, wait_time=0.5)
                if soup:
                    print(f"✓ {url} gescraped")
                else:
                    print(f"⚠ {url} retourneerde geen content")
            except Exception as e:
                print(f"✗ {url} fout: {e}")
                continue  # Ga door met volgende pagina

        print("✓ Scraping voltooid (met enkele fouten)")

    except Exception as e:
        print(f"✗ Kritieke fout: {e}")

    finally:
        # Altijd netjes afsluiten
        scraper.logout()
        print("✓ Sessie afgesloten")


if __name__ == "__main__":
    print("WEB SCRAPER VOORBEELDEN")
    print("=" * 50)
    print()
    print("Let op: Dit zijn voorbeelden met dummy URLs.")
    print("Pas deze aan voor je eigen gebruik!")
    print()

    # Voer voorbeelden uit
    # Uncomment de voorbeelden die je wilt uitvoeren:

    # voorbeeld_basis_scraper_formulier_login()
    # voorbeeld_basis_scraper_api_token()
    # voorbeeld_geavanceerd_scraper_javascript()
    # voorbeeld_geavanceerd_scraper_cookies()
    # voorbeeld_interactieve_scraping()
    # voorbeeld_handmatige_login()
    # voorbeeld_data_extractie_en_opslaan()
    # voorbeeld_error_handling()

    print("\n✓ Voorbeelden gereed!")
    print("Uncomment de voorbeelden die je wilt uitvoeren.")
