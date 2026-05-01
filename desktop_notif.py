"""Notifiche toast Windows native via PowerShell + Windows.UI.Notifications.
Niente pip dependencies: tutto si appoggia a PowerShell gia' presente su Win10+.

Cooldown 24h indipendente da quello email (timestamp 'ultimo_invio_desktop')."""
import subprocess
import sys
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

import storage
from translations import t
from notifications import imminent_deadlines


AUTO_COOLDOWN = timedelta(hours=24)
APP_ID = "CAMPERappPLUS"


def is_supported() -> bool:
    return sys.platform == "win32"


def _build_ps_script(title: str, body: str) -> str:
    """Genera lo script PowerShell che mostra il toast.
    Title/body XML-escapati per sicurezza."""
    t_xml = escape(title)
    b_xml = escape(body)
    xml_doc = (
        "<toast>"
        "<visual>"
        "<binding template=\"ToastGeneric\">"
        f"<text>{t_xml}</text>"
        f"<text>{b_xml}</text>"
        "</binding>"
        "</visual>"
        "</toast>"
    )
    return (
        "$ErrorActionPreference='Stop';"
        "[Windows.UI.Notifications.ToastNotificationManager,"
        "Windows.UI.Notifications,ContentType=WindowsRuntime]>$null;"
        "[Windows.Data.Xml.Dom.XmlDocument,"
        "Windows.Data.Xml.Dom.XmlDocument,ContentType=WindowsRuntime]>$null;"
        f"$xml=New-Object Windows.Data.Xml.Dom.XmlDocument;"
        f"$xml.LoadXml('{xml_doc}');"
        f"$toast=New-Object Windows.UI.Notifications.ToastNotification $xml;"
        f"[Windows.UI.Notifications.ToastNotificationManager]"
        f"::CreateToastNotifier('{APP_ID}').Show($toast)"
    )


def show_toast(title: str, body: str) -> str | None:
    """Mostra una notifica toast. Ritorna None se ok, stringa errore altrimenti."""
    if not is_supported():
        return "UNSUPPORTED_PLATFORM"
    ps_script = _build_ps_script(title, body)
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive",
             "-WindowStyle", "Hidden", "-Command", ps_script],
            capture_output=True, text=True, timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            return result.stderr.strip() or f"powershell exit {result.returncode}"
    except (OSError, subprocess.TimeoutExpired) as e:
        return str(e)
    return None


def _format_body(items, lang: str, max_items: int = 3) -> str:
    """Compone il body del toast: prime N scadenze + 'e altre M' se servono."""
    db = storage.load()
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    lines = []
    for giorni, s, d in items[:max_items]:
        when = t("expired", lang) if giorni < 0 else t("in_n_days", lang, n=giorni)
        camper_name = cmap.get(s["camper_id"], "?")
        lines.append(f"• {s['tipo']} ({camper_name}) — {when}")
    if len(items) > max_items:
        lines.append(t("toast_more_items", lang, n=len(items) - max_items))
    return "\n".join(lines)


def auto_send_desktop_if_due(lang: str = "it") -> tuple[int, str | None]:
    """Mostra il toast all'avvio se attivo + cooldown 24h passato.
    Ritorna (n_scadenze_notificate, errore_o_None)."""
    if not is_supported():
        return 0, None
    db = storage.load()
    imp = db["impostazioni"]
    if not imp.get("auto_invio_desktop"):
        return 0, None

    last = imp.get("ultimo_invio_desktop") or ""
    if last:
        try:
            last_dt = datetime.fromisoformat(last)
            if datetime.now() - last_dt < AUTO_COOLDOWN:
                return 0, None
        except ValueError:
            pass

    items = imminent_deadlines(db)
    if not items:
        return 0, None

    title = t("toast_title", lang, n=len(items))
    body = _format_body(items, lang)
    err = show_toast(title, body)
    if err:
        return 0, err

    storage.update_impostazioni(
        ultimo_invio_desktop=datetime.now().isoformat(timespec="seconds")
    )
    return len(items), None
