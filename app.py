"""CAMPERappPLUS — prototipo Streamlit.

Gestione camper per proprietari: scadenze, libretto, viaggi, consumi e altro.
"""
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

import affiliates
import storage
from translations import t, LINGUE_DISPONIBILI

_ICON_PATH = Path(__file__).parent / "icon.png"
st.set_page_config(
    page_title="CAMPERappPLUS",
    page_icon=str(_ICON_PATH) if _ICON_PATH.exists() else "🚐",
    layout="wide",
)

# Lingua e valuta correnti (lette una volta dal DB)
_db_init = storage.load()
LANG = _db_init["impostazioni"].get("lingua", "it")
VALUTA = _db_init["impostazioni"].get("valuta", "EUR")
SYM = storage.currency_symbol(VALUTA)


def L(key, **kwargs):
    kwargs.setdefault("sym", SYM)
    return t(key, LANG, **kwargs)


def money(amount, decimals=2):
    return storage.fmt_money(amount, VALUTA, decimals=decimals)


def open_external(url: str) -> None:
    """Apre URL in un browser esterno alla finestra Edge --app= che ospita
    Streamlit. Preferisce Chrome se installato (perche' l'utente lo ha chiesto
    esplicitamente), altrimenti usa il browser predefinito di sistema."""
    import os
    import subprocess
    import webbrowser
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        chrome_candidates.append(
            os.path.join(local, r"Google\Chrome\Application\chrome.exe")
        )
    for p in chrome_candidates:
        if os.path.exists(p):
            try:
                subprocess.Popen(
                    [p, url],
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                )
                return
            except OSError:
                continue
    webbrowser.open(url)


# ---------- Sidebar: navigazione ----------
st.sidebar.title("🚐 CAMPERappPLUS")

PAGES = [
    ("home", L("page_home")),
    ("campers", L("page_campers")),
    ("deadlines", L("page_deadlines")),
    ("logbook", L("page_logbook")),
    ("trips", L("page_trips")),
    ("map", L("page_map")),
    ("fuel", L("page_fuel")),
    ("checklist", L("page_checklist")),
    ("documents", L("page_documents")),
    ("stats", L("page_stats")),
    ("settings", L("page_settings")),
]
labels = [p[1] for p in PAGES]
codes = [p[0] for p in PAGES]
# preserva pagina corrente attraverso cambio lingua (i label cambiano, i code no)
default_code = st.session_state.get("pagina_code", "home")
default_idx = codes.index(default_code) if default_code in codes else 0
scelto = st.sidebar.radio(
    L("section"), labels, index=default_idx, key=f"nav_{LANG}",
)
pagina = next(code for code, lbl in PAGES if lbl == scelto)
st.session_state["pagina_code"] = pagina

st.sidebar.markdown("---")
st.sidebar.caption(L("sidebar_caption"))


# ---------- Helper ----------
def select_camper(key: str, label: str | None = None):
    db = storage.load()
    if not db["campers"]:
        st.info(L("select_camper_first"))
        return None, None
    options = {f"{c['marca']} {c['modello']} ({c['targa']})": c["id"] for c in db["campers"]}
    sel = st.selectbox(label or L("camper"), list(options.keys()), key=key)
    return options[sel], sel


def camper_label_map(db):
    return {c["id"]: f"{c['marca']} {c['modello']}" for c in db["campers"]}


def stato_scadenza(giorni, soglia):
    if giorni < 0:
        return "🔴 " + L("expired")
    if giorni <= soglia:
        return "🟠 " + L("upcoming")
    return "🟢 " + L("ok")


# tipi scadenza tradotti — chiave canonica salvata nel DB
TIPI_SCADENZA_KEYS = ["tipo_revisione", "tipo_vignetta", "tipo_assicurazione",
                      "tipo_bombole", "tipo_tagliando", "tipo_bollo", "tipo_altro"]
TIPI_DOCUMENTI_KEYS = ["doc_libretto", "doc_assicurazione", "doc_revisione", "doc_bollo",
                       "doc_ricevuta", "doc_manuale", "doc_foto", "doc_altro"]
CHECKLIST_CAT_KEYS = ["cat_partenza", "cat_apertura", "cat_chiusura", "cat_manutenzione"]
CATEGORIE_INTERVENTO_KEYS = ["int_revisione", "int_tagliando", "int_gomme", "int_freni",
                             "int_elettrico", "int_idraulico", "int_carrozzeria",
                             "int_motore", "int_altro"]


def tradotti(keys):
    return [L(k) for k in keys]


