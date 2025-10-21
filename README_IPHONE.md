# 📱 Web Scraper op iPhone - Quick Start

## 🎯 Snelste Manier (5 minuten)

### Stap 1: Deploy naar Streamlit Cloud

1. **Open je browser** op computer of iPhone
2. Ga naar: **[share.streamlit.io](https://share.streamlit.io)**
3. **Log in** met GitHub
4. Klik op **"New app"**
5. Vul in:
   ```
   Repository: TimmmmmW/blank-app
   Branch: claude/create-login-webscraper-011CUKkQjazdntbJsDsTpQaT
   Main file: streamlit_app.py
   ```
6. Klik **"Deploy"**
7. Wacht 2-3 minuten ⏳

### Stap 2: Open op iPhone

1. Je krijgt een URL zoals: `https://jouw-app.streamlit.app`
2. Open deze URL in **Safari** op je iPhone
3. **Klaar!** De app werkt nu als een website

### Stap 3: Voeg toe als App Icoon (Optioneel)

1. In Safari, tap het **Share** icoon (📤)
2. Scroll naar beneden
3. Tap **"Add to Home Screen"**
4. Geef een naam: "Web Scraper"
5. Tap **"Add"**
6. Nu heb je een app icoon op je home screen! 🎉

---

## ⚠️ Belangrijke Notitie

Op **Streamlit Cloud** werkt alleen de **Basis Scraper**.

Dit betekent:
- ✅ Formulier login
- ✅ Basic Auth
- ✅ API Tokens
- ✅ Data extractie
- ✅ CSV/JSON export
- ❌ **Geen** Geavanceerde Scraper (Playwright)
- ❌ **Geen** JavaScript scraping
- ❌ **Geen** Screenshots

**Voor Geavanceerde functies:** Zie DEPLOYMENT.md voor Docker deployment opties.

---

## 🎨 Hoe te Gebruiken op iPhone

### In de Streamlit App:

1. **Login Tab**:
   - Selecteer "Basis (requests)" in sidebar
   - Vul basis URL in (bijv. `https://example.com`)
   - Kies login methode
   - Vul credentials in
   - Tap "Inloggen"

2. **Scrapen Tab**:
   - Kies "Enkele pagina" of "Meerdere pagina's"
   - Vul URL(s) in
   - Tap "Scrape"

3. **Data Extractie Tab**:
   - Vul CSS selector in (bijv. `h1, h2, h3`)
   - Optioneel: voer attribuut in (bijv. `href`)
   - Tap "Extracteer Data"

4. **Resultaten Tab**:
   - Bekijk je data
   - Tap "Download als CSV" of "Download als JSON"
   - Data wordt gedownload naar je iPhone

---

## 🔒 Veiligheid

**NOOIT credentials in GitHub zetten!**

Voor veilig gebruik op Streamlit Cloud:

1. Ga naar je app op share.streamlit.io
2. Klik op **"Settings"** (⚙️)
3. Ga naar **"Secrets"**
4. Voeg toe:
   ```toml
   [credentials]
   username = "jouw_gebruikersnaam"
   password = "jouw_wachtwoord"
   ```
5. Save

Dan in de app kun je deze gebruiken zonder ze hard-coded te hebben.

---

## 💡 Tips voor iPhone Gebruik

### Safari Tips:
- **Zoom in/uit**: Pinch gesture
- **Auto-fill**: Gebruik iCloud Keychain voor wachtwoorden
- **Reader Mode**: Niet beschikbaar voor Streamlit apps

### Data Management:
- Downloads gaan naar **Files** app → **Downloads** folder
- Je kunt direct openen in Numbers (CSV) of andere apps
- Deel via AirDrop naar je Mac

### Best Practices:
- **WiFi**: Gebruik WiFi voor grote scraping jobs
- **Keep awake**: Houd iPhone actief tijdens scraping
- **Notifications**: Safari blijft actief in background tot ~5 min
- **Save vaak**: Download resultaten regelmatig

---

## 🐛 Troubleshooting

### "App is sleeping"
- Streamlit Cloud apps slapen na inactiviteit
- Tap gewoon op de app, wacht 30 sec, reload

### "Module not found"
- Check of requirements.txt compleet is
- Redeploy de app via share.streamlit.io

### "Login fails"
- Test eerst de website in Safari
- Sommige sites blokkeren automated requests
- Probeer andere login methode

### "Data niet geladen"
- Check internet connectie
- Sommige sites hebben bot detectie
- Probeer vanaf desktop browser eerst

---

## 🚀 Volgende Stappen

**Voor meer controle:**
1. Deploy naar Railway/Render met Docker (zie DEPLOYMENT.md)
2. Krijg toegang tot Geavanceerde Scraper
3. JavaScript scraping
4. Screenshot functionaliteit

**Voor development:**
1. Clone repository op Mac
2. Run lokaal met `streamlit run streamlit_app.py`
3. Test op localhost
4. Deploy updates naar cloud

---

## 📞 Support

Voor vragen, check:
- **README.md** - Volledige documentatie
- **DEPLOYMENT.md** - Deployment opties
- **examples.py** - Code voorbeelden

---

## ✅ Checklist

- [ ] GitHub account aangemaakt
- [ ] Repository geforked/gecloned
- [ ] Streamlit Cloud account aangemaakt
- [ ] App gedeployed
- [ ] URL werkt op iPhone
- [ ] App icoon toegevoegd aan home screen
- [ ] Eerste scraping test gedaan
- [ ] Data succesvol gedownload

**Veel succes!** 🎉
