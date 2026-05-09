"""Avvia l'app Flet in modalita' web e stampa un QR code per aprirla
dal telefono sulla stessa rete WiFi.

Uso:
    python mobile/run_qr.py [porta]      # porta default: 8550
"""
import os
import socket
import sys
from pathlib import Path

# Disabilita l'apertura automatica del browser fatta da Flet con
# AppView.WEB_BROWSER. Flet aprirebbe Edge sull'URL host (0.0.0.0), che
# il browser rifiuta come ERR_ADDRESS_INVALID. Con questa env var settata
# Flet salta open_in_browser() (vedi flet/app.py: il check e' "url_prefix
# is None") e l'utente apre manualmente localhost dal PC o scansiona il QR.
os.environ.setdefault("FLET_DISPLAY_URL_PREFIX", "")

# Su Windows il terminale e' spesso cp1252: senza UTF-8 i blocchi del QR
# (█ etc.) crasciano con UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

import qrcode

import flet as ft

# Importa il main della UI senza far partire ft.run del modulo
sys.path.insert(0, str(Path(__file__).parent))
from app import main


PORT_DEFAULT = 8550


def lan_ip() -> str:
    """IP LAN di questa macchina (non 127.0.0.1). Apre un socket UDP verso
    un IP pubblico: non viene inviato nulla, ma l'OS sceglie l'interfaccia
    di uscita e con getsockname otteniamo l'IP locale corrispondente."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def print_qr(url: str) -> None:
    qr = qrcode.QRCode(box_size=1, border=1)
    qr.add_data(url)
    qr.make()
    # invert=True: blocchi pieni su sfondo chiaro -> leggibile su terminali scuri
    qr.print_ascii(invert=True)


def save_qr_png(url: str, path: Path) -> None:
    """Backup PNG: utile se i caratteri Unicode dell'ASCII QR non si vedono
    bene nel terminale corrente."""
    img = qrcode.make(url)
    img.save(path)


def main_run() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT_DEFAULT
    ip = lan_ip()
    url = f"http://{ip}:{port}"

    png_path = Path(__file__).parent / "qr_telefono.png"
    save_qr_png(url, png_path)

    print()
    print("=" * 64)
    print("  CAMPERappPLUS Mobile - Anteprima sul telefono")
    print("=" * 64)
    print()
    print(f"  URL:  {url}")
    print(f"  QR (anche salvato in {png_path.name}):")
    print()
    print_qr(url)
    print()
    print("  Il telefono deve essere sulla STESSA rete WiFi del PC.")
    print(f"  Se non si collega: Windows Firewall sta bloccando la porta {port}?")
    print("  (Al primo avvio Windows mostra un popup: 'Consenti accesso'.)")
    print("=" * 64)
    print()

    # assets_dir: Flet serve i file qui dentro alla root dell'URL e
    # SOVRASCRIVE quelli di default (es. manifest.json, icons/*, favicon.png).
    # Cosi' il telefono vede le icone CamperApp invece di quelle generiche
    # Flet quando si fa "Aggiungi a schermata Home".
    assets = str(Path(__file__).parent / "assets")
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=port,
        assets_dir=assets,
    )


if __name__ == "__main__":
    main_run()
