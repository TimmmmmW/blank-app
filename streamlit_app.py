import streamlit as st
import json
from scraper_basic import BasicLoginScraper
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Try to import advanced scraper, but continue if Playwright is not available
try:
    from scraper_advanced import AdvancedLoginScraper
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    st.warning("⚠️ Playwright niet beschikbaar. Alleen Basis Scraper is actief. Voor volledige functionaliteit, installeer Playwright lokaal.")

st.set_page_config(
    page_title="Web Scraper met Login",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Web Scraper voor Pagina's met Login")
st.markdown("Een krachtige webscraper die kan inloggen en data kan extracten van beveiligde websites.")

# Sidebar voor configuratie
st.sidebar.header("⚙️ Configuratie")

# Scraper type selectie
if PLAYWRIGHT_AVAILABLE:
    scraper_options = ["Basis (requests)", "Geavanceerd (Playwright)"]
else:
    scraper_options = ["Basis (requests)"]

scraper_type = st.sidebar.selectbox(
    "Type Scraper",
    scraper_options,
    help="Basis is sneller, Geavanceerd kan JavaScript aan"
)

st.sidebar.markdown("---")

# Basis URL
base_url = st.sidebar.text_input(
    "Basis URL",
    value="https://example.com",
    help="De basis URL van de website (bijv. https://example.com)"
)

# Login configuratie
st.sidebar.subheader("🔐 Login Instellingen")

# Login methodes afhankelijk van scraper type
if scraper_type == "Geavanceerd (Playwright)" and PLAYWRIGHT_AVAILABLE:
    login_options = ["Formulier", "Basic Auth", "API Token", "Cookies", "Handmatig (alleen Geavanceerd)"]
else:
    login_options = ["Formulier", "Basic Auth", "API Token"]

login_method = st.sidebar.selectbox(
    "Login Methode",
    login_options
)

# Tabs voor verschillende functionaliteiten
tab1, tab2, tab3, tab4 = st.tabs(["Login", "Scrapen", "Data Extractie", "Resultaten"])

# Tab 1: Login
with tab1:
    st.header("Inloggen")

    if login_method == "Formulier":
        col1, col2 = st.columns(2)

        with col1:
            login_url = st.text_input("Login URL", value="/login", key="login_url")
            username = st.text_input("Gebruikersnaam", key="username")
            password = st.text_input("Wachtwoord", type="password", key="password")

        with col2:
            if scraper_type == "Geavanceerd (Playwright)":
                username_selector = st.text_input("Username Selector", value="#username", key="user_sel")
                password_selector = st.text_input("Password Selector", value="#password", key="pass_sel")
                submit_selector = st.text_input("Submit Selector", value="button[type='submit']", key="submit_sel")
            else:
                username_field = st.text_input("Username Field Name", value="username", key="user_field")
                password_field = st.text_input("Password Field Name", value="password", key="pass_field")

    elif login_method == "Basic Auth":
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Gebruikersnaam", key="basic_username")
        with col2:
            password = st.text_input("Wachtwoord", type="password", key="basic_password")

    elif login_method == "API Token":
        col1, col2 = st.columns(2)
        with col1:
            api_token = st.text_input("API Token", type="password", key="api_token")
        with col2:
            token_type = st.selectbox("Token Type", ["Bearer", "Token", "API-Key"], key="token_type")

    elif login_method == "Cookies":
        cookies_json = st.text_area(
            "Cookies (JSON formaat)",
            height=150,
            placeholder='[{"name": "session", "value": "abc123", "domain": "example.com", "path": "/"}]',
            key="cookies_json"
        )

    # Login button
    if st.button("🔓 Inloggen", type="primary", use_container_width=True):
        with st.spinner("Inloggen..."):
            try:
                if scraper_type == "Basis (requests)":
                    scraper = BasicLoginScraper(base_url)

                    if login_method == "Formulier":
                        credentials = {
                            st.session_state.user_field: st.session_state.username,
                            st.session_state.pass_field: st.session_state.password
                        }
                        success = scraper.login_form(st.session_state.login_url, credentials)

                    elif login_method == "Basic Auth":
                        success = scraper.login_basic_auth(
                            st.session_state.basic_username,
                            st.session_state.basic_password
                        )

                    elif login_method == "API Token":
                        success = scraper.login_with_token(
                            st.session_state.api_token,
                            st.session_state.token_type
                        )

                    if success:
                        st.session_state.scraper = scraper
                        st.session_state.logged_in = True
                        st.success("✅ Succesvol ingelogd!")
                    else:
                        st.error("❌ Login mislukt. Controleer je gegevens.")

                else:  # Geavanceerd
                    scraper = AdvancedLoginScraper(
                        base_url,
                        headless=st.sidebar.checkbox("Headless mode", value=True)
                    )
                    scraper.start()

                    if login_method == "Formulier":
                        selectors = {
                            'username': st.session_state.user_sel,
                            'password': st.session_state.pass_sel
                        }
                        credentials = {
                            'username': st.session_state.username,
                            'password': st.session_state.password
                        }
                        success = scraper.login_form(
                            st.session_state.login_url,
                            selectors,
                            credentials,
                            st.session_state.submit_sel
                        )

                    elif login_method == "Cookies":
                        cookies = json.loads(st.session_state.cookies_json)
                        success = scraper.login_with_cookies(cookies)

                    elif login_method == "Handmatig (alleen Geavanceerd)":
                        success = scraper.wait_for_login_manual(st.session_state.login_url)

                    if success:
                        st.session_state.scraper = scraper
                        st.session_state.logged_in = True
                        st.success("✅ Succesvol ingelogd!")
                    else:
                        st.error("❌ Login mislukt. Controleer je gegevens.")

            except Exception as e:
                st.error(f"❌ Fout tijdens inloggen: {str(e)}")

# Tab 2: Scrapen
with tab2:
    st.header("Pagina's Scrapen")

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Log eerst in via de Login tab!")
    else:
        scrape_mode = st.radio(
            "Scrape Modus",
            ["Enkele pagina", "Meerdere pagina's"],
            horizontal=True
        )

        if scrape_mode == "Enkele pagina":
            url_to_scrape = st.text_input("URL om te scrapen", value="/dashboard")

            if scraper_type == "Geavanceerd (Playwright)":
                wait_selector = st.text_input(
                    "Wacht op selector (optioneel)",
                    placeholder="#content",
                    help="CSS selector om op te wachten voordat scrapen"
                )

            if st.button("🔍 Scrape deze pagina", use_container_width=True):
                with st.spinner("Scrapen..."):
                    try:
                        scraper = st.session_state.scraper

                        if scraper_type == "Basis (requests)":
                            soup = scraper.scrape_page(url_to_scrape)
                            if soup:
                                st.session_state.current_content = str(soup)
                                st.success(f"✅ Pagina gescraped! ({len(str(soup))} karakters)")
                        else:
                            content = scraper.scrape_page(
                                url_to_scrape,
                                wait_for_selector=wait_selector if wait_selector else None
                            )
                            if content:
                                st.session_state.current_content = content
                                st.success(f"✅ Pagina gescraped! ({len(content)} karakters)")

                    except Exception as e:
                        st.error(f"❌ Fout tijdens scrapen: {str(e)}")

        else:  # Meerdere pagina's
            urls_text = st.text_area(
                "URLs om te scrapen (één per regel)",
                value="/page1\n/page2\n/page3",
                height=150
            )

            wait_time = st.slider(
                "Wachttijd tussen requests (seconden)",
                0.0, 5.0, 1.0, 0.5
            )

            if st.button("🔍 Scrape alle pagina's", use_container_width=True):
                urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

                with st.spinner(f"Scrapen van {len(urls)} pagina's..."):
                    try:
                        scraper = st.session_state.scraper
                        results = {}

                        if scraper_type == "Basis (requests)":
                            results = scraper.scrape_multiple_pages(urls, wait_time)
                            st.session_state.multiple_results = {
                                url: str(soup) for url, soup in results.items()
                            }
                        else:
                            for url in urls:
                                content = scraper.scrape_page(url, wait_time)
                                if content:
                                    results[url] = content

                            st.session_state.multiple_results = results

                        st.success(f"✅ {len(results)} pagina's gescraped!")

                    except Exception as e:
                        st.error(f"❌ Fout tijdens scrapen: {str(e)}")

# Tab 3: Data Extractie
with tab3:
    st.header("Data Extractie")

    if 'current_content' not in st.session_state and 'multiple_results' not in st.session_state:
        st.warning("⚠️ Scrape eerst een pagina via de Scrapen tab!")
    else:
        css_selector = st.text_input(
            "CSS Selector",
            value="h1, h2, h3",
            help="CSS selector voor de elementen die je wilt extracten"
        )

        attribute = st.text_input(
            "Attribuut (optioneel)",
            placeholder="href, src, alt, etc.",
            help="Laat leeg voor tekst content"
        )

        if st.button("📊 Extracteer Data", use_container_width=True):
            with st.spinner("Data extracten..."):
                try:
                    extracted_data = []

                    if 'current_content' in st.session_state:
                        # Enkele pagina
                        soup = BeautifulSoup(st.session_state.current_content, 'lxml')
                        elements = soup.select(css_selector)

                        if attribute:
                            extracted_data = [
                                elem.get(attribute, '') for elem in elements
                                if elem.get(attribute)
                            ]
                        else:
                            extracted_data = [elem.get_text(strip=True) for elem in elements]

                    elif 'multiple_results' in st.session_state:
                        # Meerdere pagina's
                        for url, content in st.session_state.multiple_results.items():
                            soup = BeautifulSoup(content, 'lxml')
                            elements = soup.select(css_selector)

                            if attribute:
                                data = [
                                    elem.get(attribute, '') for elem in elements
                                    if elem.get(attribute)
                                ]
                            else:
                                data = [elem.get_text(strip=True) for elem in elements]

                            for item in data:
                                extracted_data.append({'URL': url, 'Data': item})

                    st.session_state.extracted_data = extracted_data

                    if extracted_data:
                        st.success(f"✅ {len(extracted_data)} items geëxtraheerd!")
                    else:
                        st.warning("⚠️ Geen data gevonden met deze selector.")

                except Exception as e:
                    st.error(f"❌ Fout tijdens extractie: {str(e)}")

# Tab 4: Resultaten
with tab4:
    st.header("Resultaten")

    if 'extracted_data' in st.session_state:
        data = st.session_state.extracted_data

        if data:
            # Toon data als DataFrame als het dictionaries zijn
            if isinstance(data[0], dict):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame({'Data': data})

            st.dataframe(df, use_container_width=True)

            # Download opties
            col1, col2 = st.columns(2)

            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download als CSV",
                    csv,
                    "scraped_data.csv",
                    "text/csv",
                    use_container_width=True
                )

            with col2:
                json_str = df.to_json(orient='records', indent=2, force_ascii=False)
                st.download_button(
                    "📥 Download als JSON",
                    json_str,
                    "scraped_data.json",
                    "application/json",
                    use_container_width=True
                )

            # Statistieken
            st.subheader("📈 Statistieken")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Totaal items", len(df))

            with col2:
                if 'URL' in df.columns:
                    st.metric("Unieke URLs", df['URL'].nunique())

            with col3:
                st.metric("Kolommen", len(df.columns))

        else:
            st.info("Nog geen data geëxtraheerd.")

    else:
        st.info("Nog geen resultaten. Extracteer eerst data via de Data Extractie tab.")

# Cleanup button in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Sessie", use_container_width=True):
    if 'scraper' in st.session_state:
        try:
            scraper = st.session_state.scraper
            if hasattr(scraper, 'logout'):
                scraper.logout()
            elif hasattr(scraper, 'close'):
                scraper.close()
        except:
            pass

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Hulp")
st.sidebar.markdown("""
**Basis Scraper:**
- Sneller
- Minder resource-intensief
- Goed voor statische sites

**Geavanceerd Scraper:**
- Kan JavaScript aan
- Infinite scroll support
- Screenshots
- Langzamer maar krachtiger
""")