# ============================================================
# PAGINA — Home / Dashboard
# ============================================================
if pagina == "home":
    # Invio automatico promemoria all'avvio (una sola volta per sessione, con cooldown 24h).
    # Email + toast Windows sono indipendenti: ognuno con propria opzione e timestamp.
    if not st.session_state.get("_auto_reminder_done"):
        from notifications import auto_send_if_due
        from desktop_notif import auto_send_desktop_if_due
        n_sent, err = auto_send_if_due(LANG)
        n_toast, err_toast = auto_send_desktop_if_due(LANG)
        st.session_state["_auto_reminder_done"] = True
        if n_sent > 0:
            st.toast(L("auto_email_sent", n=n_sent), icon="📧")
        elif err and err != "SMTP_NOT_CONFIGURED":
            st.toast(L("auto_email_error"), icon="⚠️")
        if n_toast > 0:
            st.toast(L("auto_desktop_sent", n=n_toast), icon="🔔")
        elif err_toast:
            st.toast(L("auto_desktop_error"), icon="⚠️")

    st.title(L("welcome"))

    hero_path = Path(__file__).parent / "assets" / "hero.jpg"
    if hero_path.exists():
        st.image(str(hero_path), width="stretch")

    db = storage.load()
    soglia = db["impostazioni"]["giorni_promemoria"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(L("campers"), len(db["campers"]))
    c2.metric(L("deadlines"), len(db["scadenze"]))
    c3.metric(L("interventions"), len(db["interventi"]))
    c4.metric(L("trips"), len(db["viaggi"]))

    st.markdown("---")

    if not db["campers"]:
        st.info(L("start_add_camper"))
    else:
        cmap = camper_label_map(db)

        st.subheader(L("deadlines_within_days", n=soglia))
        imminenti = []
        for s in db["scadenze"]:
            d = date.fromisoformat(s["data"])
            giorni = (d - date.today()).days
            if giorni <= soglia:
                imminenti.append((giorni, s, d))
        imminenti.sort(key=lambda x: x[0])
        if not imminenti:
            st.success(L("no_upcoming"))
        else:
            for giorni, s, d in imminenti:
                stato = stato_scadenza(giorni, soglia)
                msg = f"{stato} — **{s['tipo']}** ({cmap.get(s['camper_id'], '?')}) — {d.strftime('%d/%m/%Y')}"
                when = L("expired_for_days", n=-giorni) if giorni < 0 else L("in_n_days", n=giorni)
                if giorni < 0:
                    st.error(f"{msg} · {when}")
                else:
                    st.warning(f"{msg} · {when}")

        st.markdown("---")
        st.subheader(L("total_costs_per_camper"))
        rows_costi = []
        for c in db["campers"]:
            cid = c["id"]
            tot_int = sum(i["costo"] for i in db["interventi"] if i["camper_id"] == cid)
            tot_rif = sum(r["costo"] for r in db["rifornimenti"] if r["camper_id"] == cid)
            tot_via = sum(v["costo"] for v in db["viaggi"] if v["camper_id"] == cid)
            totale = tot_int + tot_rif + tot_via
            km_percorsi = max(0, c["km"] - c.get("km_iniziale", c["km"]))
            eur_km = (totale / km_percorsi) if km_percorsi > 0 else None
            rows_costi.append({
                L("camper"): f"{c['marca']} {c['modello']}",
                L("maintenance"): tot_int,
                L("fuel_label"): tot_rif,
                L("trips_label"): tot_via,
                L("total"): totale,
                L("km_owned"): km_percorsi,
                L("eur_per_km"): eur_km if eur_km is not None else 0.0,
                "_eur_km_set": eur_km is not None,
            })
        if rows_costi:
            df_costi = pd.DataFrame(rows_costi)
            df_view = df_costi.drop(columns=["_eur_km_set"]).copy()
            eur_km_col = L("eur_per_km")
            # Mostra "—" quando non abbiamo ancora km percorsi
            df_view[eur_km_col] = [
                money(r[eur_km_col], decimals=3) if r["_eur_km_set"] else "—"
                for _, r in df_costi.iterrows()
            ]
            df_view[L("km_owned")] = df_view[L("km_owned")].map(
                lambda v: f"{v:,}".replace(",", ".")
            )
            fmt_cols = [L("maintenance"), L("fuel_label"), L("trips_label"), L("total")]
            st.dataframe(
                df_view.style.format({c: (lambda v: money(v)) for c in fmt_cols}),
                width="stretch", hide_index=True,
            )
            st.caption(L("eur_per_km_help"))

    # Banner affiliato Acronis: stesso annuncio CJ della landing e del
    # companion mobile, con sub-ID dedicato per distinguere i click desktop.
    st.markdown("---")
    with st.container(border=True):
        st.caption(L("ad_label").upper())
        st.markdown("**Acronis Cyber Protect**")
        st.write(L("ad_acronis_desc"))
        st.link_button(
            "🔒 " + L("ad_learn_more"),
            affiliates.acronis_banner_url("camperapp_desktop"),
        )


# ============================================================
# PAGINA — Camper
# ============================================================
elif pagina == "campers":
    st.title(L("my_campers"))
    db = storage.load()

    with st.expander(L("add_camper"), expanded=not db["campers"]):
        with st.form("nuovo_camper", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                marca = st.text_input(L("brand"))
                anno = st.number_input(L("year"), min_value=1980, max_value=date.today().year, value=2018)
            with col2:
                modello = st.text_input(L("model"))
                targa = st.text_input(L("plate"))
            km = st.number_input(L("current_km"), min_value=0, value=50000, step=1000)
            st.caption(L("km_iniziale_help"))

            if st.form_submit_button(L("save_camper")):
                if not (marca and modello and targa):
                    st.error(L("fill_required"))
                else:
                    storage.add_camper(marca, modello, int(anno), targa, int(km))
                    st.success(L("camper_added", name=f"{marca} {modello}"))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("my_fleet"))
    if not db["campers"]:
        st.write(L("no_camper_yet"))
    else:
        for c in db["campers"]:
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.markdown(
                        f"**{c['marca']} {c['modello']}** — {c['anno']} · "
                        f"`{c['targa']}` · {c['km']:,} km".replace(",", ".")
                    )
                with col2:
                    nuovo_km = st.number_input(
                        L("update_km"), min_value=0, value=int(c["km"]),
                        step=500, key=f"km_{c['id']}",
                    )
                    if nuovo_km != c["km"]:
                        if st.button("💾", key=f"savekm_{c['id']}", help=L("save_new_km")):
                            storage.update_camper_km(c["id"], int(nuovo_km))
                            st.rerun()
                with col3:
                    if st.button("🗑️ " + L("delete"), key=f"del_{c['id']}"):
                        storage.delete_camper(c["id"])
                        st.rerun()
                with st.expander(L("edit_km_iniziale"), expanded=False):
                    km_init = st.number_input(
                        L("km_iniziale_label"), min_value=0,
                        value=int(c.get("km_iniziale", c["km"])),
                        step=500, key=f"kmin_{c['id']}",
                    )
                    if km_init != c.get("km_iniziale", c["km"]):
                        if st.button(L("save"), key=f"savekmin_{c['id']}"):
                            storage.update_camper_km_iniziale(c["id"], int(km_init))
                            st.rerun()
                    st.caption(L("km_iniziale_help"))


# ============================================================
# PAGINA — Scadenze
# ============================================================
elif pagina == "deadlines":
    st.title(L("deadlines"))
    db = storage.load()
    soglia = db["impostazioni"]["giorni_promemoria"]

    tipi_labels = tradotti(TIPI_SCADENZA_KEYS)

    with st.expander(L("add_deadline"), expanded=not db["scadenze"]):
        with st.form("nuova_scadenza", clear_on_submit=True):
            cid, _ = select_camper("scad_camper")
            tipo = st.selectbox(L("type"), tipi_labels)
            data_scad = st.date_input(L("deadline_date"), value=date.today() + timedelta(days=30))
            note = st.text_input(L("notes_optional"))
            if st.form_submit_button(L("save_deadline")):
                if cid is None:
                    st.error(L("select_camper_error"))
                else:
                    storage.add_scadenza(cid, tipo, data_scad, note)
                    st.success(L("deadline_added"))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("upcoming_deadlines"))

    if not db["scadenze"]:
        st.write(L("no_deadline"))
    else:
        cmap = camper_label_map(db)
        rows = []
        for s in db["scadenze"]:
            d = date.fromisoformat(s["data"])
            giorni = (d - date.today()).days
            rows.append({
                L("status"): stato_scadenza(giorni, soglia),
                L("camper"): cmap.get(s["camper_id"], "?"),
                L("type"): s["tipo"],
                L("date"): d.strftime("%d/%m/%Y"),
                L("days"): giorni,
                L("notes"): s["note"] or "",
                "_id": s["id"],
            })
        rows.sort(key=lambda r: r[L("days")])
        df = pd.DataFrame(rows).drop(columns=["_id"])
        st.dataframe(df, width="stretch", hide_index=True)

        with st.expander(L("delete_deadline_section")):
            for r in rows:
                if st.button(f"🗑️ {r[L('camper')]} — {r[L('type')]} ({r[L('date')]})", key=f"dels_{r['_id']}"):
                    storage.delete_scadenza(r["_id"])
                    st.rerun()


