from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os

# === Configuration Chrome (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(), options=options)

# === Accès à la page produit UniCredit
url = "https://www.investimenti.unicredit.it/it/underlyingpage.html/211234"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# === Extraction du taux
span_val = soup.find("span", class_="price")
taux = span_val.text.strip().replace(",", ".") if span_val else None

# === Extraction de la date affichée sur la page
date_span = soup.find("span", class_="date")
if date_span:
    try:
        raw_date = date_span.get_text(strip=True)
        latest_date = datetime.strptime(raw_date, "%d.%m.%Y").date().isoformat()
    except Exception as e:
        print("❌ Erreur de parsing date :", e)
        latest_date = None
else:
    latest_date = None

# === Enregistrement dans le fichier texte
txt_filename = "hicp_history.txt"

if taux and latest_date:
    new_line = f"{latest_date} ; {taux}"
    print("📌 Dernier HICP publié :", new_line)

    existing_lines = set()
    if os.path.exists(txt_filename):
        with open(txt_filename, "r", encoding="utf-8") as f:
            existing_lines = set(line.strip() for line in f.readlines())

    if new_line in existing_lines:
        print("ℹ️ Taux déjà présent – aucun ajout.")
    else:
        with open(txt_filename, "a", encoding="utf-8") as f:
            f.write(new_line + "\n")
        print("✅ Nouveau taux ajouté au fichier.")
else:
    print("❌ Taux ou date absente – aucune donnée enregistrée.")
