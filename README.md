# CAMPERappPLUS

App desktop per camperisti italiani: gestione scadenze, libretto digitale,
viaggi, consumi, aree sosta su mappa, meteo. Tutto in locale, niente account.

Stack: **Streamlit** + **PyInstaller** + **Edge in modalità app**.

## Feature principali

- **Scadenze** revisione/assicurazione/bombole con promemoria automatici via email o toast Windows
- **Libretto digitale** interventi con categoria, costo, km. Export PDF
- **Diario viaggi** con totali km, spesa, costo per km
- **Rifornimenti** con flag "pieno": calcolo l/100km accurato
- **Aree sosta** camper / camper service / campeggi / aree verdi su mappa folium con cluster (dati OpenStreetMap)
- **Meteo** posizione attuale o per nome città (Open-Meteo, no API key)
- **Documenti** allegati per camper (libretto, polizze, ricevute, foto)
- **Checklist** personalizzate per partenza/apertura/chiusura/manutenzione
- **Backup/restore** completo in ZIP (DB + allegati)
- **Multilingua**: it / en / de / fr / es

## Avvio in dev

```bash
cd CamperApp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Apre il browser su `http://localhost:8501`.

## Build distribuibile (Windows)

```bash
pyinstaller --noconfirm CamperAppPlus.spec
```

Output in `dist\CamperAppPlus\` (cartella autosufficiente con `CamperAppPlus.exe`).

Il bundle include un `launcher.py` che:
1. Avvia Streamlit in subprocess su porta libera
2. Apre Microsoft Edge in modalità `--app=` con un profilo dedicato
3. Polla i processi Edge sul nostro profilo: chiude Streamlit solo quando l'utente chiude tutte le finestre

## Struttura moduli

| File | Ruolo |
|---|---|
| `app.py` | UI Streamlit, 11 pagine |
| `storage.py` | Persistenza JSON in `%APPDATA%\CamperAppPlus\data` (frozen) o `data/` (dev) |
| `translations.py` | Stringhe localizzate (it/en/de/fr/es) |
| `pdf_export.py` | Export libretto in PDF (reportlab) |
| `backup.py` | Export/import ZIP del DB + allegati |
| `notifications.py` | Invio email scadenze (manuale + automatico con cooldown 24h) |
| `desktop_notif.py` | Toast Windows nativi via PowerShell + `Windows.UI.Notifications` |
| `poi.py` | Aree sosta da Overpass API con cache 24h |
| `weather.py` | Meteo + geocoding via Open-Meteo |
| `launcher.py` | Boot Streamlit + Edge in modalità app (per il bundle) |
| `make_icon.py` | Genera `icon.ico` |

## Dati utente

- **Dev**: `data/camper.json` accanto al codice
- **Frozen**: `%APPDATA%\CamperAppPlus\data\camper.json`

Backup completo (DB + cartella `files/` con allegati) come ZIP da Impostazioni.

## Privacy

- Nessun account, nessun cloud, nessuna telemetria
- Connessione internet usata solo per: tile mappa OpenStreetMap, query Overpass per i POI, Open-Meteo per meteo+geocoding, geolocalizzazione browser
- Email scadenze via SMTP utente (se configurato dall'utente)

## Licenza / contatti

Progetto personale. Feedback: alessandro7007@live.it