# ============================================================
# PAGINA — Libretto
# ============================================================
elif pagina == "logbook":
    st.title(L("page_logbook").split(" ", 1)[1])
    db = storage.load()

    cat_int_labels = tradotti(CATEGORIE_INTERVENTO_KEYS)
    cat_int_label_to_key = dict(zip(cat_int_labels, CATEGORIE_INTERVENTO_KEYS))

    with st.expander(L("add_intervention"), expanded=not db["interventi"]):
        with st.form("nuovo_intervento", clear_on_submit=True):
            cid, _ = select_camper("int_camper")
            col1, col2 = st.columns(2)
            with col1:
                data_int = st.date_input(L("date"), value=date.today())
                km = st.number_input(L("km"), min_value=0, value=0, step=1000)
                categoria_label = st.selectbox(L("category"), cat_int_labels)
            with col2:
                costo = st.number_input(L("cost_eur"), min_value=0.0, value=0.0, step=10.0, format="%.2f")
            descrizione = st.text_area(L("intervention_desc"))
            if st.form_submit_button(L("save_intervention")):
                if cid is None:
                    st.error(L("select_camper_error"))
                elif not descrizione:
                    st.error(L("fill_description"))
                else:
                    cat_key = cat_int_label_to_key[categoria_label]
                    storage.add_intervento(cid, data_int, descrizione,
                                           float(costo), int(km), categoria=cat_key)
                    st.success(L("intervention_saved"))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("history_interventions"))

    if not db["interventi"]:
        st.write(L("no_intervention"))
    else:
        cmap = camper_label_map(db)
        rows = [{
            L("date"): date.fromisoformat(i["data"]).strftime("%d/%m/%Y"),
            L("camper"): cmap.get(i["camper_id"], "?"),
            L("category"): L(i.get("categoria", "int_altro")),
            L("description"): i["descrizione"],
            L("km"): f"{i['km']:,}".replace(",", "."),
            L("cost"): money(i["costo"]),
            "_id": i["id"],
        } for i in sorted(db["interventi"], key=lambda x: x["data"], reverse=True)]
        df = pd.DataFrame(rows).drop(columns=["_id"])
        st.dataframe(df, width="stretch", hide_index=True)

        totale = sum(i["costo"] for i in db["interventi"])
        st.metric(L("total_maintenance"), money(totale))

        st.markdown("---")
        st.subheader(L("export_pdf_logbook"))
        col_a, col_b = st.columns(2)
        with col_a:
            cid_exp, label_exp = select_camper("pdf_camper", L("camper_to_export"))
        with col_b:
            if cid_exp is not None:
                from pdf_export import build_libretto_pdf
                pdf_bytes = build_libretto_pdf(db, cid_exp, LANG, VALUTA)
                st.download_button(
                    L("download_pdf"),
                    data=pdf_bytes,
                    file_name=f"libretto_{label_exp.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                )

        with st.expander(L("delete_intervention_section")):
            for r in rows:
                if st.button(f"🗑️ {r[L('camper')]} — {r[L('description')][:40]} ({r[L('date')]})", key=f"deli_{r['_id']}"):
                    storage.delete_intervento(r["_id"])
                    st.rerun()


# ============================================================
# PAGINA — Viaggi
# ============================================================
elif pagina == "trips":
    st.title(L("trip_diary_title"))
    db = storage.load()

    with st.expander(L("add_trip"), expanded=not db["viaggi"]):
        with st.form("nuovo_viaggio", clear_on_submit=True):
            cid, _ = select_camper("via_camper")
            col1, col2 = st.columns(2)
            with col1:
                data_inizio = st.date_input(L("departure_date"), value=date.today())
                destinazione = st.text_input(L("destination"))
                km_perc = st.number_input(L("km_done"), min_value=0, value=0, step=50)
            with col2:
                data_fine = st.date_input(L("return_date"), value=date.today() + timedelta(days=3))
                costo = st.number_input(L("total_cost_eur"), min_value=0.0, value=0.0, step=10.0, format="%.2f")
            note = st.text_area(L("notes"))
            if st.form_submit_button(L("save_trip")):
                if cid is None:
                    st.error(L("select_camper_error"))
                elif not destinazione:
                    st.error(L("fill_destination"))
                elif data_fine < data_inizio:
                    st.error(L("return_before_departure"))
                else:
                    storage.add_viaggio(cid, data_inizio, data_fine, destinazione,
                                        int(km_perc), float(costo), note)
                    st.success(L("trip_saved"))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("my_trips"))

    if not db["viaggi"]:
        st.write(L("no_trip"))
    else:
        cmap = camper_label_map(db)
        rows = []
        for v in sorted(db["viaggi"], key=lambda x: x["data_inizio"], reverse=True):
            di = date.fromisoformat(v["data_inizio"])
            df_ = date.fromisoformat(v["data_fine"])
            durata = (df_ - di).days + 1
            rows.append({
                L("camper"): cmap.get(v["camper_id"], "?"),
                L("destination"): v["destinazione"],
                L("from"): di.strftime("%d/%m/%Y"),
                L("to"): df_.strftime("%d/%m/%Y"),
                L("days"): durata,
                L("km"): f"{v['km_percorsi']:,}".replace(",", "."),
                L("cost"): money(v["costo"]),
                L("notes"): v["note"] or "",
                "_id": v["id"],
            })
        df = pd.DataFrame(rows).drop(columns=["_id"])
        st.dataframe(df, width="stretch", hide_index=True)

        c1, c2, c3 = st.columns(3)
        c1.metric(L("total_trips"), len(db["viaggi"]))
        c2.metric(L("total_km"), f"{sum(v['km_percorsi'] for v in db['viaggi']):,}".replace(",", "."))
        c3.metric(L("total_trip_spending"), money(sum(v["costo"] for v in db["viaggi"])))

        with st.expander(L("delete_trip_section")):
            for r in rows:
                if st.button(f"🗑️ {r[L('camper')]} — {r[L('destination')]} ({r[L('from')]})", key=f"delv_{r['_id']}"):
                    storage.delete_viaggio(r["_id"])
                    st.rerun()

