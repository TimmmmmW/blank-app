# 🔍 Web Scraper met Login Functionaliteit

Een krachtige webscraper die kan inloggen op websites en data kan extracten van beveiligde pagina's. Ondersteunt zowel eenvoudige statische websites als complexe JavaScript-heavy applicaties.

## ✨ Features

- **Twee scraper types:**
  - **Basis Scraper** (requests + BeautifulSoup): Snel en lichtgewicht voor statische websites
  - **Geavanceerde Scraper** (Playwright): Voor JavaScript-heavy sites met dynamische content

- **Meerdere login methodes:**
  - HTML formulier login
  - HTTP Basic Authentication
  - API Token authenticatie
  - Cookie-based authenticatie
  - Handmatige login (voor 2FA/OAuth)

- **Krachtige data extractie:**
  - CSS selectors
  - Attribuut extractie (links, afbeeldingen, etc.)
  - JavaScript-based extractie
  - Infinite scroll support

- **Gebruiksvriendelijke Streamlit UI:**
  - Interactieve webinterface
  - Real-time scraping
  - Data export (CSV, JSON)
  - Statistieken en visualisatie

## 🚀 Installatie

1. **Clone de repository**
   ```bash
   git clone <repository-url>
   cd blank-app
   ```

2. **Installeer dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Installeer Playwright browsers** (alleen voor geavanceerde scraper)
   ```bash
   playwright install chromium
   ```

4. **Configureer credentials** (optioneel)
   ```bash
   cp .env.example .env
   # Edit .env met je eigen credentials
   ```

## 📖 Gebruik

### Via Streamlit UI (Aanbevolen voor beginners)

Start de Streamlit app:
```bash
streamlit run streamlit_app.py
```

De app opent in je browser. Volg deze stappen:

1. **Configuratie** (Sidebar):
   - Kies scraper type (Basis of Geavanceerd)
   - Voer basis URL in
   - Selecteer login methode

2. **Login Tab**:
   - Vul login credentials in
   - Klik op "Inloggen"

3. **Scrapen Tab**:
   - Kies enkele of meerdere pagina's
   - Voer URL(s) in
   - Klik op "Scrape"

4. **Data Extractie Tab**:
   - Voer CSS selector in
   - Optioneel: specificeer attribuut
   - Klik op "Extracteer Data"

5. **Resultaten Tab**:
   - Bekijk geëxtraheerde data
   - Download als CSV of JSON
   - Bekijk statistieken

### Via Python Code

#### Basis Scraper Voorbeeld

```python
from scraper_basic import BasicLoginScraper

# Initialiseer scraper
scraper = BasicLoginScraper("https://example.com")

# Login
credentials = {
    'username': 'gebruikersnaam',
    'password': 'wachtwoord'
}

if scraper.login_form('/login', credentials):
    print("Ingelogd!")

    # Scrape een pagina
    soup = scraper.scrape_page('/dashboard')

    # Extracteer data
    titles = scraper.extract_data(soup, 'h2.title')
    print(f"Gevonden titels: {titles}")

    # Logout
    scraper.logout()
```

#### Geavanceerde Scraper Voorbeeld

```python
from scraper_advanced import AdvancedLoginScraper

# Gebruik context manager voor automatische cleanup
with AdvancedLoginScraper("https://example.com", headless=True) as scraper:
    # Login met selectors
    selectors = {
        'username': '#email',
        'password': '#password'
    }

    credentials = {
        'username': 'user@example.com',
        'password': 'wachtwoord'
    }

    if scraper.login_form('/login', selectors, credentials, '#submit-btn'):
        print("Ingelogd!")

        # Scrape met wachten op specifieke content
        content = scraper.scrape_page(
            '/dashboard',
            wait_for_selector='.dashboard-loaded'
        )

        # Extracteer data met JavaScript
        titles = scraper.extract_data_js('h2.title')

        # Screenshot maken
        scraper.take_screenshot('screenshot.png', full_page=True)

        # Cookies opslaan
        scraper.save_cookies('session.json')
```

