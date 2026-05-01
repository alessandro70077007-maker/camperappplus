"""Genera icon.ico (placeholder).

Eseguire una volta:  python make_icon.py
Sostituibile in seguito con un'icona vera (basta che il file resti
icon.ico nella stessa cartella).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "icon.ico"
SIZE = 256
BG = (45, 110, 165)        # blu camper
ACCENT = (255, 200, 70)    # giallo finestrino
WHEEL = (30, 30, 30)


def draw_camper(d: ImageDraw.ImageDraw, s: int) -> None:
    # corpo del camper: rettangolo arrotondato bianco
    body = (int(s * 0.10), int(s * 0.32), int(s * 0.90), int(s * 0.72))
    d.rounded_rectangle(body, radius=int(s * 0.06), fill="white")
    # cabina (parte anteriore piu bassa) — quadrato sporgente sx
    cab = (int(s * 0.05), int(s * 0.45), int(s * 0.32), int(s * 0.72))
    d.rounded_rectangle(cab, radius=int(s * 0.04), fill="white")
    # finestrino cabina
    win = (int(s * 0.08), int(s * 0.50), int(s * 0.29), int(s * 0.62))
    d.rounded_rectangle(win, radius=int(s * 0.02), fill=ACCENT)
    # fascia colorata sotto i finestrini posteriori
    band = (int(s * 0.34), int(s * 0.55), int(s * 0.88), int(s * 0.62))
    d.rectangle(band, fill=ACCENT)
    # ruote
    r = int(s * 0.07)
    for cx in (int(s * 0.22), int(s * 0.72)):
        cy = int(s * 0.74)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHEEL)
        d.ellipse((cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2),
                  fill="white")


def main() -> None:
    img = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    d = ImageDraw.Draw(img)
    draw_camper(d, SIZE)
    img.save(
        OUT,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
               (128, 128), (256, 256)],
    )
    print(f"creato: {OUT}")


if __name__ == "__main__":
    main()
