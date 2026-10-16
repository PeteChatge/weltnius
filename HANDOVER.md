# WELTNIUS — Chat-Übergabe (Stand 16.10.2026)

Diese Datei übergibt den kompletten Arbeitsstand an einen neuen PC / neuen Chat.
Repo: https://github.com/PeteChatge/weltnius (Branch `main`, GitHub Pages aktiv).
Live: https://petechatge.github.io/weltnius/ — Einstieg `index.html` (monolithisch, 1 Datei).

## Grundidee
Der Windows-11-Widgets-Feed wiederholt monatealte Meldungen. WELTNIUS zeigt statt
dessen nur **noch nie gezeigte Beiträge** (Klick = gelesen, grau aber klickbar),
sortiert: Regional (Dresden/Sachsen) → EU → USA → RU → China → Hot/Danger
(Israel/Türkei/Indien) → Asien-Ozeanien → Fundstücke. Eine Edge-Extension wurde
verworfen (kein DOM-Zugriff aufs Widgets-Board) — WebApp statt Extension.

## Getroffene Entscheidungen (Grill-Runden, verbindlich)
- Gesehen = Klick/Öffnen, Hash aus URL+Titel, localStorage, Behaltedauer per
  Zahlenfeld (Default 7 Tage) + lesbar grau + „Nur Ungelesene"-Toggle.
- Dual-Label: ÖRR/gelenkt vs. kritisch (Tichy, NIUS, Welt, Achgut) + YouTube-Links.
- Kopf: OSM-Karte mit Pin (Default Dresden), 7 Blöcke, Themen-Tags (4 fix + bis zu
  6 freie), Hell/Dunkel (Default dunkel, Pastell-Light ohne Weiß), Ticker im
  Telegrammstil mit Puls-Linien + Tempo-Regler, Export-Button (orange, lädt
  Stand als HTML mit Snapshot), Taschenrechner-Tastenraster neben Gazette.
- Artikeltexte lang (2 Sätze mehr, Satzgrenzen-Schnitt), Zeitungslayout
  mehrspaltig / Handy einspaltig.

## Quellen (alle ohne API-Key, CORS via AllOrigins/corsproxy-Fallbacks)
RSS: Tagesschau, ZDFheute, MDR Sachsen, Euronews DE, Tichy, NIUS (optional, oft
404), Welt, Achgut, Sächsische Zeitung (optional, WAF-403 möglich), Katapult
Sachsen, Freie Presse Erzgebirge (Atom — Parser ist Atom-fähig).
YouTube-Kanal-RSS (echte Thumbnails): NIUS `UCQGqiGhMjc_p4lZEhSTb12g`,
WELT `UCZMsvbAhhRblVGXmEXW8TSA`. Wochenblättle = Google-News-RSS zum Pin-Ort
(ohne Liste, automatisch). Ortsblätter (`CONFIG.localPapers`, sachsenweit
sichtbar): Königsbrücker Stadtanzeiger (monatliches PDF, kein RSS).
Preise (`CONFIG.prices`, 54 Länder, EU-27 einzeln): Tracker-Beispielwerte +
CSV-Import/Export (`energiepreis-tracker.py` im Repo, stdlib-only, getestet).
Karte: Leaflet 1.9.4 (CDN) + CARTO-Kacheln — **Gratis-Key nötig**
(carto.com/basemaps/apikey, ohne Konto), Feld im Regionen-Dialog.
TraderFox: nur Link (`?view=desktop`), Einbetten blockiert X-Frame-Options.

## Bekannte Fallstricke (alle gefixt, bitte nicht regressieren)
- Leaflet nur lazy im Dialog öffnen + `invalidateSize()` (sonst 1/8-Kachel).
- Längengrad auf ±180 normieren (Weltkopien → -706).
- `overflow-x:clip` + `min-width:0` (Chrome-Seitenscrollen).
- Store mit Memory-Fallback (file://-Quirks), Export-Seed ÜBERSCHREIBT State.
- Export: Dialog-`open`-Attribut + Reload-Spinner im HTML strippen.
- Seed-JSON: `<` als `\u003c` escapen (sonst `</script>`-Bruch).

## Offen
- **Samstag: https://petechatge.github.io/radio-agent gründlich überarbeiten.**
- User testet Inhalte mehrere Tage; Preistabelle braucht ggf. echte Live-Quelle.
- Weiterer Content-Check „ländlicher Raum" läuft (Rural-Autoerkennung via
  Nominatim-Typ + Großstadt-Liste + Checkbox, Wochenblättle als Rückhalt).

## Arbeitsweise des Users
Deutsch, kurze Aufträge, erwartet sofortiges Committen+Pushen („damit es fixed
ist"). Er bestätigt gern Zwischenergebnisse. Kein API-Key-Chatversand.