# ============================================================
# PAGINA — Mappa live
# ============================================================
elif pagina == "map":
    st.title(L("map_title"))
    st.caption(L("map_caption"))

    from streamlit_geolocation import streamlit_geolocation
    from weather import geocode

    # Input manuale: sovrascrive il GPS quando compilato. Utile su PC fissi
    # dove la geolocalizzazione browser e' IP-based e poco precisa.
    manual_query = st.text_input(
        L("manual_location_label"),
        placeholder=L("manual_location_placeholder"),
        key="manual_loc_input",
        help=L("manual_location_help"),
    )

    lat = lon = None
    accuracy = altitude = speed = None
    location_source = None

    if manual_query.strip():
        cache_key = f"_geo_{manual_query.strip().lower()}"
        if cache_key not in st.session_state:
            with st.spinner(L("manual_searching")):
                st.session_state[cache_key] = geocode(manual_query, LANG)
        geo = st.session_state[cache_key]
        if geo is None:
            st.warning(L("manual_not_found"))
        else:
            lat, lon, place_name = geo
            st.success(L("manual_found", place=place_name))
            location_source = "manual"
    else:
        st.caption(L("manual_or_gps"))
        location = streamlit_geolocation()
        if isinstance(location, dict):
            lat = location.get("latitude")
            lon = location.get("longitude")
            accuracy = location.get("accuracy")
            altitude = location.get("altitude")
            speed = location.get("speed")
        if lat is not None and lon is not None:
            location_source = "gps"

    has_pos = lat is not None and lon is not None

    if not has_pos:
        st.info(L("click_locate"))
        # Bottone server-side: lancia Chrome (o browser predefinito) esterno
        # alla finestra Edge --app=, dove i target=_blank non si aprono.
        if st.button("🗺️ " + L("open_gmaps_direct"), key="btn_gmaps_direct"):
            open_external("https://www.google.com/maps")
    else:
        cols = st.columns(4)
        cols[0].metric(L("latitude"), f"{lat:.5f}")
        cols[1].metric(L("longitude"), f"{lon:.5f}")
        cols[2].metric(L("accuracy_m"), f"{accuracy:.0f}" if accuracy else "—")
        if speed is not None:
            cols[3].metric(L("speed_kmh"), f"{speed * 3.6:.1f}")
        elif altitude is not None:
            cols[3].metric(L("altitude_m"), f"{altitude:.0f}")

        gmaps_url = f"https://www.google.com/maps?q={lat},{lon}"
        if st.button("🗺️ " + L("open_in_gmaps"), key="btn_gmaps_pos"):
            open_external(gmaps_url)
        st.caption(L("gmaps_more_precise"))

        # ----- Meteo via Open-Meteo -----
        st.markdown("---")
        st.subheader(L("weather_section"))
        st.caption(L("weather_caption"))
        import weather as weather_mod

        weather_data, weather_err = weather_mod.fetch_weather(lat, lon)
        if weather_err:
            st.warning(L("weather_error", err=weather_err))
        elif weather_data:
            cur = weather_data.get("current", {})
            cur_code = int(cur.get("weather_code", 0))
            cur_emoji, cur_key = weather_mod.code_to_emoji_key(cur_code)
            wcols = st.columns(4)
            wcols[0].metric(
                L("weather_temp"),
                f"{cur.get('temperature_2m', 0):.0f}°C",
            )
            wcols[1].metric(
                L("weather_condition"),
                f"{cur_emoji} {L(cur_key)}",
            )
            wcols[2].metric(
                L("weather_wind"),
                f"{cur.get('wind_speed_10m', 0):.0f} km/h",
            )
            wcols[3].metric(
                L("weather_humidity"),
                f"{cur.get('relative_humidity_2m', 0):.0f}%",
            )

            daily = weather_data.get("daily") or {}
            days = daily.get("time") or []
            if days:
                st.markdown(f"**{L('weather_forecast_5d')}**")
                day_cols = st.columns(len(days))
                for i, dcol in enumerate(day_cols):
                    d = date.fromisoformat(days[i])
                    dcode = int(daily["weather_code"][i])
                    demoji, dkey = weather_mod.code_to_emoji_key(dcode)
                    tmax = daily["temperature_2m_max"][i]
                    tmin = daily["temperature_2m_min"][i]
                    prec = daily["precipitation_sum"][i] or 0
                    with dcol:
                        st.markdown(f"**{d.strftime('%a %d/%m')}**")
                        st.markdown(
                            f"<div style='font-size:32px;line-height:1.2'>{demoji}</div>",
                            unsafe_allow_html=True,
                        )
                        st.write(f"{tmax:.0f}° / {tmin:.0f}°")
                        if prec > 0:
                            st.caption(f"💧 {prec:.1f} mm")
                st.caption(L("weather_source"))

        # ----- Aree sosta / camper service da OpenStreetMap -----
        st.markdown("---")
        st.subheader(L("poi_section"))
        st.caption(L("poi_caption"))

        import poi as poi_mod

        # Inietta CSS per colorare lo sfondo dei chip del multiselect in base
        # al testo dell'aria-label. Le label hanno emoji distintive che rendono
        # il match robusto anche cambiando lingua.
        chip_css_rules = []
        emoji_color_map = [
            ("🅿️", "#1f77b4"),  # area sosta camper
            ("🚽", "#2ca02c"),   # camper service
            ("⛺", "#d62728"),   # campeggio
            ("🌳", "#9467bd"),   # greenzone
        ]
        for emoji, color in emoji_color_map:
            chip_css_rules.append(
                f'div[data-baseweb="select"] [data-baseweb="tag"]'
                f'[aria-label*="{emoji}"] {{'
                f'background-color: {color} !important; color: white !important;'
                f'}}'
            )
        st.markdown(
            "<style>" + "\n".join(chip_css_rules) + "</style>",
            unsafe_allow_html=True,
        )

        type_options = {
            L("poi_caravan_site"): "caravan_site",
            L("poi_sanitary_dump"): "sanitary_dump",
            L("poi_camp_site"): "camp_site",
            L("poi_greenzone"): "greenzone",
        }
        col_t, col_r = st.columns([3, 1])
        with col_t:
            selected_labels = st.multiselect(
                L("poi_types"),
                options=list(type_options.keys()),
                default=list(type_options.keys()),
                key="poi_types_sel",
            )
        with col_r:
            radius_km = st.selectbox(
                L("poi_radius"), options=[10, 25, 50, 100],
                index=1, key="poi_radius_sel",
            )
        selected_types = tuple(type_options[lbl] for lbl in selected_labels)

        # Invalida risultati cached se la posizione e' cambiata: senza questo
        # cambiando citta' nella casella di ricerca la mappa continuerebbe a
        # mostrare i POI della citta' precedente finche' l'utente non riclicca
        # "Cerca POI". Tolleranza ~1km (round a 2 decimali).
        cur_loc_key = f"{round(lat, 2)}|{round(lon, 2)}"
        if st.session_state.get("_poi_loc_key") != cur_loc_key:
            st.session_state.pop("_poi_results", None)
            st.session_state.pop("_poi_err", None)

        if st.button(L("poi_search"), key="poi_search_btn"):
            with st.spinner(L("poi_searching")):
                results, err = poi_mod.fetch_pois(lat, lon, int(radius_km), selected_types)
            st.session_state["_poi_results"] = results
            st.session_state["_poi_err"] = err
            st.session_state["_poi_loc_key"] = cur_loc_key

        results = st.session_state.get("_poi_results", [])
        err = st.session_state.get("_poi_err")

        if err:
            st.error(L("poi_error", err=err))
        elif results is not None and len(results) == 0 and "_poi_results" in st.session_state:
            st.info(L("poi_none_found"))
        elif results:
            st.success(L("poi_found", n=len(results)))

            import folium
            from folium.plugins import MarkerCluster
            from streamlit_folium import st_folium

            type_color = {k: v[2] for k, v in poi_mod.POI_TYPES.items()}
            type_label = {k: L(v[1]) for k, v in poi_mod.POI_TYPES.items()}

            fmap = folium.Map(location=[lat, lon], zoom_start=11)
            folium.Marker(
                [lat, lon], tooltip=L("you_are_here"),
                icon=folium.Icon(color="red", icon="user", prefix="fa"),
            ).add_to(fmap)

            # Cluster: ZoomToBoundsOnClick + spiderfy. Tiene browser fluido
            # anche con centinaia di POI.
            cluster = MarkerCluster(name="pois").add_to(fmap)
            for r in results:
                color_hex = type_color.get(r["type"], "#888888")
                tlabel = type_label.get(r["type"], r["type"])
                name = r["name"] or L("poi_no_name")
                popup_html = (
                    f"<b>{name}</b><br>{tlabel}<br>{r['distance_km']} km"
                )
                if r.get("operator"):
                    popup_html += f"<br>{r['operator']}"
                if r.get("fee"):
                    popup_html += f"<br>{L('poi_fee')}: {r['fee']}"
                if r.get("website"):
                    popup_html += f'<br><a href="{r["website"]}" target="_blank">{L("poi_website")}</a>'
                # Affiliate Booking: solo per campeggi e aree sosta camper, e solo
                # se BOOKING_AID e' impostato (altrimenti booking_search_url=None).
                if r["type"] in ("camp_site", "caravan_site"):
                    burl = affiliates.booking_search_url(
                        r["name"] or "", r["lat"], r["lon"], LANG,
                    )
                    if burl:
                        popup_html += (
                            f'<br><a href="{burl}" target="_blank" '
                            f'rel="sponsored noopener">{L("poi_book_booking")}</a>'
                        )
                folium.CircleMarker(
                    [r["lat"], r["lon"]], radius=7, color=color_hex,
                    fill=True, fill_opacity=0.85, weight=2,
                    popup=folium.Popup(popup_html, max_width=280),
                    tooltip=name,
                ).add_to(cluster)

            st_folium(fmap, width=None, height=480, returned_objects=[])

            # Disclosure affiliate: visibile solo se ci sono link Booking attivi.
            if affiliates.is_enabled() and any(
                r["type"] in ("camp_site", "caravan_site") for r in results
            ):
                st.caption(L("affiliate_disclosure"))

            # Lista compatta sotto la mappa
            st.markdown(f"**{L('poi_list')}**")
            for r in results[:50]:
                name = r["name"] or L("poi_no_name")
                tlabel = type_label.get(r["type"], r["type"])
                gm = f"https://www.google.com/maps?q={r['lat']},{r['lon']}"
                st.markdown(
                    f"- **{name}** — _{tlabel}_ · {r['distance_km']} km · "
                    f"[{L('open_in_gmaps')}]({gm})"
                )
            if len(results) > 50:
                st.caption(L("poi_truncated", shown=50, total=len(results)))


