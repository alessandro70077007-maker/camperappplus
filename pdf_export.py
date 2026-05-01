"""Generazione PDF del libretto digitale per un camper."""
from datetime import date
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
)

from translations import t


def build_libretto_pdf(db, camper_id, lang: str = "it") -> bytes:
    def L(key, **kwargs):
        return t(key, lang, **kwargs)

    camper = next((c for c in db["campers"] if c["id"] == camper_id), None)
    if camper is None:
        return b""

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=f"Libretto {camper['marca']} {camper['modello']}",
    )
    styles = getSampleStyleSheet()
    h_title = ParagraphStyle("title", parent=styles["Title"], fontSize=20, spaceAfter=12)
    h_section = ParagraphStyle("section", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6)

    story = []
    story.append(Paragraph(L("pdf_title"), h_title))
    story.append(Paragraph(
        f"<b>{camper['marca']} {camper['modello']}</b> — {L('year')} {camper['anno']}<br/>"
        f"{L('plate')}: {camper['targa']} · Km: {camper['km']:,}".replace(",", "."),
        styles["Normal"],
    ))
    story.append(Paragraph(
        L("pdf_generated_on", date=date.today().strftime('%d/%m/%Y')),
        styles["Italic"],
    ))
    story.append(Spacer(1, 12))

    # ----- Scadenze -----
    story.append(Paragraph(L("pdf_section_deadlines"), h_section))
    scads = sorted(
        [s for s in db["scadenze"] if s["camper_id"] == camper_id],
        key=lambda x: x["data"],
    )
    if not scads:
        story.append(Paragraph(L("pdf_no_deadlines"), styles["Normal"]))
    else:
        data = [[L("type"), L("date"), L("notes")]]
        for s in scads:
            d = date.fromisoformat(s["data"]).strftime("%d/%m/%Y")
            data.append([s["tipo"], d, s["note"] or ""])
        story.append(_make_table(data))

    # ----- Interventi -----
    story.append(Paragraph(L("pdf_section_maintenance"), h_section))
    ints = sorted(
        [i for i in db["interventi"] if i["camper_id"] == camper_id],
        key=lambda x: x["data"], reverse=True,
    )
    if not ints:
        story.append(Paragraph(L("pdf_no_interventions"), styles["Normal"]))
    else:
        data = [[L("date"), L("km"), L("description"), L("cost")]]
        for i in ints:
            d = date.fromisoformat(i["data"]).strftime("%d/%m/%Y")
            data.append([
                d,
                f"{i['km']:,}".replace(",", "."),
                i["descrizione"],
                f"€ {i['costo']:.2f}",
            ])
        totale = sum(i["costo"] for i in ints)
        data.append(["", "", L("total"), f"€ {totale:.2f}"])
        story.append(_make_table(data, total_row=True))

    # ----- Viaggi -----
    story.append(Paragraph(L("pdf_section_trips"), h_section))
    vias = sorted(
        [v for v in db["viaggi"] if v["camper_id"] == camper_id],
        key=lambda x: x["data_inizio"], reverse=True,
    )
    if not vias:
        story.append(Paragraph(L("pdf_no_trips"), styles["Normal"]))
    else:
        data = [[L("destination"), L("from"), L("to"), L("km"), L("cost")]]
        for v in vias:
            di = date.fromisoformat(v["data_inizio"]).strftime("%d/%m/%Y")
            df_ = date.fromisoformat(v["data_fine"]).strftime("%d/%m/%Y")
            data.append([
                v["destinazione"], di, df_,
                f"{v['km_percorsi']:,}".replace(",", "."),
                f"€ {v['costo']:.2f}",
            ])
        story.append(_make_table(data))

    # ----- Rifornimenti -----
    story.append(Paragraph(L("pdf_section_fuel"), h_section))
    rifs = sorted(
        [r for r in db["rifornimenti"] if r["camper_id"] == camper_id],
        key=lambda x: x["data"], reverse=True,
    )
    if not rifs:
        story.append(Paragraph(L("pdf_no_fuel"), styles["Normal"]))
    else:
        data = [[L("date"), L("km"), L("liters"), L("cost"), L("station")]]
        for r in rifs:
            d = date.fromisoformat(r["data"]).strftime("%d/%m/%Y")
            data.append([
                d,
                f"{r['km']:,}".replace(",", "."),
                f"{r['litri']:.2f}",
                f"€ {r['costo']:.2f}",
                r["distributore"] or "",
            ])
        story.append(_make_table(data))

    doc.build(story)
    return buf.getvalue()


def _make_table(data, total_row=False):
    t_ = Table(data, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b6cb0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]
    if total_row:
        style.append(("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"))
        style.append(("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e2e8f0")))
    t_.setStyle(TableStyle(style))
    return t_
