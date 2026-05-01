"""Export/import dati come ZIP (camper.json + cartella files/)."""
import io
import json
import zipfile
from datetime import datetime

import storage


DB_ARCNAME = "camper.json"
FILES_PREFIX = "files/"


def export_zip() -> tuple[str, bytes]:
    """Costruisce uno ZIP con il DB e tutti i documenti allegati.
    Ritorna (filename, bytes)."""
    db = storage.load()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(DB_ARCNAME, json.dumps(db, indent=2, ensure_ascii=False, default=str))
        if storage.FILES_DIR.exists():
            for f in storage.FILES_DIR.iterdir():
                if f.is_file():
                    zf.write(f, FILES_PREFIX + f.name)
    fname = f"camperappplus_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    return fname, buf.getvalue()


def import_zip(zip_bytes: bytes) -> dict:
    """Sostituisce DB e files con i contenuti dello ZIP. Ritorna il DB importato.
    Solleva ValueError se lo ZIP non e' valido."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    except zipfile.BadZipFile as e:
        raise ValueError(f"file ZIP corrotto: {e}") from e

    if DB_ARCNAME not in zf.namelist():
        raise ValueError(f"manca {DB_ARCNAME} nel backup")

    try:
        db = json.loads(zf.read(DB_ARCNAME).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(f"camper.json non valido: {e}") from e

    if not isinstance(db, dict) or "campers" not in db:
        raise ValueError("camper.json non ha la struttura attesa")

    # Svuota la cartella files/ prima di ripristinare
    if storage.FILES_DIR.exists():
        for f in storage.FILES_DIR.iterdir():
            if f.is_file():
                f.unlink()
    storage.FILES_DIR.mkdir(parents=True, exist_ok=True)

    for name in zf.namelist():
        if name.startswith(FILES_PREFIX) and not name.endswith("/"):
            target = storage.FILES_DIR / name[len(FILES_PREFIX):]
            target.write_bytes(zf.read(name))

    storage.save(db)
    return db