# ============================================================
# PAGINA — Rifornimenti
# ============================================================
elif pagina == "fuel":
    st.title(L("fuel_title"))
    db = storage.load()

    with st.expander(L("add_fuel"), expanded=not db["rifornimenti"]):
        with st.form("nuovo_rifornimento", clear_on_submit=True):
            cid, _ = select_camper("rif_camper")
            col1, col2 = st.columns(2)
            with col1:
                data_rif = st.date_input(L("date"), value=date.today())
                km = st.number_input(L("odometer_km"), min_value=0, value=0, step=100)
                litri = st.number_input(L("liters"), min_value=0.0, value=0.0, step=1.0, format="%.2f")
            with col2:
                costo = st.number_input(L("total_cost_eur"), min_value=0.0, value=0.0, step=1.0, format="%.2f")
                distributore = st.text_input(L("station"))
                pieno = st.checkbox(L("full_tank"), value=True, help=L("full_tank_help"))
            note = st.text_input(L("notes_optional"))
            if st.form_submit_button(L("save_fuel")):
                if cid is None:
                    st.error(L("select_camper_error"))
                elif litri <= 0 or km <= 0:
                    st.error(L("fill_km_liters"))
                else:
                    storage.add_rifornimento(cid, data_rif, int(km), float(litri),
                                             float(costo), distributore, note,
                                             pieno=bool(pieno))
                    st.success(L("fuel_saved"))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("fuel_history"))

    if not db["rifornimenti"]:
        st.write(L("no_fuel"))
    else:
        cmap = camper_label_map(db)
        rows = []
        for c in db["campers"]:
            rifs = sorted(
                [r for r in db["rifornimenti"] if r["camper_id"] == c["id"]],
                key=lambda x: x["km"],
            )
            # Per ogni "pieno", somma i litri dei rifornimenti dal pieno precedente
            # (inclusi quelli intermedi) diviso la distanza percorsa.
            prev_pieno_km = None
            litri_dal_pieno = 0.0
            for r in rifs:
                pieno = r.get("pieno", True)
                litri_dal_pieno += r["litri"]
                if pieno and prev_pieno_km is not None and r["km"] > prev_pieno_km:
                    delta_km = r["km"] - prev_pieno_km
                    consumo_str = f"{(litri_dal_pieno / delta_km) * 100:.1f}"
                else:
                    consumo_str = "—"
                prezzo_l = r["costo"] / r["litri"] if r["litri"] > 0 else 0
                rows.append({
                    L("date"): date.fromisoformat(r["data"]).strftime("%d/%m/%Y"),
                    L("camper"): cmap.get(r["camper_id"], "?"),
                    L("km"): f"{r['km']:,}".replace(",", "."),
                    L("liters"): f"{r['litri']:.2f}",
                    L("full_tank_short"): "✅" if pieno else "—",
                    f"{SYM}/L": f"{prezzo_l:.3f}",
                    L("cost"): money(r["costo"]),
                    L("station"): r["distributore"] or "",
                    L("consumption_l100"): consumo_str,
                    "_id": r["id"],
                    "_data": r["data"],
                })
                if pieno:
                    prev_pieno_km = r["km"]
                    litri_dal_pieno = 0.0
        rows.sort(key=lambda x: x["_data"], reverse=True)
        df = pd.DataFrame(rows).drop(columns=["_id", "_data"])
        st.dataframe(df, width="stretch", hide_index=True)

        st.markdown(f"**{L('avg_consumption')}**")
        for c in db["campers"]:
            rifs = sorted(
                [r for r in db["rifornimenti"] if r["camper_id"] == c["id"]],
                key=lambda x: x["km"],
            )
            # Media: solo tra il primo e l'ultimo "pieno"; somma litri intermedi.
            pieni_km = [(idx, r["km"]) for idx, r in enumerate(rifs) if r.get("pieno", True)]
            if len(pieni_km) >= 2:
                first_idx, first_km = pieni_km[0]
                last_idx, last_km = pieni_km[-1]
                tot_litri = sum(r["litri"] for r in rifs[first_idx + 1: last_idx + 1])
                tot_km = last_km - first_km
                if tot_km > 0 and tot_litri > 0:
                    medio = (tot_litri / tot_km) * 100
                    st.write(
                        f"- {c['marca']} {c['modello']}: **{medio:.1f} l/100km** "
                        f"({tot_km:,} km)".replace(",", ".")
                    )

        with st.expander(L("delete_fuel_section")):
            for r in rows:
                if st.button(f"🗑️ {r[L('camper')]} — {r[L('date')]} ({r[L('liters')]}L)", key=f"delr_{r['_id']}"):
                    storage.delete_rifornimento(r["_id"])
                    st.rerun()


