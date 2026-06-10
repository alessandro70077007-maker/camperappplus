"""CAMPERappPLUS Mobile — versione Flet.

Stessa logica/dati dell'app Streamlit. I moduli puri (storage, translations,
poi, weather, ...) sono importati dalla radice del progetto, cosi' le due app
condividono `data/camper.json`.

Avvio:
    python mobile/app.py             # finestra desktop Flet
    flet run mobile/app.py           # idem, via CLI
    flet build apk mobile            # build Android (richiede Flutter SDK)
"""
import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flet as ft

import affiliates
import poi
import storage
from translations import t as _t, LINGUE_DISPONIBILI
from weather import code_to_emoji_key, fetch_weather, geocode


# Etichette UI proprie del mobile, non presenti in translations.py.
# Le tengo qui per non toccare il file condiviso.
_MOBILE_LABELS = {
    "more": {"it": "Altro", "en": "More", "de": "Mehr", "fr": "Plus", "es": "Mas"},
    "in_progress": {
        "it": "In costruzione", "en": "Under construction",
        "de": "In Bearbeitung", "fr": "En construction", "es": "En construccion",
    },
    "date_format_hint": {
        "it": "Formato: GG/MM/AAAA",
        "en": "Format: DD/MM/YYYY",
        "de": "Format: TT.MM.JJJJ (verwende /)",
        "fr": "Format: JJ/MM/AAAA",
        "es": "Formato: DD/MM/AAAA",
    },
    "invalid_date": {
        "it": "Data non valida",
        "en": "Invalid date",
        "de": "Ungültiges Datum",
        "fr": "Date invalide",
        "es": "Fecha no válida",
    },
    "theme_section": {
        "it": "Tema", "en": "Theme", "de": "Design",
        "fr": "Thème", "es": "Tema",
    },
    "theme_system": {
        "it": "Sistema", "en": "System", "de": "System",
        "fr": "Système", "es": "Sistema",
    },
    "theme_light": {
        "it": "Chiaro", "en": "Light", "de": "Hell",
        "fr": "Clair", "es": "Claro",
    },
    "theme_dark": {
        "it": "Scuro", "en": "Dark", "de": "Dunkel",
        "fr": "Sombre", "es": "Oscuro",
    },
    "reset_confirm": {
        "it": "Azzerare tutte le voci di questa categoria?",
        "en": "Reset all items in this category?",
        "de": "Alle Eintraege dieser Kategorie zuruecksetzen?",
        "fr": "Réinitialiser tous les éléments de cette catégorie?",
        "es": "Restablecer todos los elementos de esta categoría?",
    },
    "saved_ok": {
        "it": "Salvato", "en": "Saved", "de": "Gespeichert",
        "fr": "Enregistré", "es": "Guardado",
    },
    "send_now_disabled_hint": {
        "it": "Salva un'email destinatario e aggiungi almeno una scadenza "
              "imminente per abilitare l'invio.",
        "en": "Save a recipient email and add at least one upcoming "
              "deadline to enable sending.",
        "de": "Speichere eine Empfaenger-E-Mail und fuege mindestens eine "
              "anstehende Frist hinzu, um den Versand zu aktivieren.",
        "fr": "Enregistrez une adresse destinataire et ajoutez au moins "
              "une échéance imminente pour activer l'envoi.",
        "es": "Guarda un email destinatario y añade al menos un "
              "vencimiento próximo para habilitar el envío.",
    },
    "mailto_help": {
        "it": "Inserisci il destinatario; 'Invia ora' apre l'app email del "
              "telefono con oggetto e testo gia' compilati.",
        "en": "Enter the recipient; 'Send now' opens your phone's email app "
              "with subject and body already filled in.",
        "de": "Empfaenger eingeben; 'Jetzt senden' oeffnet die E-Mail-App des "
              "Telefons mit ausgefuelltem Betreff und Text.",
        "fr": "Entrez le destinataire; 'Envoyer' ouvre l'app email du "
              "téléphone avec l'objet et le texte préremplis.",
        "es": "Ingresa el destinatario; 'Enviar ahora' abre la app de email "
              "del teléfono con asunto y cuerpo precompletados.",
    },
    "phone_run_hint": {
        "it": "Per accedere dal telefono avvia con:\n"
              "flet run --web --port 8000 --host 0.0.0.0 mobile/app.py\n"
              "poi inquadra il QR (richiede stessa rete Wi-Fi).",
        "en": "To open from your phone, run:\n"
              "flet run --web --port 8000 --host 0.0.0.0 mobile/app.py\n"
              "then scan the QR (same Wi-Fi network required).",
        "de": "Zum Oeffnen vom Handy starten mit:\n"
              "flet run --web --port 8000 --host 0.0.0.0 mobile/app.py\n"
              "dann QR scannen (gleiches WLAN noetig).",
        "fr": "Pour ouvrir depuis le téléphone, lancez:\n"
              "flet run --web --port 8000 --host 0.0.0.0 mobile/app.py\n"
              "puis scannez le QR (même réseau Wi-Fi requis).",
        "es": "Para abrir desde el móvil, ejecuta:\n"
              "flet run --web --port 8000 --host 0.0.0.0 mobile/app.py\n"
              "luego escanea el QR (misma red Wi-Fi).",
    },
    "map_radius": {
        "it": "Raggio (km)", "en": "Radius (km)", "de": "Radius (km)",
        "fr": "Rayon (km)", "es": "Radio (km)",
    },
    "map_search_pois": {
        "it": "Cerca POI camper",
        "en": "Search camper POIs",
        "de": "Wohnmobil-POI suchen",
        "fr": "Chercher POI camping-car",
        "es": "Buscar POI camper",
    },
    "map_searching": {
        "it": "Ricerca in corso…", "en": "Searching…",
        "de": "Suche läuft…", "fr": "Recherche…", "es": "Buscando…",
    },
    "map_results_for": {
        "it": "Risultati vicini a", "en": "Results near",
        "de": "Ergebnisse in der Nähe von", "fr": "Résultats près de",
        "es": "Resultados cerca de",
    },
    "map_no_results": {
        "it": "Nessun POI trovato in questa zona.",
        "en": "No POIs found in this area.",
        "de": "Keine POIs in diesem Gebiet gefunden.",
        "fr": "Aucun POI trouvé dans cette zone.",
        "es": "No se encontraron POI en esta zona.",
    },
    "map_geocode_failed": {
        "it": "Luogo non trovato. Prova con città o indirizzo più completo.",
        "en": "Location not found. Try a city or fuller address.",
        "de": "Ort nicht gefunden. Versuche es mit Stadt oder Adresse.",
        "fr": "Lieu introuvable. Essayez avec une ville ou adresse complète.",
        "es": "Lugar no encontrado. Prueba con ciudad o dirección completa.",
    },
    "map_network_error": {
        "it": "Errore di rete contattando OpenStreetMap. Riprova tra poco.",
        "en": "Network error contacting OpenStreetMap. Try again shortly.",
        "de": "Netzwerkfehler bei OpenStreetMap. Bitte später erneut versuchen.",
        "fr": "Erreur réseau avec OpenStreetMap. Réessayez plus tard.",
        "es": "Error de red con OpenStreetMap. Inténtalo de nuevo.",
    },
    "map_open_in_maps": {
        "it": "Apri in Maps", "en": "Open in Maps",
        "de": "In Maps öffnen", "fr": "Ouvrir dans Maps",
        "es": "Abrir en Maps",
    },
    "map_call": {
        "it": "Chiama", "en": "Call", "de": "Anrufen",
        "fr": "Appeler", "es": "Llamar",
    },
    "map_website": {
        "it": "Sito", "en": "Website", "de": "Website",
        "fr": "Site", "es": "Sitio",
    },
    "map_filters": {
        "it": "Tipi di POI", "en": "POI types", "de": "POI-Typen",
        "fr": "Types de POI", "es": "Tipos de POI",
    },
    "map_fee_yes": {
        "it": "A pagamento", "en": "Paid", "de": "Kostenpflichtig",
        "fr": "Payant", "es": "De pago",
    },
    "map_fee_no": {
        "it": "Gratuito", "en": "Free", "de": "Kostenlos",
        "fr": "Gratuit", "es": "Gratis",
    },
    "map_unnamed": {
        "it": "(senza nome)", "en": "(unnamed)", "de": "(ohne Namen)",
        "fr": "(sans nom)", "es": "(sin nombre)",
    },
}


# Chiavi dei tipi scadenza — come nel file Streamlit, restano consistenti tra le due app.
TIPI_SCADENZA_KEYS = [
    "tipo_revisione", "tipo_vignetta", "tipo_assicurazione",
    "tipo_bombole", "tipo_tagliando", "tipo_bollo", "tipo_altro",
]

CATEGORIE_INTERVENTO_KEYS = [
    "int_revisione", "int_tagliando", "int_gomme", "int_freni",
    "int_elettrico", "int_idraulico", "int_carrozzeria",
    "int_motore", "int_altro",
]

CHECKLIST_CAT_KEYS = ["cat_partenza", "cat_apertura",
                      "cat_chiusura", "cat_manutenzione"]

TIPI_DOCUMENTI_KEYS = ["doc_libretto", "doc_assicurazione", "doc_revisione",
                       "doc_bollo", "doc_ricevuta", "doc_manuale",
                       "doc_foto", "doc_altro"]


# ============================================================
# Stato globale UI
# ============================================================
class AppState:
    def __init__(self):
        self.current_page = "home"
        self.page: ft.Page | None = None
        self.refresh_fn = None  # impostato da main()
        self.file_picker: ft.FilePicker | None = None  # impostato da main()
        self.url_launcher: ft.UrlLauncher | None = None  # impostato da main()
        # Stato locale per pagine multi-step (checklist, stats, map):
        # mantenuto qui perche' render_page() ricostruisce le pagine da zero.
        self.chk_cid: int | None = None
        self.chk_cat: str = CHECKLIST_CAT_KEYS[0]
        self.stats_cid: int | None = None  # None = tutti i camper
        # Stato pagina mappa
        self.map_query: str = ""
        self.map_radius_km: int = 25
        self.map_types: set[str] = {"caravan_site", "sanitary_dump", "camp_site"}
        self.map_results: list[dict] = []
        self.map_results_label: str = ""  # "Torino, Piemonte, Italia"
        self.map_error_key: str | None = None  # chiave di _MOBILE_LABELS
        self.map_loading: bool = False
        # Meteo della posizione cercata sulla mappa
        self.map_weather: dict | None = None
        self.map_weather_err: str | None = None
        # Auto-refresh: mtime dell'ultimo camper.json visto. Il task watcher
        # in main() ricarica la pagina se l'altra app (desktop) ha salvato.
        self.last_db_mtime: float = 0.0
        self.reload()

    def reload(self):
        db = storage.load()
        self.lang = db["impostazioni"].get("lingua", "it")
        self.valuta = db["impostazioni"].get("valuta", "EUR")
        self.soglia = db["impostazioni"].get("giorni_promemoria", 30)
        self.theme = db["impostazioni"].get("tema", "system")

    def apply_theme(self):
        if self.page is None:
            return
        mode = {
            "light": ft.ThemeMode.LIGHT,
            "dark": ft.ThemeMode.DARK,
        }.get(self.theme, ft.ThemeMode.SYSTEM)
        self.page.theme_mode = mode
        self.page.update()

    def t(self, key, **kwargs):
        m = _MOBILE_LABELS.get(key)
        if m is not None:
            return m.get(self.lang, m["it"])
        kwargs.setdefault("sym", storage.currency_symbol(self.valuta))
        return _t(key, self.lang, **kwargs)

    def money(self, amount, decimals=2):
        return storage.fmt_money(amount, self.valuta, decimals=decimals)

    def refresh(self):
        if self.refresh_fn:
            self.refresh_fn()

    def snack(self, msg: str, error: bool = False):
        if self.page is None:
            return
        sb = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=ft.Colors.ERROR_CONTAINER if error else None,
            open=True,
        )
        self.page.overlay.append(sb)
        self.page.update()


