"""Invio email dei promemoria scadenze. Usato sia dal bottone manuale
in Impostazioni sia dall'invio automatico all'avvio."""
import smtplib
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText

import storage
from translations import t


AUTO_COOLDOWN = timedelta(hours=24)


def imminent_deadlines(db):
    """Ritorna [(giorni, scadenza, data)] entro la soglia, ordinate per giorni."""
    soglia = db["impostazioni"].get("giorni_promemoria", 30)
    out = []
    for s in db["scadenze"]:
        d = date.fromisoformat(s["data"])
        giorni = (d - date.today()).days
        if giorni <= soglia:
            out.append((giorni, s, d))
    out.sort(key=lambda x: x[0])
    return out


def is_smtp_configured(db) -> bool:
    imp = db["impostazioni"]
    return bool(imp.get("email") and imp.get("smtp_host") and imp.get("smtp_user"))


def _build_body(db, items, lang):
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    righe = []
    for giorni, s, d in items:
        when = t("expired", lang) if giorni < 0 else t("in_n_days", lang, n=giorni)
        righe.append(
            f"- {s['tipo']} ({cmap.get(s['camper_id'], '?')}) "
            f"— {d.strftime('%d/%m/%Y')} ({when})"
        )
    return t("email_intro", lang) + "\n".join(righe)


def send_reminders(lang: str = "it") -> tuple[int, str | None]:
    """Invia l'email dei promemoria. Aggiorna 'ultimo_invio' su successo.
    Ritorna (numero_scadenze_inviate, errore_o_None).
    Se non c'e' nulla da inviare ritorna (0, None) senza toccare nulla."""
    db = storage.load()
    if not is_smtp_configured(db):
        return 0, "SMTP_NOT_CONFIGURED"

    items = imminent_deadlines(db)
    if not items:
        return 0, None

    imp = db["impostazioni"]
    msg = MIMEText(_build_body(db, items, lang))
    msg["Subject"] = t("email_subject", lang, n=len(items))
    msg["From"] = imp["smtp_user"]
    msg["To"] = imp["email"]

    try:
        with smtplib.SMTP(imp["smtp_host"], int(imp["smtp_port"])) as srv:
            srv.starttls()
            srv.login(imp["smtp_user"], imp["smtp_pass"])
            srv.send_message(msg)
    except Exception as e:
        return 0, str(e)

    storage.update_impostazioni(ultimo_invio=datetime.now().isoformat(timespec="seconds"))
    return len(items), None


def auto_send_if_due(lang: str = "it") -> tuple[int, str | None]:
    """Invio automatico all'avvio: rispetta auto_invio + cooldown 24h.
    Ritorna (n_inviate, errore). (0, None) se non e' il momento."""
    db = storage.load()
    imp = db["impostazioni"]
    if not imp.get("auto_invio"):
        return 0, None
    if not is_smtp_configured(db):
        return 0, None
    last = imp.get("ultimo_invio") or ""
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if datetime.now() - last_dt < AUTO_COOLDOWN:
                return 0, None
        except ValueError:
            pass  # timestamp invalido, procedi
    return send_reminders(lang)
