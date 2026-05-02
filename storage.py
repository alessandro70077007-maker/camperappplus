"""Persistenza semplice su file JSON. Niente DB nel prototipo."""
import json
import locale
import os
import sys
from pathlib import Path
from datetime import date


_SUPPORTED_LANGS = ("it", "en", "de", "fr", "es")
_WIN_LANG_NAMES = {
    "italian": "it", "english": "en", "german": "de",
    "french": "fr", "spanish": "es",
}


def _detect_system_lang() -> str:
    """Lingua di sistema mappata sui codici supportati. Su Windows getlocale()
    puo' restituire 'Italian_Italy' invece di 'it_IT', quindi controlliamo
    sia il prefisso codice sia il nome esteso."""
    candidates = []
    try:
        loc = locale.getlocale()[0]
        if loc:
            candidates.append(loc)
    except (ValueError, TypeError):
        pass
    for var in ("LANG", "LC_ALL", "LC_MESSAGES", "LANGUAGE"):
        v = os.environ.get(var)
        if v:
            candidates.append(v)
    for cand in candidates:
        head = cand.lower().split(".")[0].split("_")[0].split("-")[0]
        if head in _SUPPORTED_LANGS:
            return head
        if head in _WIN_LANG_NAMES:
            return _WIN_LANG_NAMES[head]
    return "en"


_SYSTEM_LANG = _detect_system_lang()


_CURRENCY_SYMBOLS = {"EUR": "€", "CHF": "CHF"}


def currency_symbol(currency: str = "EUR") -> str:
    return _CURRENCY_SYMBOLS.get(currency, currency)


def fmt_money(amount, currency: str = "EUR", decimals: int = 2) -> str:
    """Formatta importo con simbolo valuta. Stile: 1.234,56 (it/de)."""
    sym = currency_symbol(currency)
    s = f"{amount:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sym} {s}"


def _data_dir() -> Path:
    # Quando l'app gira come exe PyInstaller, i dati utente vanno in
    # %APPDATA%/CamperAppPlus/data — separati dal bundle (read-only se
    # installato in Program Files) e persistenti tra reinstall.
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("APPDATA") or Path.home())
        return base / "CamperAppPlus" / "data"
    return Path(__file__).parent / "data"


DATA_DIR = _data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILES_DIR = DATA_DIR / "files"
FILES_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "camper.json"


def _default_db():
    return {
        "campers": [],
        "scadenze": [],
        "interventi": [],
        "viaggi": [],
        "rifornimenti": [],
        "checklist": [],
        "documenti": [],
        "impostazioni": {
            "lingua": _SYSTEM_LANG,
            "valuta": "EUR",
            "giorni_promemoria": 30,
            "email": "",
            "smtp_host": "",
            "smtp_port": 587,
            "smtp_user": "",
            "smtp_pass": "",
            "nickname": "",
            "auto_invio": False,
            "ultimo_invio": "",
            "auto_invio_desktop": False,
            "ultimo_invio_desktop": "",
        },
    }


def load():
    if not DB_FILE.exists():
        return _default_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
    # backfill chiavi mancanti per compat con DB precedenti
    default = _default_db()
    for k, v in default.items():
        if k not in db:
            db[k] = v
    if "impostazioni" in db:
        for k, v in default["impostazioni"].items():
            db["impostazioni"].setdefault(k, v)
    # rimuovi chiavi obsolete da DB precedenti
    db.pop("chat_rooms", None)
    # backfill campi nuovi sui record esistenti
    for c in db.get("campers", []):
        c.setdefault("km_iniziale", c.get("km", 0))
    for r in db.get("rifornimenti", []):
        r.setdefault("pieno", True)
    for i in db.get("interventi", []):
        i.setdefault("categoria", "altro")
    return db


def save(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False, default=str)


def _next_id(items):
    return max([x["id"] for x in items], default=0) + 1


# ---------- Camper ----------
def add_camper(marca, modello, anno, targa, km):
    db = load()
    new_id = _next_id(db["campers"])
    db["campers"].append({
        "id": new_id,
        "marca": marca,
        "modello": modello,
        "anno": anno,
        "targa": targa.upper(),
        "km": km,
        "km_iniziale": km,
    })
    save(db)
    return new_id


def update_camper_km(camper_id, km):
    db = load()
    for c in db["campers"]:
        if c["id"] == camper_id:
            c["km"] = km
    save(db)


def update_camper_km_iniziale(camper_id, km_iniziale):
    db = load()
    for c in db["campers"]:
        if c["id"] == camper_id:
            c["km_iniziale"] = km_iniziale
    save(db)