# ============================================================
# PAGINA — Checklist
# ============================================================
elif pagina == "checklist":
    st.title(L("checklist_title"))
    db = storage.load()

    if not db["campers"]:
        st.info(L("select_camper_first"))
    else:
        cid, _ = select_camper("chk_camper")
        cat_labels = tradotti(CHECKLIST_CAT_KEYS)
        categoria = st.radio(L("category"), cat_labels, horizontal=True)

        with st.form("nuova_voce_chk", clear_on_submit=True):
            voce = st.text_input(L("new_item"))
            if st.form_submit_button("➕ " + L("add")):
                if voce:
                    storage.add_checklist_voce(cid, voce, categoria)
                    st.rerun()

        st.markdown("---")
        voci = [v for v in db["checklist"] if v["camper_id"] == cid and v["categoria"] == categoria]
        if not voci:
            st.write(L("no_item_for_category", cat=categoria))
        else:
            fatte = sum(1 for v in voci if v["fatto"])
            st.progress(fatte / len(voci) if voci else 0,
                        text=L("n_completed", done=fatte, total=len(voci)))
            for v in voci:
                col1, col2 = st.columns([8, 1])
                with col1:
                    nuovo = st.checkbox(v["voce"], value=v["fatto"], key=f"chk_{v['id']}")
                    if nuovo != v["fatto"]:
                        storage.toggle_checklist_voce(v["id"])
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delchk_{v['id']}"):
                        storage.delete_checklist_voce(v["id"])
                        st.rerun()
            if st.button(L("reset_category"), key="reset_chk"):
                storage.reset_checklist(cid, categoria)
                st.rerun()