# Registro pagine: (codice, icona_off, icona_on, chiave_label_traduzione)
PAGES = [
    ("home", ft.Icons.HOME_OUTLINED, ft.Icons.HOME, "page_home"),
    ("campers", ft.Icons.AIRPORT_SHUTTLE_OUTLINED, ft.Icons.AIRPORT_SHUTTLE, "page_campers"),
    ("deadlines", ft.Icons.ALARM_OUTLINED, ft.Icons.ALARM, "page_deadlines"),
    ("logbook", ft.Icons.BUILD_OUTLINED, ft.Icons.BUILD, "page_logbook"),
    ("trips", ft.Icons.LUGGAGE_OUTLINED, ft.Icons.LUGGAGE, "page_trips"),
    ("map", ft.Icons.MAP_OUTLINED, ft.Icons.MAP, "page_map"),
    ("fuel", ft.Icons.LOCAL_GAS_STATION_OUTLINED, ft.Icons.LOCAL_GAS_STATION, "page_fuel"),
    ("checklist", ft.Icons.CHECKLIST_OUTLINED, ft.Icons.CHECKLIST, "page_checklist"),
    ("documents", ft.Icons.FOLDER_OUTLINED, ft.Icons.FOLDER, "page_documents"),
    ("stats", ft.Icons.BAR_CHART_OUTLINED, ft.Icons.BAR_CHART, "page_stats"),
    ("settings", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS, "page_settings"),
]

# 4 tab veloci in basso + 5a tab "Altro" che apre il drawer con tutte le pagine.
QUICK_TABS = ["home", "campers", "deadlines", "map"]


# ============================================================
# Helper UI
# ============================================================
def _strip_emoji(label: str) -> str:
    parts = label.split(" ", 1)
    return parts[1] if len(parts) == 2 else label


def _metric_card(label, value, icon):
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=ft.Colors.PRIMARY, size=28),
            ft.Column([
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(label, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2, tight=True),
        ], spacing=10),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        width=160,
    )


def _info_box(text, icon, icon_color=None, bgcolor=None):
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=icon_color or ft.Colors.PRIMARY),
            ft.Text(text, expand=True),
        ], spacing=10),
        padding=12,
        bgcolor=bgcolor or ft.Colors.SECONDARY_CONTAINER,
        border_radius=10,
    )


def _scrollable(children):
    return ft.ListView(controls=children, spacing=12, padding=12, expand=True)


def _swipeable(state: "AppState", content: ft.Control,
               on_swiped) -> ft.Control:
    """Avvolge una card in Dismissible: swipe destra→sinistra per cancellare.
    Mostra background rosso con icona cestino. on_swiped() riceve niente
    e tipicamente apre il dialog di conferma (state.refresh ricostruisce
    la card se l'utente annulla)."""
    bg = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.DELETE, color=ft.Colors.ON_ERROR),
        ], alignment=ft.MainAxisAlignment.END),
        bgcolor=ft.Colors.ERROR,
        padding=ft.Padding.only(right=20),
        border_radius=10,
    )

    def _on_dismiss(e):
        on_swiped()

    return ft.Dismissible(
        content=content,
        background=bg,
        dismiss_direction=ft.DismissDirection.END_TO_START,
        on_dismiss=_on_dismiss,
    )


def _confirm_delete(state: "AppState", label: str, on_confirm) -> None:
    """Dialog di conferma eliminazione: on_confirm() esegue la cancellazione,
    poi pop_dialog + state.refresh. Annulla = solo refresh (chiude dialog
    e ricostruisce la lista, utile dopo uno swipe del Dismissible)."""
    page = state.page
    if page is None:
        return
    L = state.t

    def yes(e):
        on_confirm()
        page.pop_dialog()
        state.refresh()

    def no(e):
        page.pop_dialog()
        state.refresh()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(L("delete") + " ?"),
        content=ft.Text(label),
        actions=[
            ft.TextButton(L("cancel"), on_click=no),
            ft.FilledButton(L("delete"), on_click=yes),
        ],
    ))


class DateField:
    """Bottone con label + data corrente che apre un DatePicker nativo."""

    def __init__(self, page: ft.Page, label: str, initial: date):
        self.page = page
        self.label = label
        self._value: date = initial
        self.control = ft.OutlinedButton(
            content=self._fmt(),
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self._open,
        )

    @property
    def value(self) -> date:
        return self._value

    def _fmt(self) -> str:
        return f"{self.label}: {self._value.strftime('%d/%m/%Y')}"

    def _open(self, e):
        dp = ft.DatePicker(
            value=self._value,
            first_date=date(2000, 1, 1),
            last_date=date(2099, 12, 31),
            on_change=self._on_change,
        )
        self.page.show_dialog(dp)

    def _on_change(self, e):
        v = e.control.value
        # Flet puo' passare datetime: estraiamo la data.
        self._value = v.date() if hasattr(v, "date") else v
        self.control.content = self._fmt()
        self.page.update()


# ============================================================
# Pagina HOME
# ============================================================
def build_home(state: AppState) -> ft.Control:
    db = storage.load()
    soglia = db["impostazioni"]["giorni_promemoria"]
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = []

    hero_path = ROOT / "assets" / "hero.jpg"
    if hero_path.exists():
        children.append(ft.Image(
            src=str(hero_path), fit=ft.BoxFit.COVER, height=160,
            border_radius=12,
        ))

    children.append(ft.Text(L("welcome"), size=24, weight=ft.FontWeight.BOLD))

    metrics = [
        (L("campers"), str(len(db["campers"])), ft.Icons.AIRPORT_SHUTTLE),
        (L("deadlines"), str(len(db["scadenze"])), ft.Icons.ALARM),
        (L("interventions"), str(len(db["interventi"])), ft.Icons.BUILD),
        (L("trips"), str(len(db["viaggi"])), ft.Icons.LUGGAGE),
    ]
    children.append(ft.Row(
        [_metric_card(*m) for m in metrics],
        wrap=True, spacing=8, run_spacing=8,
    ))

    children.append(ft.Divider())

    if not db["campers"]:
        children.append(_info_box(L("start_add_camper"), ft.Icons.INFO))
        return _scrollable(children)

    # Scadenze imminenti
    children.append(ft.Text(
        L("deadlines_within_days", n=soglia),
        size=18, weight=ft.FontWeight.W_600,
    ))
    imminenti = []
    for s in db["scadenze"]:
        d = date.fromisoformat(s["data"])
        giorni = (d - date.today()).days
        if giorni <= soglia:
            imminenti.append((giorni, s, d))
    imminenti.sort(key=lambda x: x[0])
    if not imminenti:
        children.append(_info_box(
            L("no_upcoming"), ft.Icons.CHECK_CIRCLE,
            icon_color=ft.Colors.GREEN, bgcolor=ft.Colors.GREEN_50,
        ))
    else:
        for giorni, s, d in imminenti:
            when = (L("expired_for_days", n=-giorni) if giorni < 0
                    else L("in_n_days", n=giorni))
            color = ft.Colors.RED_400 if giorni < 0 else ft.Colors.ORANGE_400
            icon = ft.Icons.ERROR if giorni < 0 else ft.Icons.WARNING
            children.append(ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=color),
                    ft.Column([
                        ft.Text(s["tipo"], weight=ft.FontWeight.BOLD),
                        ft.Text(
                            f"{cmap.get(s['camper_id'], '?')} - "
                            f"{d.strftime('%d/%m/%Y')} - {when}",
                            size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ], spacing=2, tight=True, expand=True),
                ], spacing=10),
                padding=12,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=10,
            ))

    children.append(ft.Divider())

    # Costi totali per camper
    children.append(ft.Text(
        L("total_costs_per_camper"),
        size=18, weight=ft.FontWeight.W_600,
    ))
    for c in db["campers"]:
        cid = c["id"]
        tot_int = sum(i["costo"] for i in db["interventi"] if i["camper_id"] == cid)
        tot_rif = sum(r["costo"] for r in db["rifornimenti"] if r["camper_id"] == cid)
        tot_via = sum(v["costo"] for v in db["viaggi"] if v["camper_id"] == cid)
        totale = tot_int + tot_rif + tot_via
        km_percorsi = max(0, c["km"] - c.get("km_iniziale", c["km"]))
        eur_km = (totale / km_percorsi) if km_percorsi > 0 else None
        rows_in_card = [
            (L("maintenance"), state.money(tot_int)),
            (L("fuel_label"), state.money(tot_rif)),
            (L("trips_label"), state.money(tot_via)),
            (L("total"), state.money(totale)),
            (L("km_owned"), f"{km_percorsi:,}".replace(",", ".")),
            (L("eur_per_km"),
             state.money(eur_km, decimals=3) if eur_km is not None else "—"),
        ]
        children.append(ft.Container(
            content=ft.Column([
                ft.Text(f"{c['marca']} {c['modello']}",
                        weight=ft.FontWeight.BOLD, size=15),
                *[ft.Row([
                    ft.Text(k, color=ft.Colors.ON_SURFACE_VARIANT, expand=True),
                    ft.Text(v, weight=ft.FontWeight.W_500),
                ]) for k, v in rows_in_card],
            ], spacing=4, tight=True),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))
    children.append(ft.Text(
        L("eur_per_km_help"), size=11,
        color=ft.Colors.ON_SURFACE_VARIANT, italic=True,
    ))

    # Banner affiliato Acronis: stesso annuncio CJ della landing page.
    async def open_acronis(e):
        if state.url_launcher is not None:
            await state.url_launcher.launch_url(affiliates.acronis_banner_url())

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("ad_label").upper(), size=10,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text("Acronis Cyber Protect",
                    weight=ft.FontWeight.BOLD, size=15),
            ft.Text(L("ad_acronis_desc"), size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            ft.FilledButton(L("ad_learn_more"), icon=ft.Icons.OPEN_IN_NEW,
                            on_click=open_acronis),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    return _scrollable(children)


# ============================================================
# Pagina CAMPER
# ============================================================
def build_campers(state: AppState) -> ft.Control:
    db = storage.load()
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(L("my_campers"), size=22, weight=ft.FontWeight.BOLD,
                    expand=True),
            ft.FilledButton(
                _strip_emoji(L("add_camper")),
                icon=ft.Icons.ADD,
                on_click=lambda e: _open_add_camper_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if not db["campers"]:
        children.append(ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.AIRPORT_SHUTTLE_OUTLINED, size=64,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(L("no_camper_yet"),
                        color=ft.Colors.ON_SURFACE_VARIANT),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=24,
            alignment=ft.Alignment.CENTER,
        ))
        return _scrollable(children)

    for c in db["campers"]:
        children.append(_camper_card(state, c))

    return _scrollable(children)


def _camper_card(state: AppState, c: dict) -> ft.Control:
    L = state.t
    km_str = f"{c['km']:,}".replace(",", ".")
    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(f"{c['marca']} {c['modello']}",
                        weight=ft.FontWeight.BOLD, size=16),
                ft.Text(f"{c['anno']} - {c['targa']} - {km_str} km",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=2, tight=True, expand=True),
            ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                tooltip=L("update_km"),
                on_click=lambda e, cid=c["id"]:
                    _open_edit_camper_dialog(state, cid),
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.ERROR,
                tooltip=L("delete"),
                on_click=lambda e, cid=c["id"],
                          name=f"{c['marca']} {c['modello']}":
                    _confirm_delete(state, name,
                                    lambda: storage.delete_camper(cid)),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    )