def delete_camper(camper_id):
    db = load()
    db["campers"] = [c for c in db["campers"] if c["id"] != camper_id]
    db["scadenze"] = [s for s in db["scadenze"] if s["camper_id"] != camper_id]
    db["interventi"] = [i for i in db["interventi"] if i["camper_id"] != camper_id]
    db["viaggi"] = [v for v in db["viaggi"] if v["camper_id"] != camper_id]
    db["rifornimenti"] = [r for r in db["rifornimenti"] if r["camper_id"] != camper_id]
    db["checklist"] = [k for k in db["checklist"] if k["camper_id"] != camper_id]
    # rimuovi anche file documenti collegati
    for d in [d for d in db["documenti"] if d["camper_id"] == camper_id]:
        f = FILES_DIR / d["filename_storage"]
        if f.exists():
            f.unlink()
    db["documenti"] = [d for d in db["documenti"] if d["camper_id"] != camper_id]
    save(db)


# ---------- Scadenze ----------
def add_scadenza(camper_id, tipo, data_scadenza, note):
    db = load()
    new_id = _next_id(db["scadenze"])
    db["scadenze"].append({
        "id": new_id,
        "camper_id": camper_id,
        "tipo": tipo,
        "data": str(data_scadenza),
        "note": note,
    })
    save(db)


def delete_scadenza(scadenza_id):
    db = load()
    db["scadenze"] = [s for s in db["scadenze"] if s["id"] != scadenza_id]
    save(db)


# ---------- Interventi ----------
def add_intervento(camper_id, data_intervento, descrizione, costo, km, categoria="altro"):
    db = load()
    new_id = _next_id(db["interventi"])
    db["interventi"].append({
        "id": new_id,
        "camper_id": camper_id,
        "data": str(data_intervento),
        "descrizione": descrizione,
        "costo": costo,
        "km": km,
        "categoria": categoria,
    })
    save(db)


def delete_intervento(intervento_id):
    db = load()
    db["interventi"] = [i for i in db["interventi"] if i["id"] != intervento_id]
    save(db)


# ---------- Viaggi ----------
def add_viaggio(camper_id, data_inizio, data_fine, destinazione, km_percorsi, costo, note):
    db = load()
    new_id = _next_id(db["viaggi"])
    db["viaggi"].append({
        "id": new_id,
        "camper_id": camper_id,
        "data_inizio": str(data_inizio),
        "data_fine": str(data_fine),
        "destinazione": destinazione,
        "km_percorsi": km_percorsi,
        "costo": costo,
        "note": note,
    })
    save(db)


def delete_viaggio(viaggio_id):
    db = load()
    db["viaggi"] = [v for v in db["viaggi"] if v["id"] != viaggio_id]
    save(db)


# ---------- Rifornimenti ----------
def add_rifornimento(camper_id, data_rif, km, litri, costo, distributore, note, pieno=True):
    db = load()
    new_id = _next_id(db["rifornimenti"])
    db["rifornimenti"].append({
        "id": new_id,
        "camper_id": camper_id,
        "data": str(data_rif),
        "km": km,
        "litri": litri,
        "costo": costo,
        "distributore": distributore,
        "note": note,
        "pieno": pieno,
    })
    save(db)


def delete_rifornimento(rifornimento_id):
    db = load()
    db["rifornimenti"] = [r for r in db["rifornimenti"] if r["id"] != rifornimento_id]
    save(db)


# ---------- Checklist ----------
def add_checklist_voce(camper_id, voce, categoria):
    db = load()
    new_id = _next_id(db["checklist"])
    db["checklist"].append({
        "id": new_id,
        "camper_id": camper_id,
        "voce": voce,
        "categoria": categoria,
        "fatto": False,
    })
    save(db)


def toggle_checklist_voce(voce_id):
    db = load()
    for v in db["checklist"]:
        if v["id"] == voce_id:
            v["fatto"] = not v["fatto"]
    save(db)


def delete_checklist_voce(voce_id):
    db = load()
    db["checklist"] = [v for v in db["checklist"] if v["id"] != voce_id]
    save(db)


def reset_checklist(camper_id, categoria):
    db = load()
    for v in db["checklist"]:
        if v["camper_id"] == camper_id and v["categoria"] == categoria:
            v["fatto"] = False
    save(db)


# ---------- Documenti ----------
def add_documento(camper_id, tipo, nome_originale, contenuto_bytes, note):
    db = load()
    new_id = _next_id(db["documenti"])
    # nome storage univoco
    suffix = Path(nome_originale).suffix
    storage_name = f"doc_{new_id}{suffix}"
    target = FILES_DIR / storage_name
    target.write_bytes(contenuto_bytes)
    db["documenti"].append({
        "id": new_id,
        "camper_id": camper_id,
        "tipo": tipo,
        "nome_originale": nome_originale,
        "filename_storage": storage_name,
        "data_caricamento": str(date.today()),
        "note": note,
    })
    save(db)


def delete_documento(documento_id):
    db = load()
    target = None
    for d in db["documenti"]:
        if d["id"] == documento_id:
            target = FILES_DIR / d["filename_storage"]
            break
    if target and target.exists():
        target.unlink()
    db["documenti"] = [d for d in db["documenti"] if d["id"] != documento_id]
    save(db)


def documento_path(documento):
    return FILES_DIR / documento["filename_storage"]


# ---------- Impostazioni ----------
def update_impostazioni(**kwargs):
    db = load()
    db["impostazioni"].update(kwargs)
    save(db)