# ============================================================
# PAGINA — Documenti
# ============================================================
elif pagina == "documents":
    st.title(L("documents_title"))
    db = storage.load()

    doc_types = tradotti(TIPI_DOCUMENTI_KEYS)

    with st.expander(L("upload_document"), expanded=not db["documenti"]):
        with st.form("nuovo_doc", clear_on_submit=True):
            cid, _ = select_camper("doc_camper")
            tipo = st.selectbox(L("doc_type"), doc_types)
            file = st.file_uploader(L("file"), type=None)
            note = st.text_input(L("notes_optional"))
            if st.form_submit_button(L("upload")):
                if cid is None:
                    st.error(L("select_camper_error"))
                elif file is None:
                    st.error(L("select_file"))
                else:
                    storage.add_documento(cid, tipo, file.name, file.getvalue(), note)
                    st.success(L("doc_uploaded", name=file.name))
                    st.rerun()

    st.markdown("---")
    st.subheader(L("documents_archive"))

    if not db["documenti"]:
        st.write(L("no_document"))
    else:
        cmap = camper_label_map(db)
        for d in sorted(db["documenti"], key=lambda x: x["data_caricamento"], reverse=True):
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    note_part = f" · {d['note']}" if d['note'] else ""
                    st.markdown(
                        f"**{d['tipo']}** — {d['nome_originale']}  \n"
                        f"_{cmap.get(d['camper_id'], '?')}_ · {L('uploaded_on')} "
                        f"{date.fromisoformat(d['data_caricamento']).strftime('%d/%m/%Y')}"
                        f"{note_part}"
                    )
                with col2:
                    path = storage.documento_path(d)
                    if path.exists():
                        st.download_button(
                            L("download"),
                            data=path.read_bytes(),
                            file_name=d["nome_originale"],
                            key=f"dl_{d['id']}",
                        )
                with col3:
                    if st.button("🗑️", key=f"deld_{d['id']}"):
                        storage.delete_documento(d["id"])
                        st.rerun()


# ============================================================
# PAGINA — Statistiche
# ============================================================
elif pagina == "stats":
    st.title(L("stats_title"))
    db = storage.load()

    if not db["campers"]:
        st.info(L("select_camper_first"))
    else:
        scelta = st.selectbox(
            L("camper"),
            [L("all_campers")] + [f"{c['marca']} {c['modello']}" for c in db["campers"]],
        )
        if scelta == L("all_campers"):
            filtro_cid = None
        else:
            filtro_cid = next(c["id"] for c in db["campers"]
                              if f"{c['marca']} {c['modello']}" == scelta)

        def filtra(coll):
            if filtro_cid is None:
                return coll
            return [x for x in coll if x["camper_id"] == filtro_cid]

        st.subheader(L("monthly_costs"))
        eventi = []
        for i in filtra(db["interventi"]):
            eventi.append({"data": i["data"], "categoria": L("maintenance"), "costo": i["costo"]})
        for r in filtra(db["rifornimenti"]):
            eventi.append({"data": r["data"], "categoria": L("fuel_label"), "costo": r["costo"]})
        for v in filtra(db["viaggi"]):
            eventi.append({"data": v["data_inizio"], "categoria": L("trips_label"), "costo": v["costo"]})

        if not eventi:
            st.write(L("no_spending_data"))
        else:
            df_e = pd.DataFrame(eventi)
            df_e["mese"] = pd.to_datetime(df_e["data"]).dt.to_period("M").astype(str)
            piv = df_e.pivot_table(
                index="mese", columns="categoria", values="costo",
                aggfunc="sum", fill_value=0,
            ).sort_index()
            st.bar_chart(piv)

        st.markdown("---")
        st.subheader(L("maintenance_breakdown"))
        ints = filtra(db["interventi"])
        if not ints:
            st.write(L("no_intervention_short"))
        else:
            df_i = pd.DataFrame(ints)
            df_i["categoria_label"] = df_i["categoria"].fillna("int_altro").map(
                lambda k: L(k if k in CATEGORIE_INTERVENTO_KEYS else "int_altro")
            )
            agg = df_i.groupby("categoria_label")["costo"].sum().sort_values(ascending=False)
            st.bar_chart(agg)

        st.markdown("---")
        st.subheader(L("consumption_trend"))
        rifs = filtra(db["rifornimenti"])
        if filtro_cid is None:
            st.caption(L("select_single_camper"))
        elif len(rifs) < 2:
            st.write(L("need_two_refills"))
        else:
            rifs_s = sorted(rifs, key=lambda x: x["km"])
            punti = []
            for prec, succ in zip(rifs_s, rifs_s[1:]):
                delta = succ["km"] - prec["km"]
                if delta > 0 and succ["litri"] > 0:
                    punti.append({
                        "data": succ["data"],
                        "l/100km": (succ["litri"] / delta) * 100,
                    })
            if punti:
                df_c = pd.DataFrame(punti)
                df_c["data"] = pd.to_datetime(df_c["data"])
                df_c = df_c.set_index("data")
                st.line_chart(df_c)