def _open_add_camper_dialog(state: AppState) -> None:
    page = state.page
    if page is None:
        return
    L = state.t

    f_marca = ft.TextField(label=L("brand"), autofocus=True)
    f_modello = ft.TextField(label=L("model"))
    f_anno = ft.TextField(label=L("year"), value="2018",
                          keyboard_type=ft.KeyboardType.NUMBER)
    f_targa = ft.TextField(label=L("plate"),
                           capitalization=ft.TextCapitalization.CHARACTERS)
    f_km = ft.TextField(label=L("current_km"), value="50000",
                        keyboard_type=ft.KeyboardType.NUMBER)
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    def save(e):
        if not (f_marca.value and f_modello.value and f_targa.value):
            err.value = L("fill_required")
            err.visible = True
            page.update()
            return
        try:
            anno = int(f_anno.value or 0)
            km = int(f_km.value or 0)
        except ValueError:
            err.value = L("fill_required")
            err.visible = True
            page.update()
            return
        storage.add_camper(
            f_marca.value.strip(), f_modello.value.strip(),
            anno, f_targa.value.strip(), km,
        )
        page.pop_dialog()
        state.refresh()

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("add_camper"))),
        content=ft.Container(width=320, content=ft.Column([
            f_marca, f_modello, f_anno, f_targa, f_km,
            ft.Text(L("km_iniziale_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save_camper"), on_click=save),
        ],
    ))


def _open_edit_camper_dialog(state: AppState, camper_id: int) -> None:
    page = state.page
    if page is None:
        return
    L = state.t
    db = storage.load()
    c = next((x for x in db["campers"] if x["id"] == camper_id), None)
    if c is None:
        return

    f_km = ft.TextField(label=L("update_km"), value=str(c["km"]),
                        keyboard_type=ft.KeyboardType.NUMBER, autofocus=True)
    f_km_init = ft.TextField(
        label=L("km_iniziale_label"),
        value=str(c.get("km_iniziale", c["km"])),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def save(e):
        try:
            km = int(f_km.value or 0)
            km_init = int(f_km_init.value or 0)
        except ValueError:
            return
        storage.update_camper_km(camper_id, km)
        storage.update_camper_km_iniziale(camper_id, km_init)
        page.pop_dialog()
        state.refresh()

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(f"{c['marca']} {c['modello']}"),
        content=ft.Container(width=320, content=ft.Column([
            f_km, f_km_init,
            ft.Text(L("km_iniziale_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
        ], tight=True, spacing=10)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save"), on_click=save),
        ],
    ))


# ============================================================
# Pagina SCADENZE
# ============================================================
def _parse_it_date(s: str) -> date | None:
    """Accetta GG/MM/AAAA, GG-MM-AAAA o ISO AAAA-MM-GG."""
    if not s:
        return None
    s = s.strip().replace(".", "/").replace("-", "/")
    parts = s.split("/")
    try:
        if len(parts) == 3:
            a, b, c = parts
            if len(a) == 4:  # ISO
                return date(int(a), int(b), int(c))
            return date(int(c), int(b), int(a))
    except ValueError:
        return None
    return None


def _scadenza_status(giorni: int, soglia: int) -> tuple[str, str, str]:
    """Ritorna (chiave_label, colore, icona) per la scadenza."""
    if giorni < 0:
        return "expired", ft.Colors.RED_400, ft.Icons.ERROR
    if giorni <= soglia:
        return "upcoming", ft.Colors.ORANGE_400, ft.Icons.WARNING
    return "ok", ft.Colors.GREEN_500, ft.Icons.CHECK_CIRCLE


def build_deadlines(state: AppState) -> ft.Control:
    db = storage.load()
    soglia = db["impostazioni"]["giorni_promemoria"]
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(L("upcoming_deadlines"), size=22,
                    weight=ft.FontWeight.BOLD, expand=True),
            ft.FilledButton(
                _strip_emoji(L("add_deadline")),
                icon=ft.Icons.ADD,
                on_click=lambda e: _open_add_scadenza_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if not db["scadenze"]:
        children.append(_info_box(L("no_deadline"), ft.Icons.INFO))
        return _scrollable(children)

    rows = []
    for s in db["scadenze"]:
        d = date.fromisoformat(s["data"])
        giorni = (d - date.today()).days
        rows.append((giorni, s, d))
    rows.sort(key=lambda r: r[0])

    for giorni, s, d in rows:
        status_key, color, icon = _scadenza_status(giorni, soglia)
        when = (L("expired_for_days", n=-giorni) if giorni < 0
                else L("in_n_days", n=giorni))
        sub_lines = [
            ft.Text(
                f"{cmap.get(s['camper_id'], '?')} - "
                f"{d.strftime('%d/%m/%Y')} - {when}",
                size=12, color=ft.Colors.ON_SURFACE_VARIANT,
            ),
        ]
        if s.get("note"):
            sub_lines.append(ft.Text(
                s["note"], size=12, italic=True,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ))
        children.append(ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color),
                ft.Column([
                    ft.Row([
                        ft.Text(s["tipo"], weight=ft.FontWeight.BOLD,
                                expand=True),
                        ft.Container(
                            content=ft.Text(L(status_key), size=11,
                                            color=ft.Colors.ON_PRIMARY),
                            bgcolor=color, padding=ft.Padding.symmetric(
                                horizontal=8, vertical=2),
                            border_radius=10,
                        ),
                    ]),
                    *sub_lines,
                ], spacing=2, tight=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    tooltip=L("delete"),
                    on_click=lambda e, sid=s["id"],
                              label=f"{s['tipo']} - {d.strftime('%d/%m/%Y')}":
                        _confirm_delete(state, label,
                                        lambda: storage.delete_scadenza(sid)),
                ),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))

    return _scrollable(children)


def _open_add_scadenza_dialog(state: AppState) -> None:
    page = state.page
    if page is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(_strip_emoji(L("add_deadline"))),
            content=ft.Text(L("select_camper_first")),
            actions=[ft.TextButton(L("cancel"),
                                   on_click=lambda e: page.pop_dialog())],
        ))
        return

    # Camper dropdown — primo selezionato di default.
    camper_options = [
        ft.dropdown.Option(key=str(c["id"]),
                           text=f"{c['marca']} {c['modello']} ({c['targa']})")
        for c in db["campers"]
    ]
    f_camper = ft.Dropdown(
        label=L("camper"), options=camper_options,
        value=str(db["campers"][0]["id"]),
    )

    tipi_labels = [_t(k, state.lang) for k in TIPI_SCADENZA_KEYS]
    f_tipo = ft.Dropdown(
        label=L("type"),
        options=[ft.dropdown.Option(key=lbl, text=lbl) for lbl in tipi_labels],
        value=tipi_labels[0],
    )

    f_data = DateField(page, L("deadline_date"),
                       date.today() + timedelta(days=30))
    f_note = ft.TextField(label=L("notes_optional"))
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    def save(e):
        if f_camper.value is None:
            err.value = L("select_camper_error")
            err.visible = True
            page.update()
            return
        storage.add_scadenza(
            int(f_camper.value), f_tipo.value, f_data.value,
            (f_note.value or "").strip(),
        )
        page.pop_dialog()
        state.refresh()
        state.snack(L("deadline_added"))

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("add_deadline"))),
        content=ft.Container(width=320, content=ft.Column([
            f_camper, f_tipo, f_data.control, f_note, err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save_deadline"), on_click=save),
        ],
    ))


# ============================================================
# Pagina LIBRETTO (interventi)
# ============================================================
def _parse_decimal(s: str) -> float | None:
    """Accetta sia '10.50' che '10,50'."""
    if s is None:
        return None
    s = s.strip().replace(",", ".")
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return None


def _parse_int(s: str) -> int | None:
    if s is None:
        return None
    s = s.strip().replace(".", "").replace(" ", "")
    if not s:
        return 0
    try:
        return int(s)
    except ValueError:
        return None


