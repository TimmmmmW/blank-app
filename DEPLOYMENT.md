# 📱 Deployment Guide - iPhone Toegang

## Streamlit Cloud Deployment (Aanbevolen)

### Stap 1: Bereid je repository voor

De code is al klaar! Alles staat in je GitHub repository.

### Stap 2: Deploy naar Streamlit Cloud

1. Ga naar [share.streamlit.io](https://share.streamlit.io)
2. Log in met je GitHub account
3. Klik op "New app"
4. Selecteer:
   - Repository: `TimmmmmW/blank-app`
   - Branch: `claude/create-login-webscraper-011CUKkQjazdntbJsDsTpQaT`
   - Main file path: `streamlit_app.py`
5. Klik op "Deploy"

### Stap 3: Wacht op deployment

Streamlit Cloud zal:
- Je requirements installeren
- De app starten
- Een URL genereren (bijv. `https://your-app.streamlit.app`)

**LET OP:** De Playwright browser werkt NIET op Streamlit Cloud vanwege beperkingen. Gebruik alleen de **Basis Scraper** op Streamlit Cloud.

### Stap 4: Gebruik op iPhone

1. Open Safari of Chrome op je iPhone
2. Ga naar je app URL
3. Je kunt de app nu gebruiken alsof het een normale website is!

**Tip:** Voeg toe aan Home Screen:
- Tap het "Share" icoon in Safari
- Scroll en tap "Add to Home Screen"
- Nu heb je een app icoon!

---

## 🐳 Optie 2: Docker Deployment (Voor geavanceerde functies)

Als je de **Geavanceerde Scraper** (Playwright) wilt gebruiken, moet je naar een platform dat Docker ondersteunt.

### Maak een Dockerfile:

```dockerfile
FROM python:3.11-slim

# Install dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
```

### Deploy naar:

**Railway.app:**
1. Ga naar [railway.app](https://railway.app)
2. Connect je GitHub repository
3. Railway detecteert automatisch het Dockerfile
4. Deploy! Je krijgt een URL

**Render.com:**
1. Ga naar [render.com](https://render.com)
2. "New" → "Web Service"
3. Connect GitHub repository
4. Kies "Docker" als environment
5. Deploy! Je krijgt een URL

**Fly.io:**
```bash
# Installeer flyctl
brew install flyctl  # Op Mac
# Of download van fly.io

# Login
flyctl auth login

# Deploy
flyctl launch
flyctl deploy
```

---

## ⚡ Optie 3: Replit (Snelste test)

Voor een snelle test:

1. Ga naar [replit.com](https://replit.com)
2. Import van GitHub
3. Voer uit
4. Deel de URL
5. Open op iPhone

---

## 📋 Beperkingen per Platform

| Platform | Basis Scraper | Geavanceerde Scraper | Gratis Tier |
|----------|--------------|---------------------|-------------|
| Streamlit Cloud | ✅ | ❌ | ✅ |
| Railway | ✅ | ✅ | ⚠️ Beperkt |
| Render | ✅ | ✅ | ⚠️ Beperkt |
| Fly.io | ✅ | ✅ | ⚠️ Beperkt |
| Replit | ✅ | ❌ | ✅ |

---

## 🎯 Aanbeveling voor iPhone gebruik

**Voor eenvoudige scraping:**
→ Gebruik **Streamlit Cloud** (gratis, makkelijk, werkt direct)

**Voor geavanceerde scraping (JavaScript sites):**
→ Gebruik **Railway** of **Render** met Docker

---

## 💡 Alternatief: Python op iPhone

Je kunt ook Python DIRECT op iPhone runnen:

**Pythonista App** (€10,99):
1. Download Pythonista van App Store
2. Installeer pip packages (beperkt)
3. Run Python scripts

**a-Shell App** (Gratis):
1. Download a-Shell van App Store
2. Heeft Python ondersteuning
3. Beperkte functionaliteit

**MAAR:** Deze apps zijn beperkt en Streamlit werkt er niet op. Cloud deployment is beter!

---

## 🔒 Veiligheid

**LET OP:** Zet NOOIT je login credentials in de code of GitHub!

Voor cloud deployment:
1. Ga naar je Streamlit Cloud app settings
2. Ga naar "Secrets"
3. Voeg toe:
```toml
[credentials]
username = "jouw_username"
password = "jouw_password"
```

4. Gebruik in code:
```python
import streamlit as st

username = st.secrets["credentials"]["username"]
password = st.secrets["credentials"]["password"]
```

---

## 🚀 Quick Start voor Streamlit Cloud

1. Push je code naar GitHub ✅ (Done!)
2. Ga naar share.streamlit.io
3. Klik "New app"
4. Selecteer je repository
5. Deploy!
6. Open URL op iPhone
7. Klaar! 🎉