## 📚 Voorbeelden

Bekijk `examples.py` voor uitgebreide voorbeelden:

```bash
python examples.py
```

Voorbeelden omvatten:
- Formulier login
- API token authenticatie
- JavaScript scraping
- Cookie hergebruik
- Interactieve scraping (klikken, scrollen)
- Handmatige login (2FA/OAuth)
- Data extractie en opslaan
- Error handling

## 🔧 API Referentie

### BasicLoginScraper

**Initialisatie:**
```python
scraper = BasicLoginScraper(base_url, headers=None)
```

**Belangrijkste methodes:**
- `login_form(login_url, credentials, form_data=None)` - Login via HTML formulier
- `login_basic_auth(username, password)` - HTTP Basic Auth
- `login_with_token(token, token_type="Bearer")` - API Token auth
- `scrape_page(url, wait_time=0)` - Scrape enkele pagina
- `scrape_multiple_pages(urls, wait_time=1.0)` - Scrape meerdere pagina's
- `extract_data(soup, selector, attribute=None)` - Extracteer data
- `get_cookies()` - Haal cookies op
- `set_cookies(cookies)` - Stel cookies in
- `logout()` - Logout en reset sessie

### AdvancedLoginScraper

**Initialisatie:**
```python
scraper = AdvancedLoginScraper(base_url, headless=True, browser_type="chromium")
```

**Belangrijkste methodes:**
- `start()` - Start browser
- `close()` - Sluit browser
- `login_form(login_url, selectors, credentials, submit_selector, success_check=None)` - Login via formulier
- `login_with_cookies(cookies)` - Login met cookies
- `wait_for_login_manual(login_url, timeout=300000)` - Handmatige login
- `scrape_page(url, wait_time=0, wait_for_selector=None)` - Scrape pagina
- `scrape_with_scroll(url, scroll_count=5, scroll_delay=1.0)` - Scrape met scrolling
- `extract_data_js(selector, attribute=None)` - JavaScript data extractie
- `click_and_scrape(click_selector, wait_selector=None, wait_time=1.0)` - Klik en scrape
- `take_screenshot(filename, full_page=False)` - Screenshot maken
- `save_cookies(filename)` - Cookies opslaan
- `load_cookies(filename)` - Cookies laden

## 🛡️ Best Practices

1. **Respecteer robots.txt**: Controleer altijd de robots.txt van de website
2. **Rate limiting**: Gebruik wachttijden tussen requests (min. 1 seconde)
3. **User-Agent**: De scrapers gebruiken realistische User-Agent headers
4. **Error handling**: Implementeer goede error handling voor robuustheid
5. **Cookies opslaan**: Sla sessies op om herhaalde logins te vermijden
6. **Verantwoord gebruik**: Gebruik scrapers alleen voor legale doeleinden

## ⚠️ Legal & Ethisch Gebruik

- Gebruik deze scraper alleen voor websites waar je toestemming voor hebt
- Respecteer de Terms of Service van websites
- Implementeer rate limiting om servers niet te overbelasten
- Gebruik scrapers niet voor het verzamelen van persoonlijke data zonder toestemming

## 🤝 Contributing

Bijdragen zijn welkom! Open een issue of pull request.

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License - zie het LICENSE bestand voor details.

## 🆘 Hulp nodig?

- Bekijk de `examples.py` voor voorbeeldcode
- Gebruik de Streamlit UI voor een visuele interface
- Check de API documentatie hierboven
- Voor complexe scraping scenarios, overweeg de geavanceerde scraper

## 🔄 Updates

- **v1.0.0** - Initiële release met basis en geavanceerde scrapers
  - Formulier, Basic Auth, en Token authenticatie
  - Streamlit UI
  - Data export functionaliteit
  - Cookie management
  - Screenshot support