# ============================================================
# PAGINA — Impostazioni
# ============================================================
elif pagina == "settings":
    st.title(L("settings_title"))
    db = storage.load()
    imp = db["impostazioni"]

    # ----- QR per installare la PWA mobile (CamperAppMobile) -----
    st.subheader("📱 " + L("install_pwa_section"))

    import socket
    import io
    import qrcode

    def _detect_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

    local_ip = _detect_local_ip()
    if local_ip is None:
        st.warning(L("phone_no_network"))
    else:
        # Porta del server Flet (mobile/run_qr.py default 8550)
        pwa_port = 8550
        pwa_url = f"http://{local_ip}:{pwa_port}"
        st.caption(L("install_pwa_help"))

        col_qr_pwa, col_info_pwa = st.columns([1, 2])
        with col_qr_pwa:
            img = qrcode.make(pwa_url)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), width=220)
        with col_info_pwa:
            st.code(pwa_url, language=None)
            st.markdown(L("install_pwa_steps"))
            st.caption(L("install_pwa_server_warning"))

    st.markdown("---")

    # ----- LINGUA -----
    st.subheader("🌍 " + L("language"))
    codici = list(LINGUE_DISPONIBILI.keys())
    etichette = [LINGUE_DISPONIBILI[c] for c in codici]
    indice_corrente = codici.index(LANG) if LANG in codici else 0
    nuova_lingua_label = st.selectbox(
        L("language"), etichette, index=indice_corrente, key=f"lang_select_{LANG}",
    )
    nuova_lingua_code = codici[etichette.index(nuova_lingua_label)]
    if nuova_lingua_code != LANG:
        if st.button("💾 " + L("save")):
            storage.update_impostazioni(lingua=nuova_lingua_code)
            st.success(L("language_saved"))
            st.rerun()

    st.markdown("---")

    # ----- VALUTA -----
    st.subheader("💱 " + L("currency"))
    valute = ["EUR", "CHF"]
    valute_labels = [f"{storage.currency_symbol(v)} {v}" for v in valute]
    val_idx = valute.index(VALUTA) if VALUTA in valute else 0
    nuova_valuta_label = st.selectbox(
        L("currency"), valute_labels, index=val_idx, key=f"cur_select_{VALUTA}",
    )
    nuova_valuta = valute[valute_labels.index(nuova_valuta_label)]
    if nuova_valuta != VALUTA:
        if st.button("💾 " + L("save"), key="save_currency_btn"):
            storage.update_impostazioni(valuta=nuova_valuta)
            st.success(L("currency_saved"))
            st.rerun()

    st.markdown("---")
    st.subheader("💬 " + L("nickname"))
    cur_nick = imp.get("nickname", "")
    new_nick = st.text_input(L("nickname"), value=cur_nick, max_chars=24, key="set_nick")
    if new_nick.strip() and new_nick.strip() != cur_nick:
        if st.button("💾 " + L("save_nickname"), key="save_nick_btn"):
            storage.update_impostazioni(nickname=new_nick.strip())
            st.success(L("nickname_saved"))
            st.rerun()

    st.markdown("---")
    st.subheader(L("reminder_section"))
    soglia = st.number_input(
        L("days_before"),
        min_value=1, max_value=365, value=int(imp.get("giorni_promemoria", 30)),
    )
    if soglia != imp.get("giorni_promemoria"):
        if st.button(L("save_threshold")):
            storage.update_impostazioni(giorni_promemoria=int(soglia))
            st.success(L("saved"))
            st.rerun()

    st.markdown("---")
    st.subheader(L("email_section"))
    st.caption(L("email_help"))
    with st.form("smtp_form"):
        email = st.text_input(L("email_dest"), value=imp.get("email", ""))
        col1, col2 = st.columns(2)
        with col1:
            smtp_host = st.text_input("SMTP host", value=imp.get("smtp_host", ""))
            smtp_user = st.text_input("SMTP user", value=imp.get("smtp_user", ""))
        with col2:
            smtp_port = st.number_input("SMTP port", min_value=1, max_value=65535, value=int(imp.get("smtp_port", 587)))
            smtp_pass = st.text_input("SMTP password", value=imp.get("smtp_pass", ""), type="password")
        if st.form_submit_button(L("save_email_config")):
            storage.update_impostazioni(
                email=email, smtp_host=smtp_host, smtp_port=int(smtp_port),
                smtp_user=smtp_user, smtp_pass=smtp_pass,
            )
            st.success(L("config_saved"))
            st.rerun()

    st.markdown("---")
    st.subheader(L("backup_section"))
    st.caption(L("backup_help"))
    import backup as backup_mod

    col_exp, col_imp = st.columns(2)
    with col_exp:
        st.markdown(f"**{L('backup_export')}**")
        if st.button(L("backup_prepare"), key="bk_prep"):
            fname, data = backup_mod.export_zip()
            st.session_state["_backup_data"] = data
            st.session_state["_backup_name"] = fname
        if st.session_state.get("_backup_data"):
            st.download_button(
                L("backup_download"),
                data=st.session_state["_backup_data"],
                file_name=st.session_state["_backup_name"],
                mime="application/zip",
                key="bk_dl",
            )

    with col_imp:
        st.markdown(f"**{L('backup_import')}**")
        st.caption(L("backup_import_help"))
        up = st.file_uploader(L("backup_zip_file"), type=["zip"], key="bk_up")
        if up is not None:
            confermo = st.checkbox(L("backup_import_confirm"), key="bk_cnf")
            if confermo and st.button(L("backup_restore_now"), key="bk_run"):
                try:
                    backup_mod.import_zip(up.getvalue())
                    st.session_state.pop("_backup_data", None)
                    st.success(L("backup_imported"))
                    st.rerun()
                except ValueError as e:
                    st.error(L("backup_invalid", err=str(e)))

    st.markdown("---")
    st.subheader(L("desktop_section"))
    st.caption(L("desktop_help"))
    import desktop_notif
    if not desktop_notif.is_supported():
        st.info(L("desktop_unsupported"))
    else:
        auto_d = bool(imp.get("auto_invio_desktop", False))
        nuovo_d = st.checkbox(
            L("auto_desktop_toggle"), value=auto_d,
            help=L("auto_desktop_help"),
        )
        if nuovo_d != auto_d:
            storage.update_impostazioni(auto_invio_desktop=bool(nuovo_d))
            st.rerun()

        ultimo_d = imp.get("ultimo_invio_desktop") or ""
        if ultimo_d:
            try:
                ultimo_d_fmt = datetime.fromisoformat(ultimo_d).strftime("%d/%m/%Y %H:%M")
                st.caption(L("last_sent_on", when=ultimo_d_fmt))
            except ValueError:
                pass
        else:
            st.caption(L("never_sent"))

        if st.button(L("desktop_test"), key="dt_test"):
            err = desktop_notif.show_toast(
                L("toast_test_title"), L("toast_test_body"),
            )
            if err:
                st.error(L("send_error", err=err))
            else:
                st.success(L("desktop_test_sent"))

    st.markdown("---")
    st.subheader(L("send_reminders_now"))
    import notifications

    if not notifications.is_smtp_configured(db):
        st.info(L("configure_email_first"))
    else:
        soglia_v = imp.get("giorni_promemoria", 30)
        imminenti = notifications.imminent_deadlines(db)

        # Toggle invio automatico
        auto_corrente = bool(imp.get("auto_invio", False))
        nuovo_auto = st.checkbox(
            L("auto_email_toggle"), value=auto_corrente,
            help=L("auto_email_help"),
        )
        if nuovo_auto != auto_corrente:
            storage.update_impostazioni(auto_invio=bool(nuovo_auto))
            st.rerun()

        # Ultimo invio
        ultimo = imp.get("ultimo_invio") or ""
        if ultimo:
            try:
                ultimo_fmt = datetime.fromisoformat(ultimo).strftime("%d/%m/%Y %H:%M")
                st.caption(L("last_sent_on", when=ultimo_fmt))
            except ValueError:
                pass
        else:
            st.caption(L("never_sent"))

        if not imminenti:
            st.success(L("no_upcoming_to_notify"))
        else:
            st.write(L("found_n_deadlines", n=len(imminenti), days=soglia_v))
            if st.button(L("send_now")):
                n_sent, err = notifications.send_reminders(LANG)
                if err and err != "SMTP_NOT_CONFIGURED":
                    st.error(L("send_error", err=err))
                else:
                    st.success(L("email_sent_to", to=imp["email"]))
                    st.rerun()