def build_logbook(state: AppState) -> ft.Control:
    db = storage.load()
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(_strip_emoji(L("page_logbook")), size=22,
                    weight=ft.FontWeight.BOLD, expand=True),
            ft.FilledButton(
                _strip_emoji(L("add_intervention")),
                icon=ft.Icons.ADD,
                on_click=lambda e: _open_add_intervento_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if db["campers"]:
        children.append(ft.OutlinedButton(
            L("export_pdf_logbook"),
            icon=ft.Icons.PICTURE_AS_PDF,
            on_click=lambda e: _open_export_pdf_dialog(state),
        ))

    if not db["interventi"]:
        children.append(_info_box(L("no_intervention"), ft.Icons.INFO))
        return _scrollable(children)

    totale = sum(i["costo"] for i in db["interventi"])
    children.append(_info_box(
        f"{L('total_maintenance')}: {state.money(totale)}",
        ft.Icons.PAID,
    ))

    interventi = sorted(db["interventi"], key=lambda x: x["data"], reverse=True)
    for i in interventi:
        d = date.fromisoformat(i["data"])
        cat_label = L(i.get("categoria", "int_altro"))
        km_str = f"{i['km']:,}".replace(",", ".")
        children.append(ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.BUILD, color=ft.Colors.PRIMARY),
                ft.Column([
                    ft.Row([
                        ft.Text(i["descrizione"], weight=ft.FontWeight.BOLD,
                                expand=True, max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(state.money(i["costo"]),
                                weight=ft.FontWeight.W_500),
                    ]),
                    ft.Text(
                        f"{cmap.get(i['camper_id'], '?')} - "
                        f"{d.strftime('%d/%m/%Y')} - "
                        f"{cat_label} - {km_str} km",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ], spacing=2, tight=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    tooltip=L("delete"),
                    on_click=lambda e, iid=i["id"],
                              label=f"{i['descrizione'][:40]} - "
                                    f"{d.strftime('%d/%m/%Y')}":
                        _confirm_delete(state, label,
                                        lambda: storage.delete_intervento(iid)),
                ),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))

    return _scrollable(children)


def _open_add_intervento_dialog(state: AppState) -> None:
    page = state.page
    if page is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(_strip_emoji(L("add_intervention"))),
            content=ft.Text(L("select_camper_first")),
            actions=[ft.TextButton(L("cancel"),
                                   on_click=lambda e: page.pop_dialog())],
        ))
        return

    f_camper = ft.Dropdown(
        label=L("camper"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(db["campers"][0]["id"]),
    )

    f_cat = ft.Dropdown(
        label=L("category"),
        options=[ft.dropdown.Option(key=k, text=L(k))
                 for k in CATEGORIE_INTERVENTO_KEYS],
        value="int_altro",
    )

    f_data = DateField(page, L("date"), date.today())
    f_km = ft.TextField(
        label=L("km"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_costo = ft.TextField(
        label=L("cost_eur"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_desc = ft.TextField(
        label=L("intervention_desc"),
        multiline=True, min_lines=2, max_lines=4,
    )
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    def show_err(msg: str):
        err.value = msg
        err.visible = True
        page.update()

    def save(e):
        if f_camper.value is None:
            show_err(L("select_camper_error"))
            return
        if not (f_desc.value or "").strip():
            show_err(L("fill_description"))
            return
        km = _parse_int(f_km.value or "0")
        costo = _parse_decimal(f_costo.value or "0")
        if km is None or costo is None:
            show_err(L("fill_required"))
            return
        storage.add_intervento(
            int(f_camper.value), f_data.value, f_desc.value.strip(),
            float(costo), int(km), categoria=f_cat.value or "int_altro",
        )
        page.pop_dialog()
        state.refresh()
        state.snack(L("intervention_saved"))

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("add_intervention"))),
        content=ft.Container(width=320, content=ft.Column([
            f_camper, f_cat, f_data.control, f_km, f_costo, f_desc, err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save_intervention"), on_click=save),
        ],
    ))


def _open_export_pdf_dialog(state: AppState) -> None:
    page = state.page
    if page is None or state.file_picker is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        return

    f_camper = ft.Dropdown(
        label=L("camper_to_export"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(db["campers"][0]["id"]),
    )

    async def do_export(e):
        cid = int(f_camper.value)
        camper = next(c for c in db["campers"] if c["id"] == cid)
        from pdf_export import build_libretto_pdf
        try:
            data = build_libretto_pdf(db, cid, state.lang, state.valuta)
        except Exception as ex:
            page.pop_dialog()
            state.snack(str(ex), error=True)
            return

        safe_name = (
            f"{camper['marca']}_{camper['modello']}"
            .replace(" ", "_").replace("/", "-")
        )
        fname = f"libretto_{safe_name}.pdf"

        def on_result(ev: ft.FilePickerResultEvent):
            if not ev.path:
                return
            try:
                Path(ev.path).write_bytes(data)
                state.snack(L("export_pdf_logbook") + " ✓")
            except OSError as oex:
                state.snack(str(oex), error=True)

        state.file_picker.on_result = on_result
        page.pop_dialog()
        await state.file_picker.save_file(
            file_name=fname, allowed_extensions=["pdf"],
        )

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(L("export_pdf_logbook")),
        content=ft.Container(width=320, content=ft.Column([
            f_camper,
        ], tight=True, spacing=10)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("download_pdf"), on_click=do_export),
        ],
    ))


# ============================================================
# Pagina VIAGGI
# ============================================================
def build_trips(state: AppState) -> ft.Control:
    db = storage.load()
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(L("trip_diary_title"), size=22,
                    weight=ft.FontWeight.BOLD, expand=True),
            ft.FilledButton(
                _strip_emoji(L("add_trip")),
                icon=ft.Icons.ADD,
                on_click=lambda e: _open_add_viaggio_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if not db["viaggi"]:
        children.append(_info_box(L("no_trip"), ft.Icons.INFO))
        return _scrollable(children)

    n_viaggi = len(db["viaggi"])
    tot_km = sum(v["km_percorsi"] for v in db["viaggi"])
    tot_costo = sum(v["costo"] for v in db["viaggi"])
    children.append(ft.Row([
        _metric_card(L("total_trips"), str(n_viaggi), ft.Icons.LUGGAGE),
        _metric_card(L("total_km"),
                     f"{tot_km:,}".replace(",", "."), ft.Icons.ROUTE),
        _metric_card(L("total_trip_spending"),
                     state.money(tot_costo), ft.Icons.PAID),
    ], wrap=True, spacing=8, run_spacing=8))

    viaggi = sorted(db["viaggi"], key=lambda x: x["data_inizio"], reverse=True)
    for v in viaggi:
        di = date.fromisoformat(v["data_inizio"])
        df_ = date.fromisoformat(v["data_fine"])
        durata = (df_ - di).days + 1
        km_str = f"{v['km_percorsi']:,}".replace(",", ".")
        sub_lines = [
            ft.Text(
                f"{cmap.get(v['camper_id'], '?')} - "
                f"{di.strftime('%d/%m/%Y')} → {df_.strftime('%d/%m/%Y')} "
                f"({durata} {L('days').lower()}) - "
                f"{km_str} km",
                size=12, color=ft.Colors.ON_SURFACE_VARIANT,
            ),
        ]
        if v.get("note"):
            sub_lines.append(ft.Text(
                v["note"], size=12, italic=True,
                color=ft.Colors.ON_SURFACE_VARIANT,
                max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
            ))
        children.append(ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LUGGAGE, color=ft.Colors.PRIMARY),
                ft.Column([
                    ft.Row([
                        ft.Text(v["destinazione"], weight=ft.FontWeight.BOLD,
                                expand=True, max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(state.money(v["costo"]),
                                weight=ft.FontWeight.W_500),
                    ]),
                    *sub_lines,
                ], spacing=2, tight=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    tooltip=L("delete"),
                    on_click=lambda e, vid=v["id"],
                              label=f"{v['destinazione']} - "
                                    f"{di.strftime('%d/%m/%Y')}":
                        _confirm_delete(state, label,
                                        lambda: storage.delete_viaggio(vid)),
                ),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))

    return _scrollable(children)


def _open_add_viaggio_dialog(state: AppState) -> None:
    page = state.page
    if page is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(_strip_emoji(L("add_trip"))),
            content=ft.Text(L("select_camper_first")),
            actions=[ft.TextButton(L("cancel"),
                                   on_click=lambda e: page.pop_dialog())],
        ))
        return

    f_camper = ft.Dropdown(
        label=L("camper"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(db["campers"][0]["id"]),
    )
    f_dest = ft.TextField(label=L("destination"))
    f_inizio = DateField(page, L("departure_date"), date.today())
    f_fine = DateField(page, L("return_date"),
                       date.today() + timedelta(days=3))
    f_km = ft.TextField(
        label=L("km_done"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_costo = ft.TextField(
        label=L("total_cost_eur"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_note = ft.TextField(
        label=L("notes"), multiline=True, min_lines=2, max_lines=4,
    )
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    def show_err(msg: str):
        err.value = msg
        err.visible = True
        page.update()

    def save(e):
        if f_camper.value is None:
            show_err(L("select_camper_error"))
            return
        if not (f_dest.value or "").strip():
            show_err(L("fill_destination"))
            return
        if f_fine.value < f_inizio.value:
            show_err(L("return_before_departure"))
            return
        km = _parse_int(f_km.value or "0")
        costo = _parse_decimal(f_costo.value or "0")
        if km is None or costo is None:
            show_err(L("fill_required"))
            return
        storage.add_viaggio(
            int(f_camper.value), f_inizio.value, f_fine.value,
            f_dest.value.strip(), int(km), float(costo),
            (f_note.value or "").strip(),
        )
        page.pop_dialog()
        state.refresh()
        state.snack(L("trip_saved"))

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("add_trip"))),
        content=ft.Container(width=320, content=ft.Column([
            f_camper, f_dest, f_inizio.control, f_fine.control,
            f_km, f_costo, f_note, err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save_trip"), on_click=save),
        ],
    ))


# ============================================================
# Pagina RIFORNIMENTI (fuel)
# ============================================================
def _consumo_per_id(db: dict) -> dict[int, str]:
    """Per ogni rifornimento "pieno" calcola il consumo medio l/100km
    rispetto al pieno precedente (litri intermedi inclusi)."""
    out: dict[int, str] = {}
    for c in db["campers"]:
        rifs = sorted(
            [r for r in db["rifornimenti"] if r["camper_id"] == c["id"]],
            key=lambda x: x["km"],
        )
        prev_pieno_km = None
        litri_dal_pieno = 0.0
        for r in rifs:
            pieno = r.get("pieno", True)
            litri_dal_pieno += r["litri"]
            if pieno and prev_pieno_km is not None and r["km"] > prev_pieno_km:
                delta_km = r["km"] - prev_pieno_km
                out[r["id"]] = f"{(litri_dal_pieno / delta_km) * 100:.1f}"
            if pieno:
                prev_pieno_km = r["km"]
                litri_dal_pieno = 0.0
    return out


def _media_consumo(db: dict, camper_id: int) -> tuple[float | None, int]:
    """Media tra primo e ultimo pieno (escluso il primo dal totale litri)."""
    rifs = sorted(
        [r for r in db["rifornimenti"] if r["camper_id"] == camper_id],
        key=lambda x: x["km"],
    )
    pieni = [(idx, r["km"]) for idx, r in enumerate(rifs)
             if r.get("pieno", True)]
    if len(pieni) < 2:
        return None, 0
    first_idx, first_km = pieni[0]
    last_idx, last_km = pieni[-1]
    tot_litri = sum(r["litri"] for r in rifs[first_idx + 1: last_idx + 1])
    tot_km = last_km - first_km
    if tot_km <= 0 or tot_litri <= 0:
        return None, 0
    return (tot_litri / tot_km) * 100, tot_km


def build_fuel(state: AppState) -> ft.Control:
    db = storage.load()
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(L("fuel_title"), size=22,
                    weight=ft.FontWeight.BOLD, expand=True),
            ft.FilledButton(
                _strip_emoji(L("add_fuel")),
                icon=ft.Icons.ADD,
                on_click=lambda e: _open_add_rifornimento_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if not db["rifornimenti"]:
        children.append(_info_box(L("no_fuel"), ft.Icons.INFO))
        return _scrollable(children)

    n_rif = len(db["rifornimenti"])
    tot_litri = sum(r["litri"] for r in db["rifornimenti"])
    tot_costo = sum(r["costo"] for r in db["rifornimenti"])
    children.append(ft.Row([
        _metric_card(_strip_emoji(L("page_fuel")), str(n_rif),
                     ft.Icons.LOCAL_GAS_STATION),
        _metric_card(L("liters"), f"{tot_litri:.0f}", ft.Icons.WATER_DROP),
        _metric_card(L("cost"), state.money(tot_costo), ft.Icons.PAID),
    ], wrap=True, spacing=8, run_spacing=8))

    # Consumo medio per camper
    medie_lines = []
    for c in db["campers"]:
        media, km = _media_consumo(db, c["id"])
        if media is not None:
            km_str = f"{km:,}".replace(",", ".")
            medie_lines.append(ft.Text(
                f"• {c['marca']} {c['modello']}: "
                f"{media:.1f} l/100km ({km_str} km)",
                size=12,
            ))
    if medie_lines:
        children.append(ft.Container(
            content=ft.Column([
                ft.Text(L("avg_consumption"), weight=ft.FontWeight.W_600),
                *medie_lines,
            ], spacing=4, tight=True),
            padding=12,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=10,
        ))

    consumi = _consumo_per_id(db)
    rifs = sorted(db["rifornimenti"], key=lambda x: x["data"], reverse=True)
    for r in rifs:
        d = date.fromisoformat(r["data"])
        km_str = f"{r['km']:,}".replace(",", ".")
        prezzo_l = r["costo"] / r["litri"] if r["litri"] > 0 else 0
        sym = storage.currency_symbol(state.valuta)
        pieno = r.get("pieno", True)
        consumo = consumi.get(r["id"])
        line2 = (
            f"{cmap.get(r['camper_id'], '?')} - "
            f"{d.strftime('%d/%m/%Y')} - {km_str} km"
        )
        line3_parts = [
            f"{r['litri']:.2f} L",
            f"{sym}{prezzo_l:.3f}/L",
        ]
        if r.get("distributore"):
            line3_parts.append(r["distributore"])
        if consumo:
            line3_parts.append(f"{consumo} l/100km")
        sub_lines = [
            ft.Text(line2, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(" - ".join(line3_parts), size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT),
        ]
        if r.get("note"):
            sub_lines.append(ft.Text(
                r["note"], size=12, italic=True,
                color=ft.Colors.ON_SURFACE_VARIANT,
                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
            ))
        title_row_children = [
            ft.Text(state.money(r["costo"]),
                    weight=ft.FontWeight.BOLD, expand=True),
        ]
        if pieno:
            title_row_children.append(ft.Container(
                content=ft.Text(L("full_tank_short"), size=11,
                                color=ft.Colors.ON_PRIMARY),
                bgcolor=ft.Colors.PRIMARY,
                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                border_radius=10,
            ))
        children.append(ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LOCAL_GAS_STATION, color=ft.Colors.PRIMARY),
                ft.Column([
                    ft.Row(title_row_children),
                    *sub_lines,
                ], spacing=2, tight=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    tooltip=L("delete"),
                    on_click=lambda e, rid=r["id"],
                              label=f"{d.strftime('%d/%m/%Y')} - "
                                    f"{r['litri']:.2f} L":
                        _confirm_delete(state, label,
                                        lambda: storage.delete_rifornimento(rid)),
                ),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))

    return _scrollable(children)


def _open_add_rifornimento_dialog(state: AppState) -> None:
    page = state.page
    if page is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(_strip_emoji(L("add_fuel"))),
            content=ft.Text(L("select_camper_first")),
            actions=[ft.TextButton(L("cancel"),
                                   on_click=lambda e: page.pop_dialog())],
        ))
        return

    f_camper = ft.Dropdown(
        label=L("camper"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(db["campers"][0]["id"]),
    )
    f_data = DateField(page, L("date"), date.today())
    f_km = ft.TextField(
        label=L("odometer_km"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_litri = ft.TextField(
        label=L("liters"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_costo = ft.TextField(
        label=L("total_cost_eur"), value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    f_dist = ft.TextField(label=L("station"))
    f_pieno = ft.Checkbox(label=L("full_tank"), value=True)
    f_note = ft.TextField(label=L("notes_optional"))
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    def show_err(msg: str):
        err.value = msg
        err.visible = True
        page.update()

    def save(e):
        if f_camper.value is None:
            show_err(L("select_camper_error"))
            return
        km = _parse_int(f_km.value or "0")
        litri = _parse_decimal(f_litri.value or "0")
        costo = _parse_decimal(f_costo.value or "0")
        if km is None or litri is None or costo is None:
            show_err(L("fill_km_liters"))
            return
        if litri <= 0 or km <= 0:
            show_err(L("fill_km_liters"))
            return
        storage.add_rifornimento(
            int(f_camper.value), f_data.value, int(km),
            float(litri), float(costo),
            (f_dist.value or "").strip(), (f_note.value or "").strip(),
            pieno=bool(f_pieno.value),
        )
        page.pop_dialog()
        state.refresh()
        state.snack(L("fuel_saved"))

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("add_fuel"))),
        content=ft.Container(width=320, content=ft.Column([
            f_camper, f_data.control, f_km, f_litri, f_costo, f_dist,
            f_pieno,
            ft.Text(L("full_tank_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            f_note, err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("save_fuel"), on_click=save),
        ],
    ))


# ============================================================
# Pagina CHECKLIST
# ============================================================
def build_checklist(state: AppState) -> ft.Control:
    db = storage.load()
    L = state.t

    children: list[ft.Control] = [
        ft.Text(L("checklist_title"), size=22, weight=ft.FontWeight.BOLD),
    ]

    if not db["campers"]:
        children.append(_info_box(L("select_camper_first"), ft.Icons.INFO))
        return _scrollable(children)

    # Inizializza camper di default se non gia' impostato o se eliminato.
    valid_ids = {c["id"] for c in db["campers"]}
    if state.chk_cid not in valid_ids:
        state.chk_cid = db["campers"][0]["id"]
    if state.chk_cat not in CHECKLIST_CAT_KEYS:
        state.chk_cat = CHECKLIST_CAT_KEYS[0]

    def on_camper_change(e):
        state.chk_cid = int(e.control.value)
        state.refresh()

    def on_cat_change(cat_key):
        state.chk_cat = cat_key
        state.refresh()

    children.append(ft.Dropdown(
        label=L("camper"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(state.chk_cid),
        on_select=on_camper_change,
    ))

    # Categoria: bottoni "filter chip"-like
    cat_buttons = []
    for k in CHECKLIST_CAT_KEYS:
        is_sel = (k == state.chk_cat)
        cat_buttons.append(
            ft.FilledButton(
                _strip_emoji(L(k)),
                on_click=lambda e, kk=k: on_cat_change(kk),
            ) if is_sel else ft.OutlinedButton(
                _strip_emoji(L(k)),
                on_click=lambda e, kk=k: on_cat_change(kk),
            )
        )
    children.append(ft.Row(cat_buttons, wrap=True, spacing=6, run_spacing=6))

    # Add nuova voce
    f_voce = ft.TextField(label=L("new_item"), expand=True)

    def add_voce(e):
        if (f_voce.value or "").strip():
            storage.add_checklist_voce(
                state.chk_cid, f_voce.value.strip(), state.chk_cat,
            )
            f_voce.value = ""
            state.refresh()

    children.append(ft.Row([
        f_voce,
        ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=ft.Colors.PRIMARY,
            tooltip=L("add"),
            on_click=add_voce,
        ),
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER))

    voci = [v for v in db["checklist"]
            if v["camper_id"] == state.chk_cid
            and v["categoria"] == state.chk_cat]

    if not voci:
        children.append(_info_box(
            L("no_item_for_category", cat=L(state.chk_cat)),
            ft.Icons.INFO,
        ))
        return _scrollable(children)

    fatte = sum(1 for v in voci if v["fatto"])
    children.append(ft.Container(
        content=ft.Column([
            ft.Text(
                L("n_completed", done=fatte, total=len(voci)),
                size=12, weight=ft.FontWeight.W_500,
            ),
            ft.ProgressBar(value=fatte / len(voci) if voci else 0),
        ], spacing=4, tight=True),
        padding=ft.Padding.symmetric(horizontal=2, vertical=4),
    ))

    def make_toggle(vid):
        def _h(e):
            storage.toggle_checklist_voce(vid)
            state.refresh()
        return _h

    def make_delete(vid):
        def _h(e):
            storage.delete_checklist_voce(vid)
            state.refresh()
        return _h

    for v in voci:
        children.append(ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=v["fatto"], on_change=make_toggle(v["id"]),
                ),
                ft.Text(
                    v["voce"], expand=True,
                    color=(ft.Colors.ON_SURFACE_VARIANT
                           if v["fatto"] else None),
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    on_click=make_delete(v["id"]),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding.only(left=4),
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
        ))

    def reset_cat(e):
        page = state.page
        if page is None:
            return

        def yes(ev):
            storage.reset_checklist(state.chk_cid, state.chk_cat)
            page.pop_dialog()
            state.refresh()

        def no(ev):
            page.pop_dialog()
            page.update()

        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(L("reset_category")),
            content=ft.Text(L("reset_confirm")),
            actions=[
                ft.TextButton(L("cancel"), on_click=no),
                ft.FilledButton(L("reset_category"), on_click=yes),
            ],
        ))

    children.append(ft.OutlinedButton(
        L("reset_category"),
        icon=ft.Icons.REFRESH,
        on_click=reset_cat,
    ))

    return _scrollable(children)


# ============================================================
# Pagina DOCUMENTI
# ============================================================
def build_documents(state: AppState) -> ft.Control:
    db = storage.load()
    cmap = {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}
    L = state.t

    children: list[ft.Control] = [
        ft.Row([
            ft.Text(L("documents_title"), size=22,
                    weight=ft.FontWeight.BOLD, expand=True),
            ft.FilledButton(
                _strip_emoji(L("upload_document")),
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda e: _open_add_documento_dialog(state),
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ]

    if not db["documenti"]:
        children.append(_info_box(L("no_document"), ft.Icons.INFO))
        return _scrollable(children)

    docs = sorted(db["documenti"], key=lambda x: x["data_caricamento"],
                  reverse=True)

    async def open_doc(d):
        path = storage.documento_path(d)
        if path.exists() and state.url_launcher is not None:
            await state.url_launcher.launch_url(path.resolve().as_uri())

    def make_open(d):
        async def _h(e):
            await open_doc(d)
        return _h

    def make_delete(did, label):
        return lambda e: _confirm_delete(
            state, label, lambda: storage.delete_documento(did))

    for d in docs:
        data_up = date.fromisoformat(d["data_caricamento"])
        sub_lines = [
            ft.Text(
                f"{cmap.get(d['camper_id'], '?')} - "
                f"{L('uploaded_on')} {data_up.strftime('%d/%m/%Y')}",
                size=12, color=ft.Colors.ON_SURFACE_VARIANT,
            ),
            ft.Text(d["nome_originale"], size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT, italic=True),
        ]
        if d.get("note"):
            sub_lines.append(ft.Text(
                d["note"], size=12, italic=True,
                color=ft.Colors.ON_SURFACE_VARIANT,
                max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
            ))
        children.append(ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.PRIMARY),
                ft.Column([
                    ft.Text(d["tipo"], weight=ft.FontWeight.BOLD,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    *sub_lines,
                ], spacing=2, tight=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.OPEN_IN_NEW,
                    tooltip=L("download"),
                    on_click=make_open(d),
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.ERROR,
                    tooltip=L("delete"),
                    on_click=make_delete(
                        d["id"],
                        f"{d['tipo']} - {d['nome_originale']}",
                    ),
                ),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=10,
        ))

    return _scrollable(children)


def _open_add_documento_dialog(state: AppState) -> None:
    page = state.page
    if page is None or state.file_picker is None:
        return
    L = state.t
    db = storage.load()

    if not db["campers"]:
        page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text(_strip_emoji(L("upload_document"))),
            content=ft.Text(L("select_camper_first")),
            actions=[ft.TextButton(L("cancel"),
                                   on_click=lambda e: page.pop_dialog())],
        ))
        return

    f_camper = ft.Dropdown(
        label=L("camper"),
        options=[ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']} ({c['targa']})",
        ) for c in db["campers"]],
        value=str(db["campers"][0]["id"]),
    )
    tipi_labels = [_t(k, state.lang) for k in TIPI_DOCUMENTI_KEYS]
    f_tipo = ft.Dropdown(
        label=L("doc_type"),
        options=[ft.dropdown.Option(key=lbl, text=lbl) for lbl in tipi_labels],
        value=tipi_labels[0],
    )
    f_note = ft.TextField(label=L("notes_optional"))
    f_file_label = ft.Text(L("file"), color=ft.Colors.ON_SURFACE_VARIANT)
    err = ft.Text("", color=ft.Colors.ERROR, size=12, visible=False)

    picked: dict = {"path": None, "name": None}

    def on_pick(e: ft.FilePickerResultEvent):
        if e.files:
            f = e.files[0]
            picked["path"] = f.path
            picked["name"] = f.name
            f_file_label.value = f.name
            f_file_label.color = ft.Colors.PRIMARY
            page.update()

    state.file_picker.on_result = on_pick

    async def pick_file(e):
        await state.file_picker.pick_files(allow_multiple=False)

    def show_err(msg: str):
        err.value = msg
        err.visible = True
        page.update()

    def save(e):
        if f_camper.value is None:
            show_err(L("select_camper_error"))
            return
        if not picked["path"]:
            show_err(L("select_file"))
            return
        try:
            data = Path(picked["path"]).read_bytes()
        except OSError as ex:
            show_err(str(ex))
            return
        storage.add_documento(
            int(f_camper.value), f_tipo.value, picked["name"],
            data, (f_note.value or "").strip(),
        )
        page.pop_dialog()
        state.refresh()
        state.snack(L("doc_uploaded", name=picked["name"]))

    def cancel(e):
        page.pop_dialog()
        page.update()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(_strip_emoji(L("upload_document"))),
        content=ft.Container(width=320, content=ft.Column([
            f_camper, f_tipo, f_note,
            ft.Row([
                ft.OutlinedButton(
                    L("file"), icon=ft.Icons.ATTACH_FILE,
                    on_click=pick_file,
                ),
                f_file_label,
            ], spacing=8),
            err,
        ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO)),
        actions=[
            ft.TextButton(L("cancel"), on_click=cancel),
            ft.FilledButton(L("upload"), on_click=save),
        ],
    ))


# ============================================================
# Pagina STATISTICHE
# ============================================================
def build_stats(state: AppState) -> ft.Control:
    db = storage.load()
    L = state.t

    children: list[ft.Control] = [
        ft.Text(L("stats_title"), size=22, weight=ft.FontWeight.BOLD),
    ]

    if not db["campers"]:
        children.append(_info_box(L("select_camper_first"), ft.Icons.INFO))
        return _scrollable(children)

    valid_ids = {c["id"] for c in db["campers"]}
    if state.stats_cid is not None and state.stats_cid not in valid_ids:
        state.stats_cid = None

    def on_change(e):
        v = e.control.value
        state.stats_cid = None if v == "__all__" else int(v)
        state.refresh()

    options = [ft.dropdown.Option(key="__all__", text=L("all_campers"))]
    for c in db["campers"]:
        options.append(ft.dropdown.Option(
            key=str(c["id"]),
            text=f"{c['marca']} {c['modello']}",
        ))
    children.append(ft.Dropdown(
        label=L("camper"), options=options,
        value="__all__" if state.stats_cid is None else str(state.stats_cid),
        on_select=on_change,
    ))

    def filtra(coll):
        if state.stats_cid is None:
            return coll
        return [x for x in coll if x["camper_id"] == state.stats_cid]

    interventi = filtra(db["interventi"])
    rifornimenti = filtra(db["rifornimenti"])
    viaggi = filtra(db["viaggi"])

    tot_int = sum(i["costo"] for i in interventi)
    tot_rif = sum(r["costo"] for r in rifornimenti)
    tot_via = sum(v["costo"] for v in viaggi)
    totale = tot_int + tot_rif + tot_via

    children.append(ft.Row([
        _metric_card(L("maintenance"), state.money(tot_int), ft.Icons.BUILD),
        _metric_card(L("fuel_label"), state.money(tot_rif),
                     ft.Icons.LOCAL_GAS_STATION),
        _metric_card(L("trips_label"), state.money(tot_via),
                     ft.Icons.LUGGAGE),
        _metric_card(L("total"), state.money(totale), ft.Icons.PAID),
    ], wrap=True, spacing=8, run_spacing=8))

    if not (interventi or rifornimenti or viaggi):
        children.append(_info_box(L("no_spending_data"), ft.Icons.INFO))
        return _scrollable(children)

    # ---- Costi mensili (ultimi 12 mesi)
    children.append(ft.Divider())
    children.append(ft.Text(L("monthly_costs"),
                            size=18, weight=ft.FontWeight.W_600))
    eventi: list[tuple[str, float]] = []
    for i in interventi:
        eventi.append((i["data"][:7], i["costo"]))
    for r in rifornimenti:
        eventi.append((r["data"][:7], r["costo"]))
    for v in viaggi:
        eventi.append((v["data_inizio"][:7], v["costo"]))
    by_month: dict[str, float] = {}
    for mese, costo in eventi:
        by_month[mese] = by_month.get(mese, 0.0) + costo
    mesi = sorted(by_month.keys(), reverse=True)[:12]
    if not mesi:
        children.append(ft.Text(L("no_spending_data"),
                                color=ft.Colors.ON_SURFACE_VARIANT))
    else:
        max_v = max(by_month[m] for m in mesi) or 1
        for m in mesi:
            v = by_month[m]
            children.append(ft.Row([
                ft.Text(m, size=12, width=68),
                ft.Container(
                    width=max(2, int(180 * v / max_v)),
                    height=14,
                    bgcolor=ft.Colors.PRIMARY,
                    border_radius=4,
                ),
                ft.Text(state.money(v), size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=8))

    # ---- Spaccato manutenzione per categoria
    children.append(ft.Divider())
    children.append(ft.Text(L("maintenance_breakdown"),
                            size=18, weight=ft.FontWeight.W_600))
    if not interventi:
        children.append(ft.Text(L("no_intervention_short"),
                                color=ft.Colors.ON_SURFACE_VARIANT))
    else:
        by_cat: dict[str, float] = {}
        for i in interventi:
            k = i.get("categoria", "int_altro")
            if k not in CATEGORIE_INTERVENTO_KEYS:
                k = "int_altro"
            by_cat[k] = by_cat.get(k, 0.0) + i["costo"]
        max_v = max(by_cat.values()) or 1
        for k in sorted(by_cat.keys(), key=lambda x: -by_cat[x]):
            v = by_cat[k]
            children.append(ft.Row([
                ft.Text(L(k), size=12, width=110,
                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Container(
                    width=max(2, int(180 * v / max_v)),
                    height=14,
                    bgcolor=ft.Colors.SECONDARY,
                    border_radius=4,
                ),
                ft.Text(state.money(v), size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT),
            ], spacing=8))

    # ---- Trend consumo (solo se filtrato su un camper)
    children.append(ft.Divider())
    children.append(ft.Text(L("consumption_trend"),
                            size=18, weight=ft.FontWeight.W_600))
    if state.stats_cid is None:
        children.append(ft.Text(L("select_single_camper"),
                                color=ft.Colors.ON_SURFACE_VARIANT))
    elif len(rifornimenti) < 2:
        children.append(ft.Text(L("need_two_refills"),
                                color=ft.Colors.ON_SURFACE_VARIANT))
    else:
        rifs_s = sorted(rifornimenti, key=lambda x: x["km"])
        punti = []
        for prec, succ in zip(rifs_s, rifs_s[1:]):
            delta = succ["km"] - prec["km"]
            if delta > 0 and succ["litri"] > 0:
                punti.append((succ["data"], (succ["litri"] / delta) * 100))
        if not punti:
            children.append(ft.Text(L("need_two_refills"),
                                    color=ft.Colors.ON_SURFACE_VARIANT))
        else:
            punti = punti[-12:]  # ultimi 12 punti
            max_v = max(p[1] for p in punti) or 1
            for d, v in punti:
                children.append(ft.Row([
                    ft.Text(d, size=12, width=88),
                    ft.Container(
                        width=max(2, int(180 * v / max_v)),
                        height=14,
                        bgcolor=ft.Colors.TERTIARY,
                        border_radius=4,
                    ),
                    ft.Text(f"{v:.1f} l/100km", size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT),
                ], spacing=8))

    return _scrollable(children)


# ============================================================
# Pagina IMPOSTAZIONI
# ============================================================
def _detect_local_ip() -> str | None:
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return None


def _build_phone_qr_section(state: AppState) -> ft.Control:
    """Sezione 'Apri sul telefono': QR + URL se l'app gira come web,
    altrimenti istruzioni per riavviare in modalita' web."""
    L = state.t
    page = state.page
    ip = _detect_local_ip()
    is_web = bool(page is not None and page.web)

    body: list[ft.Control] = [
        ft.Text(L("phone_section"), weight=ft.FontWeight.W_600),
    ]

    if is_web and ip:
        from urllib.parse import urlparse
        import io, base64
        import qrcode

        port = None
        try:
            port = urlparse(page.url or "").port
        except (ValueError, AttributeError):
            pass
        url = f"http://{ip}:{port or 8000}"

        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()

        body.extend([
            ft.Text(L("phone_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Image(src=f"data:image/png;base64,{b64}",
                     width=220, height=220),
            ft.Text(url, size=12, weight=ft.FontWeight.W_500,
                    selectable=True),
            ft.Text(L("phone_geo_warning"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
        ])
    elif not ip:
        body.append(_info_box(L("phone_no_network"), ft.Icons.WIFI_OFF))
    else:
        body.append(ft.Text(L("phone_run_hint"), size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                            selectable=True))

    return ft.Container(
        content=ft.Column(body, spacing=8, tight=True,
                          horizontal_alignment=ft.CrossAxisAlignment.START),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    )


def build_settings(state: AppState) -> ft.Control:
    db = storage.load()
    imp = db["impostazioni"]
    L = state.t

    children: list[ft.Control] = [
        ft.Text(L("settings_title"), size=22, weight=ft.FontWeight.BOLD),
        _build_phone_qr_section(state),
    ]

    # ---- Lingua
    codici = list(LINGUE_DISPONIBILI.keys())
    f_lang = ft.Dropdown(
        label=L("language"),
        options=[ft.dropdown.Option(key=c, text=LINGUE_DISPONIBILI[c])
                 for c in codici],
        value=state.lang,
    )

    def save_lang(e):
        if f_lang.value and f_lang.value != state.lang:
            storage.update_impostazioni(lingua=f_lang.value)
            state.reload()
            state.refresh()

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("language"), weight=ft.FontWeight.W_600),
            ft.Row([f_lang, ft.FilledButton(
                L("save"), icon=ft.Icons.SAVE, on_click=save_lang,
            )], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Valuta
    valute = ["EUR", "CHF"]
    f_val = ft.Dropdown(
        label=L("currency"),
        options=[ft.dropdown.Option(
            key=v, text=f"{storage.currency_symbol(v)} {v}",
        ) for v in valute],
        value=state.valuta,
    )

    def save_val(e):
        if f_val.value and f_val.value != state.valuta:
            storage.update_impostazioni(valuta=f_val.value)
            state.reload()
            state.refresh()

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("currency"), weight=ft.FontWeight.W_600),
            ft.Row([f_val, ft.FilledButton(
                L("save"), icon=ft.Icons.SAVE, on_click=save_val,
            )], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Soglia promemoria
    f_soglia = ft.TextField(
        label=L("days_before"), value=str(state.soglia),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def save_soglia(e):
        n = _parse_int(f_soglia.value or "0")
        if n is None or n < 1 or n > 365:
            return
        storage.update_impostazioni(giorni_promemoria=n)
        state.reload()
        state.refresh()

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("reminder_section"), weight=ft.FontWeight.W_600),
            ft.Row([f_soglia, ft.FilledButton(
                L("save_threshold"), icon=ft.Icons.SAVE, on_click=save_soglia,
            )], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Nickname
    f_nick = ft.TextField(
        label=L("nickname"), value=imp.get("nickname", ""), max_length=24,
    )

    def save_nick(e):
        new = (f_nick.value or "").strip()
        storage.update_impostazioni(nickname=new)
        state.refresh()

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("nickname"), weight=ft.FontWeight.W_600),
            ft.Row([f_nick, ft.FilledButton(
                L("save_nickname"), icon=ft.Icons.SAVE, on_click=save_nick,
            )], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Tema
    f_theme = ft.Dropdown(
        label=L("theme_section"),
        options=[
            ft.dropdown.Option(key="system", text=L("theme_system")),
            ft.dropdown.Option(key="light", text=L("theme_light")),
            ft.dropdown.Option(key="dark", text=L("theme_dark")),
        ],
        value=state.theme,
    )

    def save_theme(e):
        if not f_theme.value or f_theme.value == state.theme:
            return
        storage.update_impostazioni(tema=f_theme.value)
        state.reload()
        state.apply_theme()
        state.refresh()

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("theme_section"), weight=ft.FontWeight.W_600),
            ft.Row([f_theme, ft.FilledButton(
                L("save"), icon=ft.Icons.SAVE, on_click=save_theme,
            )], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Email (solo mailto: apre l'app email del telefono)
    f_email = ft.TextField(label=L("email_dest"),
                           value=imp.get("email", ""))

    def save_email(e):
        storage.update_impostazioni(email=(f_email.value or "").strip())
        state.snack(L("saved_ok"))

    # Mailto pre-calcolato: il bottone usa url= (link HTML nativo) cosi'
    # il browser/OS apre il client email anche in modalita' web.
    from notifications import imminent_deadlines, _build_body
    from urllib.parse import quote
    db_now = storage.load()
    items = imminent_deadlines(db_now)
    addr_saved = (imp.get("email") or "").strip()
    if items and addr_saved:
        subject = _t("email_subject", state.lang, n=len(items))
        body = _build_body(db_now, items, state.lang)
        mailto_url = (
            f"mailto:{quote(addr_saved)}"
            f"?subject={quote(subject)}&body={quote(body)}"
        )
    else:
        mailto_url = None

    if mailto_url:
        send_btn = ft.OutlinedButton(
            L("send_now"), icon=ft.Icons.SEND, url=mailto_url,
        )
    else:
        send_btn = ft.OutlinedButton(
            L("send_now"), icon=ft.Icons.SEND, disabled=True,
        )

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("email_section"), weight=ft.FontWeight.W_600),
            ft.Text(L("mailto_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            f_email,
            ft.Row([
                ft.FilledButton(
                    L("save"),
                    icon=ft.Icons.SAVE, on_click=save_email,
                ),
                send_btn,
            ], spacing=8, wrap=True, run_spacing=8),
            ft.Text(
                L("send_now_disabled_hint")
                if mailto_url is None else "",
                size=11,
                color=ft.Colors.ON_SURFACE_VARIANT,
                visible=mailto_url is None,
            ),
        ], spacing=8, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Backup
    async def on_backup_export(e):
        await _do_backup_export(state)

    def on_backup_import(e):
        _do_backup_import(state)

    children.append(ft.Container(
        content=ft.Column([
            ft.Text(L("backup_section"), weight=ft.FontWeight.W_600),
            ft.Text(L("backup_help"), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Row([
                ft.FilledButton(
                    L("backup_export"),
                    icon=ft.Icons.DOWNLOAD,
                    on_click=on_backup_export,
                ),
                ft.OutlinedButton(
                    L("backup_import"),
                    icon=ft.Icons.UPLOAD,
                    on_click=on_backup_import,
                ),
            ], spacing=8, wrap=True, run_spacing=8),
        ], spacing=8, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    ))

    # ---- Info path dati
    children.append(ft.Container(
        content=ft.Column([
            ft.Text("Database", weight=ft.FontWeight.W_600),
            ft.Text(str(storage.DB_FILE), size=11,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                    selectable=True),
        ], spacing=4, tight=True),
        padding=12,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        border_radius=10,
    ))

    return _scrollable(children)


async def _do_backup_export(state: AppState) -> None:
    """Genera lo ZIP e apre un Save dialog perche' l'utente scelga dove
    salvarlo."""
    page = state.page
    if page is None or state.file_picker is None:
        return
    L = state.t
    import backup as backup_mod

    fname, data = backup_mod.export_zip()

    def on_result(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        try:
            Path(e.path).write_bytes(data)
            state.snack(L("backup_export") + " ✓")
        except OSError as ex:
            state.snack(str(ex), error=True)

    state.file_picker.on_result = on_result
    await state.file_picker.save_file(
        file_name=fname,
        allowed_extensions=["zip"],
    )


def _do_backup_import(state: AppState) -> None:
    """Chiede conferma, poi apre un Pick dialog e ripristina lo ZIP."""
    page = state.page
    if page is None or state.file_picker is None:
        return
    L = state.t
    import backup as backup_mod

    async def proceed():
        def on_result(e: ft.FilePickerResultEvent):
            if not e.files:
                return
            picked = e.files[0]
            try:
                data = Path(picked.path).read_bytes()
                backup_mod.import_zip(data)
            except (OSError, ValueError) as ex:
                state.snack(str(ex), error=True)
                return
            state.reload()
            state.snack(L("backup_import") + " ✓")
            state.refresh()

        state.file_picker.on_result = on_result
        await state.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["zip"],
        )

    async def yes(e):
        page.pop_dialog()
        await proceed()

    def no(e):
        page.pop_dialog()
        state.refresh()

    page.show_dialog(ft.AlertDialog(
        modal=True,
        title=ft.Text(L("backup_import")),
        content=ft.Text(L("backup_import_help")),
        actions=[
            ft.TextButton(L("cancel"), on_click=no),
            ft.FilledButton(L("backup_restore_now"), on_click=yes),
        ],
    ))


# ============================================================
# Pagina MAPPA
# ============================================================
MAP_RADII_KM = [10, 25, 50, 100]

POI_ICONS = {
    "caravan_site": ft.Icons.AIRPORT_SHUTTLE,
    "sanitary_dump": ft.Icons.WATER_DROP,
    "camp_site": ft.Icons.HOLIDAY_VILLAGE,
    "greenzone": ft.Icons.PARK,
}


def _toggle_map_type(state: AppState, key: str, selected: bool) -> None:
    if selected:
        state.map_types.add(key)
    else:
        state.map_types.discard(key)


def _build_weather_section(state: AppState) -> ft.Control | None:
    """Riquadro meteo (current + forecast 5gg) per la posizione cercata.
    Ritorna None se non c'e' nessun dato/errore da mostrare."""
    L = state.t
    if state.map_weather_err:
        return _info_box(
            L("weather_error", err=state.map_weather_err),
            ft.Icons.CLOUD_OFF,
            icon_color=ft.Colors.ERROR,
            bgcolor=ft.Colors.ERROR_CONTAINER,
        )
    data = state.map_weather
    if not data:
        return None

    cur = data.get("current") or {}
    cur_emoji, cur_key = code_to_emoji_key(int(cur.get("weather_code", 0) or 0))

    def metric(label: str, value: str) -> ft.Control:
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=11,
                        color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(value, size=16, weight=ft.FontWeight.W_600),
            ], spacing=2, tight=True),
            padding=8,
            expand=True,
        )

    current_row = ft.Row([
        metric(L("weather_temp"),
               f"{cur.get('temperature_2m', 0):.0f}°C"),
        metric(L("weather_condition"),
               f"{cur_emoji} {L(cur_key)}"),
        metric(L("weather_wind"),
               f"{cur.get('wind_speed_10m', 0):.0f} km/h"),
        metric(L("weather_humidity"),
               f"{cur.get('relative_humidity_2m', 0):.0f}%"),
    ], wrap=True, run_spacing=4)

    children: list[ft.Control] = [
        ft.Text(L("weather_section"), weight=ft.FontWeight.W_600),
        ft.Text(L("weather_caption"), size=11,
                color=ft.Colors.ON_SURFACE_VARIANT),
        current_row,
    ]

    daily = data.get("daily") or {}
    days = daily.get("time") or []
    if days:
        forecast_cards: list[ft.Control] = []
        for i, iso in enumerate(days):
            d = date.fromisoformat(iso)
            dcode = int((daily.get("weather_code") or [0])[i] or 0)
            demoji, _dkey = code_to_emoji_key(dcode)
            tmax = (daily.get("temperature_2m_max") or [0])[i]
            tmin = (daily.get("temperature_2m_min") or [0])[i]
            prec = (daily.get("precipitation_sum") or [0])[i] or 0
            day_children = [
                ft.Text(d.strftime("%a %d/%m"),
                        size=11, weight=ft.FontWeight.W_600),
                ft.Text(demoji, size=24),
                ft.Text(f"{tmax:.0f}° / {tmin:.0f}°", size=12),
            ]
            if prec > 0:
                day_children.append(ft.Text(f"💧 {prec:.1f} mm",
                                            size=10,
                                            color=ft.Colors.ON_SURFACE_VARIANT))
            forecast_cards.append(ft.Container(
                content=ft.Column(day_children, spacing=2, tight=True,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=8, width=82,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
            ))
        children.append(ft.Text(L("weather_forecast_5d"),
                                weight=ft.FontWeight.W_600))
        children.append(ft.Row(forecast_cards, scroll=ft.ScrollMode.AUTO,
                               spacing=8))
        children.append(ft.Text(L("weather_source"), size=10,
                                color=ft.Colors.ON_SURFACE_VARIANT))

    return ft.Container(
        content=ft.Column(children, spacing=8, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    )


def _poi_card(state: AppState, r: dict) -> ft.Control:
    L = state.t
    name = r.get("name") or L("map_unnamed")
    type_label = (_t(f"poi_{r['type']}", state.lang)
                  if r.get("type") else "?")
    icon = POI_ICONS.get(r.get("type"), ft.Icons.PLACE)

    subtitle_parts = [type_label, f"{r['distance_km']} km"]
    fee = (r.get("fee") or "").lower()
    if fee == "yes":
        subtitle_parts.append(L("map_fee_yes"))
    elif fee == "no":
        subtitle_parts.append(L("map_fee_no"))
    op = r.get("operator") or ""
    if op:
        subtitle_parts.append(op)

    actions: list[ft.Control] = []

    async def open_maps(e, lat=r["lat"], lon=r["lon"]):
        if state.url_launcher is not None:
            await state.url_launcher.launch_url(
                f"https://www.google.com/maps/?q={lat},{lon}"
            )

    actions.append(ft.OutlinedButton(
        L("map_open_in_maps"), icon=ft.Icons.MAP, on_click=open_maps,
    ))

    phone = (r.get("phone") or "").strip()
    if phone:
        async def call(e, p=phone):
            if state.url_launcher is not None:
                await state.url_launcher.launch_url(f"tel:{p}")
        actions.append(ft.OutlinedButton(
            L("map_call"), icon=ft.Icons.CALL, on_click=call,
        ))

    website = (r.get("website") or "").strip()
    if website:
        if not website.startswith(("http://", "https://")):
            website = "https://" + website
        async def open_site(e, w=website):
            if state.url_launcher is not None:
                await state.url_launcher.launch_url(w)
        actions.append(ft.OutlinedButton(
            L("map_website"), icon=ft.Icons.LANGUAGE, on_click=open_site,
        ))

    # Affiliate Booking: solo per campeggi e aree sosta camper, e solo
    # se le credenziali CJ sono configurate (altrimenti booking_search_url=None).
    if r.get("type") in ("camp_site", "caravan_site"):
        burl = affiliates.booking_search_url(
            r.get("name") or "", r.get("lat"), r.get("lon"), state.lang,
        )
        if burl:
            async def open_booking(e, u=burl):
                if state.url_launcher is not None:
                    await state.url_launcher.launch_url(u)
            actions.append(ft.OutlinedButton(
                L("poi_book_booking"), icon=ft.Icons.HOTEL,
                on_click=open_booking,
            ))

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(icon, color=ft.Colors.PRIMARY),
                ft.Text(name, weight=ft.FontWeight.BOLD, size=15,
                        expand=True, max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS),
            ], spacing=10),
            ft.Text(" · ".join(subtitle_parts),
                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Row(actions, wrap=True, spacing=6, run_spacing=4),
        ], spacing=6, tight=True),
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
    )


def build_map(state: AppState) -> ft.Control:
    L = state.t

    f_query = ft.TextField(
        label=L("manual_location_label"),
        hint_text=L("manual_location_placeholder"),
        value=state.map_query,
        expand=True,
        on_change=lambda e: setattr(state, "map_query",
                                    e.control.value or ""),
    )

    async def open_search(e):
        if state.url_launcher is None:
            return
        q = (f_query.value or "").strip()
        if q:
            url = ("https://www.google.com/maps/search/?api=1"
                   f"&query={q.replace(' ', '+')}")
        else:
            url = "https://www.google.com/maps"
        await state.url_launcher.launch_url(url)

    f_radius = ft.Dropdown(
        label=L("map_radius"),
        value=str(state.map_radius_km),
        options=[ft.dropdown.Option(str(r)) for r in MAP_RADII_KM],
        on_select=lambda e: setattr(
            state, "map_radius_km", int(e.control.value or 25)),
        width=140,
    )

    def make_chip(t_key: str) -> ft.Chip:
        return ft.Chip(
            label=ft.Text(_t(f"poi_{t_key}", state.lang)),
            selected=t_key in state.map_types,
            on_select=lambda e, k=t_key: _toggle_map_type(
                state, k, e.control.selected),
        )

    chips = [make_chip(k) for k in poi.POI_TYPES.keys()]

    async def search_pois(e):
        q = (f_query.value or "").strip()
        if not q:
            state.map_error_key = "map_geocode_failed"
            state.refresh()
            return
        if not state.map_types:
            return
        state.map_query = q
        state.map_loading = True
        state.map_error_key = None
        state.map_results = []
        state.map_results_label = ""
        state.map_weather = None
        state.map_weather_err = None
        state.refresh()

        geo = await asyncio.to_thread(geocode, q, state.lang)
        if geo is None:
            state.map_loading = False
            state.map_error_key = "map_geocode_failed"
            state.refresh()
            return
        lat, lon, display = geo
        types = tuple(sorted(state.map_types))
        # POI + meteo in parallelo: usano endpoint diversi, nessun conflitto.
        pois_task = asyncio.to_thread(
            poi.fetch_pois, lat, lon, state.map_radius_km, types,
        )
        weather_task = asyncio.to_thread(fetch_weather, lat, lon)
        (results, err), (wdata, werr) = await asyncio.gather(
            pois_task, weather_task,
        )
        state.map_loading = False
        state.map_error_key = "map_network_error" if err else None
        state.map_results = results
        state.map_results_label = display
        state.map_weather = wdata
        state.map_weather_err = werr
        state.refresh()

    children: list[ft.Control] = [
        ft.Text(L("map_title"), size=22, weight=ft.FontWeight.BOLD),
        ft.Text(L("map_caption"), size=12,
                color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Row([
            f_query,
            ft.IconButton(
                icon=ft.Icons.SEARCH,
                icon_color=ft.Colors.PRIMARY,
                on_click=open_search,
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Text(L("manual_location_help"), size=11,
                color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Divider(),
        ft.Text(L("map_filters"), weight=ft.FontWeight.W_600),
        ft.Row(chips, wrap=True, spacing=6, run_spacing=6),
        ft.Row([
            f_radius,
            ft.FilledButton(
                L("map_search_pois"), icon=ft.Icons.TRAVEL_EXPLORE,
                on_click=search_pois, expand=True,
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.END, spacing=8),
    ]

    if state.map_loading:
        children.append(ft.Row([
            ft.ProgressRing(width=18, height=18, stroke_width=2),
            ft.Text(L("map_searching")),
        ], spacing=10))

    if state.map_error_key:
        children.append(_info_box(
            L(state.map_error_key), ft.Icons.ERROR_OUTLINE,
            icon_color=ft.Colors.ERROR,
            bgcolor=ft.Colors.ERROR_CONTAINER,
        ))

    weather_section = _build_weather_section(state)
    if weather_section is not None:
        children.append(ft.Divider())
        children.append(weather_section)

    if state.map_results:
        children.append(ft.Divider())
        children.append(ft.Text(
            f"{L('map_results_for')} {state.map_results_label} "
            f"({len(state.map_results)})",
            weight=ft.FontWeight.W_600,
        ))
        for r in state.map_results:
            children.append(_poi_card(state, r))
        # Disclosure affiliate: visibile solo se ci sono link Booking attivi.
        if affiliates.is_enabled() and any(
            r.get("type") in ("camp_site", "caravan_site")
            for r in state.map_results
        ):
            children.append(ft.Text(
                L("affiliate_disclosure"), size=10,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ))
    elif (state.map_results_label and not state.map_loading
          and not state.map_error_key):
        children.append(_info_box(L("map_no_results"), ft.Icons.SEARCH_OFF))

    children.append(_info_box(L("phone_geo_warning"), ft.Icons.INFO))

    return _scrollable(children)


# ============================================================
# Pagina placeholder (per i prossimi step)
# ============================================================
def build_placeholder(state: AppState, page_code: str) -> ft.Control:
    L = state.t
    label_key = next((k for code, _, _, k in PAGES if code == page_code), None)
    label = L(label_key) if label_key else page_code
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.CONSTRUCTION, size=64,
                    color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(label, size=22, weight=ft.FontWeight.BOLD),
            ft.Text(L("in_progress"), color=ft.Colors.ON_SURFACE_VARIANT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )


# ============================================================
# Router
# ============================================================
PAGE_BUILDERS = {
    "home": build_home,
    "campers": build_campers,
    "deadlines": build_deadlines,
    "logbook": build_logbook,
    "trips": build_trips,
    "fuel": build_fuel,
    "checklist": build_checklist,
    "documents": build_documents,
    "stats": build_stats,
    "settings": build_settings,
    "map": build_map,
}


def render_page(state: AppState, code: str) -> ft.Control:
    builder = PAGE_BUILDERS.get(code)
    if builder is None:
        return build_placeholder(state, code)
    return builder(state)


# ============================================================
# Main
# ============================================================
def main(page: ft.Page):
    state = AppState()
    state.page = page
    L = state.t

    page.title = "CAMPERappPLUS"
    page.theme_mode = ft.ThemeMode.SYSTEM
    state.apply_theme()
    page.padding = 0
    page.adaptive = True
    page.window.width = 420
    page.window.height = 820

    # FilePicker condiviso (usato dalla pagina Documenti).
    # In Flet 0.84+ FilePicker e' un service, non un control:
    # va in page.services, non in page.overlay.
    state.file_picker = ft.FilePicker()
    state.url_launcher = ft.UrlLauncher()
    page.services.append(state.file_picker)
    page.services.append(state.url_launcher)

    body = ft.Container(
        content=render_page(state, state.current_page),
        expand=True,
    )

    def navigate(code: str):
        state.current_page = code
        body.content = render_page(state, code)
        label_key = next((k for c, _, _, k in PAGES if c == code), None)
        if label_key:
            appbar.title = ft.Text(L(label_key))
        if code in QUICK_TABS:
            nav_bar.selected_index = QUICK_TABS.index(code)
        else:
            nav_bar.selected_index = len(QUICK_TABS)
        page.update()

    state.refresh_fn = lambda: navigate(state.current_page)

    # Drawer: tutte le pagine
    async def drawer_changed(e):
        idx = e.control.selected_index
        if 0 <= idx < len(PAGES):
            code = PAGES[idx][0]
            await page.close_drawer()
            navigate(code)

    drawer = ft.NavigationDrawer(
        controls=[ft.Container(content=ft.Text(
            "CAMPERappPLUS", weight=ft.FontWeight.BOLD, size=18,
        ), padding=ft.Padding.only(left=16, top=20, bottom=8))]
        + [
            ft.NavigationDrawerDestination(
                icon=ico_off, selected_icon=ico_on, label=L(lkey),
            )
            for code, ico_off, ico_on, lkey in PAGES
        ],
        on_change=drawer_changed,
    )
    page.drawer = drawer

    # NavigationBar in basso
    async def nav_changed(e):
        idx = e.control.selected_index
        if idx < len(QUICK_TABS):
            navigate(QUICK_TABS[idx])
        else:
            # ripristina indice precedente prima di aprire il drawer
            if state.current_page in QUICK_TABS:
                e.control.selected_index = QUICK_TABS.index(state.current_page)
            await page.show_drawer()

    nav_destinations = []
    for tab_code in QUICK_TABS:
        info = next(p for p in PAGES if p[0] == tab_code)
        _, ico_off, ico_on, lkey = info
        nav_destinations.append(ft.NavigationBarDestination(
            icon=ico_off, selected_icon=ico_on, label=_strip_emoji(L(lkey)),
        ))
    nav_destinations.append(ft.NavigationBarDestination(
        icon=ft.Icons.MENU, label=L("more"),
    ))
    nav_bar = ft.NavigationBar(
        destinations=nav_destinations,
        selected_index=0,
        on_change=nav_changed,
    )

    async def open_drawer(e):
        await page.show_drawer()

    appbar = ft.AppBar(
        title=ft.Text(L("page_home")),
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    page.appbar = appbar
    page.navigation_bar = nav_bar
    page.add(body)

    # Auto-refresh: se l'altra app (desktop) salva camper.json, ricarichiamo
    # la pagina in modo che l'utente non lavori su dati stale e non crei
    # conflitti al prossimo salvataggio (il lock cross-process in storage.py
    # protegge l'integrita', questo watcher protegge l'esperienza utente).
    try:
        state.last_db_mtime = storage.DB_FILE.stat().st_mtime
    except OSError:
        state.last_db_mtime = 0.0

    async def watch_db():
        while True:
            await asyncio.sleep(5)
            try:
                m = storage.DB_FILE.stat().st_mtime
            except OSError:
                continue
            if m != state.last_db_mtime:
                state.last_db_mtime = m
                state.reload()
                state.refresh()

    page.run_task(watch_db)


if __name__ == "__main__":
    ft.run(main)
