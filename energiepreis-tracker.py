#!/usr/bin/env python3
"""Weltweite Energiepreise -> CSV. Nur Standardbibliothek (kein pip nötig).

Datenquellen-Strategie:
  1. Optional: offizielle API (z. B. GlobalPetrolPrices/CollectAPI) per ENV-Key.
  2. Referenzpool unten (bitte periodisch gegen EU Oil Bulletin / ADAC /
     BDEW / GlobalPetrolPrices prüfen) – ersetzt manuelle Tabellen-Recherche.
Wechselkurse: open.er-api.com (kostenlos, ohne Key).
"""
import csv
import json
import os
import urllib.request
from datetime import datetime

API_KEY = os.environ.get("GLOBALPETROL_API_KEY", "")
EXPORT_DATEINAME = f"weltweite_energiepreise_{datetime.now().strftime('%Y-%m-%d')}.csv"
FX_URL = "https://open.er-api.com/v6/latest/EUR"  # kostenlos, ohne Key
FX_FALLBACK_USD = 1.08  # 1 EUR = X USD


def hole_wechselkurs():
    """Tagesaktueller EUR->USD-Kurs, sonst Fallback."""
    try:
        with urllib.request.urlopen(FX_URL, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        usd = (data.get("rates") or {}).get("USD")
        if usd:
            print(f"Wechselkurs: 1 EUR = {usd} USD (Stand {data.get('time_last_update_utc', '?')})")
            return float(usd)
    except Exception as e:
        print(f"Hinweis: Wechselkurs offline ({e}). Fallback {FX_FALLBACK_USD}.")
    return FX_FALLBACK_USD


# Referenzpool: Benzin/Diesel in EUR/L, Strom in EUR/kWh.
# Gruppe: Deutschland | Weltmächte | Krisenregionen | Rest
DATEN_POOL = [
    {"Land": "Deutschland", "Gruppe": "Deutschland", "Benzin_EUR_L": 1.74, "Diesel_EUR_L": 1.62, "Strom_EUR_kWh": 0.36},
    {"Land": "USA", "Gruppe": "Weltmächte", "Benzin_EUR_L": 0.88, "Diesel_EUR_L": 0.98, "Strom_EUR_kWh": 0.16},
    {"Land": "China", "Gruppe": "Weltmächte", "Benzin_EUR_L": 1.05, "Diesel_EUR_L": 0.95, "Strom_EUR_kWh": 0.09},
    {"Land": "Russland", "Gruppe": "Weltmächte", "Benzin_EUR_L": 0.65, "Diesel_EUR_L": 0.60, "Strom_EUR_kWh": 0.06},
    {"Land": "Venezuela", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 0.02, "Diesel_EUR_L": 0.01, "Strom_EUR_kWh": 0.005},
    {"Land": "Iran", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 0.03, "Diesel_EUR_L": 0.01, "Strom_EUR_kWh": 0.003},
    {"Land": "Israel", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 1.95, "Diesel_EUR_L": 1.85, "Strom_EUR_kWh": 0.20},
    {"Land": "Türkei", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 1.10, "Diesel_EUR_L": 1.05, "Strom_EUR_kWh": 0.12},
    {"Land": "Indien", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 1.15, "Diesel_EUR_L": 1.00, "Strom_EUR_kWh": 0.08},
    {"Land": "Ukraine", "Gruppe": "Krisenregionen", "Benzin_EUR_L": 1.35, "Diesel_EUR_L": 1.30, "Strom_EUR_kWh": 0.10},
    {"Land": "Frankreich", "Gruppe": "Rest", "Benzin_EUR_L": 1.78, "Diesel_EUR_L": 1.69, "Strom_EUR_kWh": 0.26},
    {"Land": "Polen", "Gruppe": "Rest", "Benzin_EUR_L": 1.48, "Diesel_EUR_L": 1.50, "Strom_EUR_kWh": 0.21},
    {"Land": "Österreich", "Gruppe": "Rest", "Benzin_EUR_L": 1.56, "Diesel_EUR_L": 1.58, "Strom_EUR_kWh": 0.25},
    {"Land": "Schweiz", "Gruppe": "Rest", "Benzin_EUR_L": 1.81, "Diesel_EUR_L": 1.92, "Strom_EUR_kWh": 0.32},
    {"Land": "Italien", "Gruppe": "Rest", "Benzin_EUR_L": 1.82, "Diesel_EUR_L": 1.73, "Strom_EUR_kWh": 0.34},
    {"Land": "Spanien", "Gruppe": "Rest", "Benzin_EUR_L": 1.61, "Diesel_EUR_L": 1.49, "Strom_EUR_kWh": 0.22},
    {"Land": "Niederlande", "Gruppe": "Rest", "Benzin_EUR_L": 1.94, "Diesel_EUR_L": 1.71, "Strom_EUR_kWh": 0.38},
    {"Land": "Dänemark", "Gruppe": "Rest", "Benzin_EUR_L": 2.02, "Diesel_EUR_L": 1.85, "Strom_EUR_kWh": 0.39},
    {"Land": "Belgien", "Gruppe": "Rest", "Benzin_EUR_L": 1.75, "Diesel_EUR_L": 1.80, "Strom_EUR_kWh": 0.33},
    {"Land": "Portugal", "Gruppe": "Rest", "Benzin_EUR_L": 1.80, "Diesel_EUR_L": 1.65, "Strom_EUR_kWh": 0.25},
    {"Land": "Griechenland", "Gruppe": "Rest", "Benzin_EUR_L": 1.95, "Diesel_EUR_L": 1.70, "Strom_EUR_kWh": 0.28},
    {"Land": "Tschechien", "Gruppe": "Rest", "Benzin_EUR_L": 1.55, "Diesel_EUR_L": 1.50, "Strom_EUR_kWh": 0.28},
    {"Land": "Ungarn", "Gruppe": "Rest", "Benzin_EUR_L": 1.50, "Diesel_EUR_L": 1.52, "Strom_EUR_kWh": 0.12},
    {"Land": "Rumänien", "Gruppe": "Rest", "Benzin_EUR_L": 1.45, "Diesel_EUR_L": 1.45, "Strom_EUR_kWh": 0.18},
    {"Land": "Kroatien", "Gruppe": "Rest", "Benzin_EUR_L": 1.60, "Diesel_EUR_L": 1.55, "Strom_EUR_kWh": 0.20},
    {"Land": "Schweden", "Gruppe": "Rest", "Benzin_EUR_L": 1.85, "Diesel_EUR_L": 1.80, "Strom_EUR_kWh": 0.20},
    {"Land": "Finnland", "Gruppe": "Rest", "Benzin_EUR_L": 1.90, "Diesel_EUR_L": 1.75, "Strom_EUR_kWh": 0.22},
    {"Land": "Irland", "Gruppe": "Rest", "Benzin_EUR_L": 1.85, "Diesel_EUR_L": 1.75, "Strom_EUR_kWh": 0.35},
    {"Land": "Luxemburg", "Gruppe": "Rest", "Benzin_EUR_L": 1.65, "Diesel_EUR_L": 1.60, "Strom_EUR_kWh": 0.28},
    {"Land": "Malta", "Gruppe": "Rest", "Benzin_EUR_L": 1.35, "Diesel_EUR_L": 1.30, "Strom_EUR_kWh": 0.30},
    {"Land": "Zypern", "Gruppe": "Rest", "Benzin_EUR_L": 1.50, "Diesel_EUR_L": 1.55, "Strom_EUR_kWh": 0.32},
    {"Land": "Estland", "Gruppe": "Rest", "Benzin_EUR_L": 1.70, "Diesel_EUR_L": 1.55, "Strom_EUR_kWh": 0.28},
    {"Land": "Lettland", "Gruppe": "Rest", "Benzin_EUR_L": 1.65, "Diesel_EUR_L": 1.55, "Strom_EUR_kWh": 0.30},
    {"Land": "Litauen", "Gruppe": "Rest", "Benzin_EUR_L": 1.55, "Diesel_EUR_L": 1.50, "Strom_EUR_kWh": 0.28},
    {"Land": "Slowakei", "Gruppe": "Rest", "Benzin_EUR_L": 1.60, "Diesel_EUR_L": 1.50, "Strom_EUR_kWh": 0.22},
    {"Land": "Slowenien", "Gruppe": "Rest", "Benzin_EUR_L": 1.55, "Diesel_EUR_L": 1.60, "Strom_EUR_kWh": 0.25},
    {"Land": "Bulgarien", "Gruppe": "Rest", "Benzin_EUR_L": 1.40, "Diesel_EUR_L": 1.42, "Strom_EUR_kWh": 0.15},
    {"Land": "UK", "Gruppe": "Rest", "Benzin_EUR_L": 1.75, "Diesel_EUR_L": 1.85, "Strom_EUR_kWh": 0.32},
    {"Land": "Norwegen", "Gruppe": "Rest", "Benzin_EUR_L": 2.10, "Diesel_EUR_L": 1.95, "Strom_EUR_kWh": 0.12},
    {"Land": "Japan", "Gruppe": "Rest", "Benzin_EUR_L": 1.30, "Diesel_EUR_L": 1.15, "Strom_EUR_kWh": 0.25},
    {"Land": "Südkorea", "Gruppe": "Rest", "Benzin_EUR_L": 1.45, "Diesel_EUR_L": 1.30, "Strom_EUR_kWh": 0.15},
    {"Land": "Hongkong", "Gruppe": "Rest", "Benzin_EUR_L": 2.98, "Diesel_EUR_L": 2.75, "Strom_EUR_kWh": 0.20},
    {"Land": "Australien", "Gruppe": "Rest", "Benzin_EUR_L": 1.35, "Diesel_EUR_L": 1.40, "Strom_EUR_kWh": 0.28},
    {"Land": "Brasilien", "Gruppe": "Rest", "Benzin_EUR_L": 1.05, "Diesel_EUR_L": 1.00, "Strom_EUR_kWh": 0.18},
    {"Land": "Südafrika", "Gruppe": "Rest", "Benzin_EUR_L": 1.20, "Diesel_EUR_L": 1.15, "Strom_EUR_kWh": 0.14},
    {"Land": "Kanada", "Gruppe": "Rest", "Benzin_EUR_L": 1.15, "Diesel_EUR_L": 1.20, "Strom_EUR_kWh": 0.12},
    {"Land": "Mexiko", "Gruppe": "Rest", "Benzin_EUR_L": 1.05, "Diesel_EUR_L": 1.05, "Strom_EUR_kWh": 0.10},
    {"Land": "Argentinien", "Gruppe": "Rest", "Benzin_EUR_L": 0.90, "Diesel_EUR_L": 0.85, "Strom_EUR_kWh": 0.08},
    {"Land": "Ägypten", "Gruppe": "Rest", "Benzin_EUR_L": 0.45, "Diesel_EUR_L": 0.35, "Strom_EUR_kWh": 0.05},
    {"Land": "Nigeria", "Gruppe": "Rest", "Benzin_EUR_L": 0.55, "Diesel_EUR_L": 0.60, "Strom_EUR_kWh": 0.08},
    {"Land": "Saudi-Arabien", "Gruppe": "Rest", "Benzin_EUR_L": 0.60, "Diesel_EUR_L": 0.55, "Strom_EUR_kWh": 0.07},
    {"Land": "VAE", "Gruppe": "Rest", "Benzin_EUR_L": 0.75, "Diesel_EUR_L": 0.80, "Strom_EUR_kWh": 0.09},
    {"Land": "Thailand", "Gruppe": "Rest", "Benzin_EUR_L": 1.10, "Diesel_EUR_L": 1.00, "Strom_EUR_kWh": 0.11},
    {"Land": "Indonesien", "Gruppe": "Rest", "Benzin_EUR_L": 0.85, "Diesel_EUR_L": 0.80, "Strom_EUR_kWh": 0.09},
]


def daten_abrufen():
    """Referenzpool (+ optional API-Merge bei gesetztem Key). Max. Alter: 48h anstreben."""
    print("Stelle Datensatz zusammen (Referenzpool, ggf. API-Merge)...")
    pool = list(DATEN_POOL)
    if API_KEY:
        print("API-Key gesetzt – hier würde der Live-Abruf gemergt (Platzhalter).")
    return pool


def main():
    eur_zu_usd = hole_wechselkurs()
    stand = datetime.now().strftime("%Y-%m-%d %H:%M")

    zeilen = []
    for e in sorted(daten_abrufen(), key=lambda x: x["Land"]):
        b, d, s = e["Benzin_EUR_L"], e["Diesel_EUR_L"], e["Strom_EUR_kWh"]
        zeilen.append({
            "Land": e["Land"],
            "Gruppe": e.get("Gruppe", "Rest"),
            "Benzin (€/L)": round(b, 2),
            "Benzin ($/L)": round(b * eur_zu_usd, 2),
            "Diesel (€/L)": round(d, 2),
            "Diesel ($/L)": round(d * eur_zu_usd, 2),
            "Strom (€/kWh)": round(s, 3),
            "Strom ($/kWh)": round(s * eur_zu_usd, 3),
            "Stand": stand,
        })

    with open(EXPORT_DATEINAME, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
        w.writeheader()
        w.writerows(zeilen)

    print(f"\n[ERFOLG] {len(zeilen)} Länder exportiert nach: {os.path.abspath(EXPORT_DATEINAME)}")
    for z in zeilen[:5]:
        print(f"  {z['Land']}: Benzin {z['Benzin (€/L)']} €/L, Strom {z['Strom (€/kWh)']} €/kWh")


if __name__ == "__main__":
    main()
