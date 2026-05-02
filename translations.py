"""Stringhe localizzate per CAMPERappPLUS. Lingue: it, en, de, fr, es."""

LINGUE_DISPONIBILI = {
    "it": "🇮🇹 Italiano",
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
}

TRANSLATIONS = {
    # ---------- Sidebar ----------
    "sidebar_caption": {
        "it": "Prototipo MVP — dati salvati in data/camper.json",
        "en": "MVP prototype — data saved in data/camper.json",
        "de": "MVP-Prototyp — Daten gespeichert in data/camper.json",
        "fr": "Prototype MVP — données dans data/camper.json",
        "es": "Prototipo MVP — datos guardados en data/camper.json",
    },
    "section": {
        "it": "Sezione", "en": "Section", "de": "Bereich",
        "fr": "Section", "es": "Sección",
    },
    "page_home": {
        "it": "🏠 Inizio", "en": "🏠 Dashboard", "de": "🏠 Startseite",
        "fr": "🏠 Accueil", "es": "🏠 Inicio",
    },
    "page_campers": {
        "it": "🚐 I miei camper", "en": "🚐 My campers", "de": "🚐 Meine Wohnmobile",
        "fr": "🚐 Mes camping-cars", "es": "🚐 Mis autocaravanas",
    },
    "page_deadlines": {
        "it": "⏰ Scadenze", "en": "⏰ Deadlines", "de": "⏰ Fristen",
        "fr": "⏰ Échéances", "es": "⏰ Vencimientos",
    },
    "page_logbook": {
        "it": "🔧 Libretto digitale", "en": "🔧 Digital logbook",
        "de": "🔧 Digitales Wartungsheft", "fr": "🔧 Carnet d'entretien",
        "es": "🔧 Libro digital",
    },
    "page_trips": {
        "it": "🗺️ Diario viaggi", "en": "🗺️ Trip diary", "de": "🗺️ Reisetagebuch",
        "fr": "🗺️ Journal de voyage", "es": "🗺️ Diario de viajes",
    },
    "page_fuel": {
        "it": "⛽ Rifornimenti", "en": "⛽ Fuel", "de": "⛽ Tankstopps",
        "fr": "⛽ Carburant", "es": "⛽ Repostajes",
    },
    "page_checklist": {
        "it": "✅ Liste controlli", "en": "✅ Checklists", "de": "✅ Checklisten",
        "fr": "✅ Listes de contrôle", "es": "✅ Listas de control",
    },
    "page_documents": {
        "it": "📎 Documenti", "en": "📎 Files & docs", "de": "📎 Dokumente",
        "fr": "📎 Mes documents", "es": "📎 Documentos",
    },
    "page_stats": {
        "it": "📊 Statistiche", "en": "📊 Statistics", "de": "📊 Statistiken",
        "fr": "📊 Statistiques", "es": "📊 Estadísticas",
    },
    "page_settings": {
        "it": "⚙️ Impostazioni", "en": "⚙️ Settings", "de": "⚙️ Einstellungen",
        "fr": "⚙️ Paramètres", "es": "⚙️ Ajustes",
    },
    "page_map": {
        "it": "📍 Mappa live", "en": "📍 Live map", "de": "📍 Live-Karte",
        "fr": "📍 Carte live", "es": "📍 Mapa en vivo",
    },
    "page_chat": {
        "it": "💬 Chat", "en": "💬 Chat", "de": "💬 Chat",
        "fr": "💬 Chat", "es": "💬 Chat",
    },
    "phone_section": {
        "it": "📱 Apri sul telefono", "en": "📱 Open on phone",
        "de": "📱 Am Handy öffnen", "fr": "📱 Ouvrir sur téléphone",
        "es": "📱 Abrir en el móvil",
    },
    "phone_help": {
        "it": "Scansiona il QR con il telefono (deve essere sulla stessa Wi-Fi del PC).",
        "en": "Scan the QR with your phone (must be on the same Wi-Fi as the PC).",
        "de": "QR mit dem Handy scannen (muss im gleichen WLAN wie der PC sein).",
        "fr": "Scannez le QR avec le téléphone (même Wi-Fi que le PC).",
        "es": "Escanea el QR con el móvil (misma Wi-Fi que el PC).",
    },
    "phone_no_network": {
        "it": "Impossibile rilevare l'IP locale. Usa l'URL mostrato nel terminale di Streamlit.",
        "en": "Unable to detect local IP. Use the URL shown in the Streamlit terminal.",
        "de": "Lokale IP nicht erkennbar. URL aus dem Streamlit-Terminal verwenden.",
        "fr": "IP locale non détectable. Utilisez l'URL affichée dans le terminal Streamlit.",
        "es": "No se detecta la IP local. Usa la URL del terminal de Streamlit.",
    },
    "phone_geo_warning": {
        "it": "⚠️ La geolocalizzazione non funziona via IP locale (serve HTTPS). "
              "Sul telefono usa il pulsante \"Apri Google Maps\".",
        "en": "⚠️ Geolocation doesn't work over local IP (HTTPS required). "
              "On your phone use the \"Open Google Maps\" button.",
        "de": "⚠️ Geolokalisierung funktioniert nicht über lokale IP (HTTPS nötig). "
              "Am Handy den Button \"Google Maps öffnen\" verwenden.",
        "fr": "⚠️ La géolocalisation ne marche pas via IP locale (HTTPS requis). "
              "Sur le téléphone utilisez \"Ouvrir Google Maps\".",
        "es": "⚠️ La geolocalización no funciona por IP local (requiere HTTPS). "
              "En el móvil usa el botón \"Abrir Google Maps\".",
    },

    # ---------- Comuni ----------
    "camper": {"it": "Camper", "en": "Camper", "de": "Wohnmobil", "fr": "Camping-car", "es": "Autocaravana"},
    "save": {"it": "Salva", "en": "Save", "de": "Speichern", "fr": "Enregistrer", "es": "Guardar"},
    "delete": {"it": "Elimina", "en": "Delete", "de": "Löschen", "fr": "Supprimer", "es": "Eliminar"},
    "add": {"it": "Aggiungi", "en": "Add", "de": "Hinzufügen", "fr": "Ajouter", "es": "Añadir"},
    "date": {"it": "Data", "en": "Date", "de": "Datum", "fr": "Date", "es": "Fecha"},
    "type": {"it": "Tipo", "en": "Type", "de": "Typ", "fr": "Type", "es": "Tipo"},
    "notes": {"it": "Note", "en": "Notes", "de": "Notizen", "fr": "Notes", "es": "Notas"},
    "notes_optional": {"it": "Note (opzionale)", "en": "Notes (optional)", "de": "Notizen (optional)", "fr": "Notes (optionnel)", "es": "Notas (opcional)"},
    "km": {"it": "Km", "en": "Km", "de": "Km", "fr": "Km", "es": "Km"},
    "cost": {"it": "Costo", "en": "Cost", "de": "Kosten", "fr": "Coût", "es": "Coste"},
    "cost_eur": {"it": "Costo ({sym})", "en": "Cost ({sym})", "de": "Kosten ({sym})", "fr": "Coût ({sym})", "es": "Coste ({sym})"},
    "description": {"it": "Descrizione", "en": "Description", "de": "Beschreibung", "fr": "Description", "es": "Descripción"},
    "select_camper_first": {
        "it": "Aggiungi prima un camper nella sezione 'I miei camper'.",
        "en": "Add a camper first in the 'My campers' section.",
        "de": "Bitte erst ein Wohnmobil im Bereich 'Meine Wohnmobile' anlegen.",
        "fr": "Ajoutez d'abord un camping-car dans 'Mes camping-cars'.",
        "es": "Añade primero una autocaravana en 'Mis autocaravanas'.",
    },
    "select_camper_error": {
        "it": "Seleziona un camper.", "en": "Select a camper.",
        "de": "Wähle ein Wohnmobil.", "fr": "Sélectionnez un camping-car.",
        "es": "Selecciona una autocaravana.",
    },
    "total": {"it": "Totale", "en": "Total", "de": "Gesamt", "fr": "Total", "es": "Total"},

    # ---------- Home ----------
    "welcome": {
        "it": "Benvenuto in CAMPERappPLUS", "en": "Welcome to CAMPERappPLUS",
        "de": "Willkommen bei CAMPERappPLUS", "fr": "Bienvenue dans CAMPERappPLUS",
        "es": "Bienvenido a CAMPERappPLUS",
    },
    "campers": {"it": "Camper", "en": "Campers", "de": "Wohnmobile", "fr": "Camping-cars", "es": "Autocaravanas"},
    "deadlines": {"it": "Scadenze", "en": "Deadlines", "de": "Fristen", "fr": "Échéances", "es": "Vencimientos"},
    "interventions": {"it": "Interventi", "en": "Interventions", "de": "Wartungen", "fr": "Interventions", "es": "Intervenciones"},
    "trips": {"it": "Viaggi", "en": "Trips", "de": "Reisen", "fr": "Voyages", "es": "Viajes"},
    "start_add_camper": {
        "it": "Inizia aggiungendo un camper nella sezione **I miei camper**.",
        "en": "Start by adding a camper in **My campers**.",
        "de": "Beginne mit dem Anlegen eines Wohnmobils unter **Meine Wohnmobile**.",
        "fr": "Commencez par ajouter un camping-car dans **Mes camping-cars**.",
        "es": "Empieza añadiendo una autocaravana en **Mis autocaravanas**.",
    },
    "deadlines_within_days": {
        "it": "⏰ Scadenze entro {n} giorni", "en": "⏰ Deadlines within {n} days",
        "de": "⏰ Fristen innerhalb {n} Tagen", "fr": "⏰ Échéances dans {n} jours",
        "es": "⏰ Vencimientos en {n} días",
    },
    "no_upcoming": {
        "it": "Nessuna scadenza imminente. 🎉", "en": "No upcoming deadlines. 🎉",
        "de": "Keine anstehenden Fristen. 🎉", "fr": "Aucune échéance imminente. 🎉",
        "es": "Sin vencimientos próximos. 🎉",
    },
    "expired": {"it": "Scaduta", "en": "Expired", "de": "Abgelaufen", "fr": "Expirée", "es": "Vencida"},
    "upcoming": {"it": "In arrivo", "en": "Upcoming", "de": "Anstehend", "fr": "À venir", "es": "Próxima"},
    "ok": {"it": "OK", "en": "OK", "de": "OK", "fr": "OK", "es": "OK"},
    "expired_for_days": {"it": "scaduta da {n} gg", "en": "expired {n} days ago",
        "de": "vor {n} Tagen abgelaufen", "fr": "expirée depuis {n} j",
        "es": "vencida hace {n} días"},
    "in_n_days": {"it": "tra {n} gg", "en": "in {n} days",
        "de": "in {n} Tagen", "fr": "dans {n} j", "es": "en {n} días"},
    "total_costs_per_camper": {
        "it": "💶 Costi totali per camper", "en": "💶 Total costs per camper",
        "de": "💶 Gesamtkosten pro Wohnmobil", "fr": "💶 Coûts totaux par camping-car",
        "es": "💶 Costes totales por autocaravana",
    },
    "maintenance": {"it": "Manutenzione", "en": "Maintenance", "de": "Wartung", "fr": "Entretien", "es": "Mantenimiento"},
    "fuel_label": {"it": "Carburante", "en": "Fuel", "de": "Kraftstoff", "fr": "Carburant", "es": "Combustible"},
    "trips_label": {"it": "Viaggi", "en": "Trips", "de": "Reisen", "fr": "Voyages", "es": "Viajes"},

    # ---------- Camper page ----------
    "my_campers": {"it": "I miei camper", "en": "My campers", "de": "Meine Wohnmobile", "fr": "Mes camping-cars", "es": "Mis autocaravanas"},
    "add_camper": {"it": "➕ Aggiungi camper", "en": "➕ Add camper", "de": "➕ Wohnmobil hinzufügen", "fr": "➕ Ajouter un camping-car", "es": "➕ Añadir autocaravana"},
    "brand": {"it": "Marca", "en": "Brand", "de": "Marke", "fr": "Marque", "es": "Marca"},
    "model": {"it": "Modello", "en": "Model", "de": "Modell", "fr": "Modèle", "es": "Modelo"},
    "year": {"it": "Anno", "en": "Year", "de": "Baujahr", "fr": "Année", "es": "Año"},
    "plate": {"it": "Targa", "en": "Plate", "de": "Kennzeichen", "fr": "Immatriculation", "es": "Matrícula"},
    "current_km": {"it": "Km attuali", "en": "Current km", "de": "Aktuelle km", "fr": "Km actuels", "es": "Km actuales"},
    "save_camper": {"it": "Salva camper", "en": "Save camper", "de": "Wohnmobil speichern", "fr": "Enregistrer", "es": "Guardar autocaravana"},
    "fill_required": {
        "it": "Compila marca, modello e targa.", "en": "Fill in brand, model and plate.",
        "de": "Marke, Modell und Kennzeichen ausfüllen.",
        "fr": "Renseignez marque, modèle et immatriculation.",
        "es": "Rellena marca, modelo y matrícula.",
    },
    "camper_added": {
        "it": "Camper {name} aggiunto!", "en": "Camper {name} added!",
        "de": "Wohnmobil {name} hinzugefügt!", "fr": "Camping-car {name} ajouté!",
        "es": "Autocaravana {name} añadida!",
    },
    "my_fleet": {"it": "La mia flotta", "en": "My fleet", "de": "Meine Flotte", "fr": "Ma flotte", "es": "Mi flota"},
    "no_camper_yet": {"it": "Nessun camper ancora.", "en": "No camper yet.", "de": "Noch kein Wohnmobil.", "fr": "Aucun camping-car.", "es": "Aún sin autocaravana."},
    "update_km": {"it": "Aggiorna km", "en": "Update km", "de": "Km aktualisieren", "fr": "Mettre à jour km", "es": "Actualizar km"},
    "save_new_km": {"it": "Salva nuovi km", "en": "Save new km", "de": "Neue km speichern", "fr": "Enregistrer", "es": "Guardar km"},

    # ---------- Deadlines ----------
    "add_deadline": {"it": "➕ Aggiungi scadenza", "en": "➕ Add deadline", "de": "➕ Frist hinzufügen", "fr": "➕ Ajouter une échéance", "es": "➕ Añadir vencimiento"},
    "deadline_date": {"it": "Data scadenza", "en": "Deadline date", "de": "Fälligkeitsdatum", "fr": "Date d'échéance", "es": "Fecha de vencimiento"},
    "save_deadline": {"it": "Salva scadenza", "en": "Save deadline", "de": "Frist speichern", "fr": "Enregistrer", "es": "Guardar"},
    "deadline_added": {"it": "Scadenza aggiunta!", "en": "Deadline added!", "de": "Frist hinzugefügt!", "fr": "Échéance ajoutée!", "es": "Vencimiento añadido!"},
    "upcoming_deadlines": {"it": "Prossime scadenze", "en": "Upcoming deadlines", "de": "Anstehende Fristen", "fr": "Prochaines échéances", "es": "Próximos vencimientos"},
    "no_deadline": {"it": "Nessuna scadenza registrata.", "en": "No deadlines yet.", "de": "Keine Fristen.", "fr": "Aucune échéance.", "es": "Sin vencimientos."},
    "status": {"it": "Stato", "en": "Status", "de": "Status", "fr": "État", "es": "Estado"},
    "days": {"it": "Giorni", "en": "Days", "de": "Tage", "fr": "Jours", "es": "Días"},
    "delete_deadline_section": {"it": "Elimina una scadenza", "en": "Delete a deadline", "de": "Frist löschen", "fr": "Supprimer une échéance", "es": "Eliminar un vencimiento"},
    # tipi scadenza
    "tipo_revisione": {"it": "Revisione", "en": "Inspection", "de": "TÜV", "fr": "Contrôle technique", "es": "Inspección"},
    "tipo_vignetta": {"it": "Vignetta autostradale", "en": "Highway vignette", "de": "Vignette", "fr": "Vignette autoroute", "es": "Viñeta autopista"},
    "tipo_assicurazione": {"it": "Assicurazione", "en": "Insurance", "de": "Versicherung", "fr": "Assurance", "es": "Seguro"},
    "tipo_bombole": {"it": "Bombole gas", "en": "Gas bottles", "de": "Gasflaschen", "fr": "Bouteilles de gaz", "es": "Bombonas de gas"},
    "tipo_tagliando": {"it": "Tagliando", "en": "Service", "de": "Inspektion", "fr": "Révision", "es": "Revisión"},
    "tipo_bollo": {"it": "Bollo", "en": "Road tax", "de": "Kfz-Steuer", "fr": "Taxe", "es": "Impuesto"},
    "tipo_altro": {"it": "Altro", "en": "Other", "de": "Sonstiges", "fr": "Autre", "es": "Otro"},

    # ---------- Logbook ----------
    "add_intervention": {"it": "➕ Registra intervento", "en": "➕ Log intervention", "de": "➕ Wartung erfassen", "fr": "➕ Enregistrer intervention", "es": "➕ Registrar intervención"},
    "intervention_desc": {"it": "Descrizione intervento", "en": "Intervention description", "de": "Beschreibung der Wartung", "fr": "Description", "es": "Descripción"},
    "save_intervention": {"it": "Salva intervento", "en": "Save intervention", "de": "Speichern", "fr": "Enregistrer", "es": "Guardar"},
    "intervention_saved": {"it": "Intervento registrato!", "en": "Intervention saved!", "de": "Wartung gespeichert!", "fr": "Intervention enregistrée!", "es": "Intervención guardada!"},
    "fill_description": {"it": "Inserisci una descrizione.", "en": "Enter a description.", "de": "Bitte Beschreibung eingeben.", "fr": "Saisissez une description.", "es": "Introduce una descripción."},
    "history_interventions": {"it": "Storico interventi", "en": "Intervention history", "de": "Wartungshistorie", "fr": "Historique", "es": "Historial"},
    "no_intervention": {"it": "Nessun intervento registrato.", "en": "No interventions yet.", "de": "Keine Wartungen.", "fr": "Aucune intervention.", "es": "Sin intervenciones."},
    "total_maintenance": {"it": "Totale speso in manutenzione", "en": "Total spent on maintenance", "de": "Wartungskosten gesamt", "fr": "Total entretien", "es": "Total mantenimiento"},
    "export_pdf_logbook": {"it": "📄 Esporta libretto in PDF", "en": "📄 Export logbook to PDF", "de": "📄 Wartungsheft als PDF", "fr": "📄 Exporter en PDF", "es": "📄 Exportar a PDF"},
    "camper_to_export": {"it": "Camper da esportare", "en": "Camper to export", "de": "Wohnmobil exportieren", "fr": "Camping-car à exporter", "es": "Autocaravana a exportar"},
    "download_pdf": {"it": "⬇️ Scarica PDF", "en": "⬇️ Download PDF", "de": "⬇️ PDF herunterladen", "fr": "⬇️ Télécharger PDF", "es": "⬇️ Descargar PDF"},
    "delete_intervention_section": {"it": "Elimina un intervento", "en": "Delete an intervention", "de": "Wartung löschen", "fr": "Supprimer une intervention", "es": "Eliminar una intervención"},

    # ---------- Trips ----------
    "trip_diary_title": {"it": "Diario viaggi", "en": "Trip diary", "de": "Reisetagebuch", "fr": "Journal de voyage", "es": "Diario de viajes"},
    "add_trip": {"it": "➕ Registra viaggio", "en": "➕ Log trip", "de": "➕ Reise erfassen", "fr": "➕ Enregistrer voyage", "es": "➕ Registrar viaje"},
    "departure_date": {"it": "Data partenza", "en": "Departure date", "de": "Abreisedatum", "fr": "Date de départ", "es": "Fecha salida"},
    "destination": {"it": "Destinazione", "en": "Destination", "de": "Reiseziel", "fr": "Destination", "es": "Destino"},
    "km_done": {"it": "Km percorsi", "en": "Km driven", "de": "Gefahrene km", "fr": "Km parcourus", "es": "Km recorridos"},
    "return_date": {"it": "Data ritorno", "en": "Return date", "de": "Rückkehrdatum", "fr": "Date retour", "es": "Fecha regreso"},
    "total_cost_eur": {"it": "Costo totale ({sym})", "en": "Total cost ({sym})", "de": "Gesamtkosten ({sym})", "fr": "Coût total ({sym})", "es": "Coste total ({sym})"},
    "save_trip": {"it": "Salva viaggio", "en": "Save trip", "de": "Reise speichern", "fr": "Enregistrer", "es": "Guardar"},
    "trip_saved": {"it": "Viaggio registrato!", "en": "Trip saved!", "de": "Reise gespeichert!", "fr": "Voyage enregistré!", "es": "Viaje guardado!"},
    "fill_destination": {"it": "Inserisci la destinazione.", "en": "Enter destination.", "de": "Bitte Reiseziel eingeben.", "fr": "Saisissez la destination.", "es": "Introduce el destino."},
    "return_before_departure": {
        "it": "La data di ritorno è precedente alla partenza.",
        "en": "Return date is before departure.",
        "de": "Rückkehrdatum liegt vor der Abreise.",
        "fr": "Le retour est avant le départ.",
        "es": "La fecha de regreso es anterior a la salida.",
    },
    "my_trips": {"it": "I miei viaggi", "en": "My trips", "de": "Meine Reisen", "fr": "Mes voyages", "es": "Mis viajes"},
    "no_trip": {"it": "Nessun viaggio ancora.", "en": "No trips yet.", "de": "Noch keine Reisen.", "fr": "Aucun voyage.", "es": "Sin viajes."},
    "from": {"it": "Dal", "en": "From", "de": "Von", "fr": "Du", "es": "Desde"},
    "to": {"it": "Al", "en": "To", "de": "Bis", "fr": "Au", "es": "Hasta"},
    "total_trips": {"it": "Viaggi totali", "en": "Total trips", "de": "Reisen gesamt", "fr": "Voyages au total", "es": "Viajes totales"},
    "total_km": {"it": "Km totali", "en": "Total km", "de": "Km gesamt", "fr": "Km au total", "es": "Km totales"},
    "total_trip_spending": {"it": "Spesa totale viaggi", "en": "Total trip spending", "de": "Reisekosten gesamt", "fr": "Dépenses voyages", "es": "Gasto total"},
    "delete_trip_section": {"it": "Elimina un viaggio", "en": "Delete a trip", "de": "Reise löschen", "fr": "Supprimer un voyage", "es": "Eliminar un viaje"},

    # ---------- Fuel ----------
    "fuel_title": {"it": "Rifornimenti carburante", "en": "Fuel refills", "de": "Tankstopps", "fr": "Pleins carburant", "es": "Repostajes"},
    "add_fuel": {"it": "➕ Aggiungi rifornimento", "en": "➕ Add refill", "de": "➕ Tankstopp hinzufügen", "fr": "➕ Ajouter plein", "es": "➕ Añadir repostaje"},
    "odometer_km": {"it": "Km contachilometri", "en": "Odometer km", "de": "Kilometerstand", "fr": "Km compteur", "es": "Km cuentakilómetros"},
    "liters": {"it": "Litri", "en": "Liters", "de": "Liter", "fr": "Litres", "es": "Litros"},
    "station": {"it": "Distributore", "en": "Station", "de": "Tankstelle", "fr": "Station", "es": "Gasolinera"},
    "save_fuel": {"it": "Salva rifornimento", "en": "Save refill", "de": "Speichern", "fr": "Enregistrer", "es": "Guardar"},
    "fuel_saved": {"it": "Rifornimento salvato!", "en": "Refill saved!", "de": "Tankstopp gespeichert!", "fr": "Plein enregistré!", "es": "Repostaje guardado!"},
    "fill_km_liters": {"it": "Inserisci km e litri validi.", "en": "Enter valid km and liters.", "de": "Gültige km und Liter eingeben.", "fr": "Saisissez km et litres valides.", "es": "Introduce km y litros válidos."},
    "fuel_history": {"it": "Storico rifornimenti", "en": "Refill history", "de": "Tankhistorie", "fr": "Historique pleins", "es": "Historial repostajes"},
    "no_fuel": {"it": "Nessun rifornimento ancora.", "en": "No refills yet.", "de": "Noch keine Tankstopps.", "fr": "Aucun plein.", "es": "Sin repostajes."},
    "consumption_l100": {"it": "Consumo l/100km", "en": "Consumption l/100km", "de": "Verbrauch l/100km", "fr": "Conso l/100km", "es": "Consumo l/100km"},
    "avg_consumption": {"it": "Consumo medio per camper", "en": "Average consumption per camper", "de": "Durchschnittsverbrauch pro Wohnmobil", "fr": "Consommation moyenne par camping-car", "es": "Consumo medio por autocaravana"},
    "delete_fuel_section": {"it": "Elimina un rifornimento", "en": "Delete a refill", "de": "Tankstopp löschen", "fr": "Supprimer un plein", "es": "Eliminar un repostaje"},

    # ---------- Checklist ----------
    "checklist_title": {"it": "Liste controlli", "en": "Checklists", "de": "Checklisten", "fr": "Listes de contrôle", "es": "Listas de control"},
    "category": {"it": "Categoria", "en": "Category", "de": "Kategorie", "fr": "Catégorie", "es": "Categoría"},
    "cat_partenza": {"it": "Partenza", "en": "Departure", "de": "Abfahrt", "fr": "Départ", "es": "Salida"},
    "cat_apertura": {"it": "Apertura stagione", "en": "Season opening", "de": "Saisonbeginn", "fr": "Ouverture saison", "es": "Apertura temporada"},
    "cat_chiusura": {"it": "Chiusura stagione", "en": "Season closing", "de": "Saisonende", "fr": "Fermeture saison", "es": "Cierre temporada"},
    "cat_manutenzione": {"it": "Manutenzione", "en": "Maintenance", "de": "Wartung", "fr": "Entretien", "es": "Mantenimiento"},
    "new_item": {"it": "Nuova voce", "en": "New item", "de": "Neuer Eintrag", "fr": "Nouvel élément", "es": "Nuevo elemento"},
    "no_item_for_category": {
        "it": "Nessuna voce per categoria '{cat}'.",
        "en": "No items for category '{cat}'.",
        "de": "Keine Einträge für Kategorie '{cat}'.",
        "fr": "Aucun élément pour la catégorie '{cat}'.",
        "es": "Sin elementos para la categoría '{cat}'.",
    },
    "n_completed": {
        "it": "{done}/{total} completate", "en": "{done}/{total} completed",
        "de": "{done}/{total} erledigt", "fr": "{done}/{total} terminés",
        "es": "{done}/{total} completados",
    },
    "reset_category": {"it": "🔄 Reset categoria", "en": "🔄 Reset category", "de": "🔄 Kategorie zurücksetzen", "fr": "🔄 Réinitialiser", "es": "🔄 Reiniciar"},

    # ---------- Documents ----------
    "documents_title": {"it": "Documenti", "en": "Documents", "de": "Dokumente", "fr": "Documents", "es": "Documentos"},
    "upload_document": {"it": "➕ Carica documento", "en": "➕ Upload document", "de": "➕ Dokument hochladen", "fr": "➕ Télécharger document", "es": "➕ Subir documento"},
    "doc_type": {"it": "Tipo documento", "en": "Document type", "de": "Dokumenttyp", "fr": "Type de document", "es": "Tipo de documento"},
    "doc_libretto": {"it": "Libretto", "en": "Vehicle papers", "de": "Fahrzeugschein", "fr": "Carte grise", "es": "Permiso"},
    "doc_assicurazione": {"it": "Assicurazione", "en": "Insurance", "de": "Versicherung", "fr": "Assurance", "es": "Seguro"},
    "doc_revisione": {"it": "Revisione", "en": "Inspection", "de": "TÜV", "fr": "Contrôle technique", "es": "Inspección"},
    "doc_bollo": {"it": "Bollo", "en": "Road tax", "de": "Kfz-Steuer", "fr": "Taxe", "es": "Impuesto"},
    "doc_ricevuta": {"it": "Ricevuta intervento", "en": "Service receipt", "de": "Werkstattrechnung", "fr": "Reçu intervention", "es": "Recibo intervención"},
    "doc_manuale": {"it": "Manuale", "en": "Manual", "de": "Handbuch", "fr": "Manuel", "es": "Manual"},
    "doc_foto": {"it": "Foto", "en": "Photo", "de": "Foto", "fr": "Photo", "es": "Foto"},
    "doc_altro": {"it": "Altro", "en": "Other", "de": "Sonstiges", "fr": "Autre", "es": "Otro"},
    "file": {"it": "File", "en": "File", "de": "Datei", "fr": "Fichier", "es": "Archivo"},
    "upload": {"it": "Carica", "en": "Upload", "de": "Hochladen", "fr": "Télécharger", "es": "Subir"},
    "select_file": {"it": "Seleziona un file.", "en": "Select a file.", "de": "Datei auswählen.", "fr": "Sélectionnez un fichier.", "es": "Selecciona un archivo."},
    "doc_uploaded": {
        "it": "Documento '{name}' caricato!", "en": "Document '{name}' uploaded!",
        "de": "Dokument '{name}' hochgeladen!", "fr": "Document '{name}' téléchargé!",
        "es": "Documento '{name}' subido!",
    },
    "documents_archive": {"it": "Archivio documenti", "en": "Documents archive", "de": "Dokumentenarchiv", "fr": "Archive documents", "es": "Archivo documentos"},
    "no_document": {"it": "Nessun documento caricato.", "en": "No documents uploaded.", "de": "Keine Dokumente.", "fr": "Aucun document.", "es": "Sin documentos."},
    "uploaded_on": {"it": "caricato il", "en": "uploaded on", "de": "hochgeladen am", "fr": "téléchargé le", "es": "subido el"},
    "download": {"it": "⬇️ Scarica", "en": "⬇️ Download", "de": "⬇️ Herunterladen", "fr": "⬇️ Télécharger", "es": "⬇️ Descargar"},

    # ---------- Stats ----------
    "stats_title": {"it": "Statistiche", "en": "Statistics", "de": "Statistiken", "fr": "Statistiques", "es": "Estadísticas"},
    "all_campers": {"it": "— Tutti —", "en": "— All —", "de": "— Alle —", "fr": "— Tous —", "es": "— Todos —"},
    "monthly_costs": {"it": "Costi mensili", "en": "Monthly costs", "de": "Monatliche Kosten", "fr": "Coûts mensuels", "es": "Costes mensuales"},
    "no_spending_data": {"it": "Nessun dato di spesa ancora.", "en": "No spending data yet.", "de": "Noch keine Ausgabedaten.", "fr": "Aucune dépense.", "es": "Sin datos de gasto."},
    "maintenance_breakdown": {"it": "Ripartizione manutenzione", "en": "Maintenance breakdown", "de": "Wartungsaufteilung", "fr": "Répartition entretien", "es": "Reparto mantenimiento"},
    "no_intervention_short": {"it": "Nessun intervento.", "en": "No interventions.", "de": "Keine Wartungen.", "fr": "Aucune intervention.", "es": "Sin intervenciones."},
    "consumption_trend": {"it": "Andamento consumo (l/100km)", "en": "Consumption trend (l/100km)", "de": "Verbrauchsverlauf (l/100km)", "fr": "Évolution conso (l/100km)", "es": "Evolución consumo (l/100km)"},
    "select_single_camper": {
        "it": "Seleziona un singolo camper per vedere il consumo nel tempo.",
        "en": "Select a single camper to see consumption over time.",
        "de": "Wähle ein einzelnes Wohnmobil für den Verbrauchsverlauf.",
        "fr": "Sélectionnez un seul camping-car pour voir l'évolution.",
        "es": "Selecciona una sola autocaravana para ver el consumo.",
    },
    "need_two_refills": {
        "it": "Servono almeno 2 rifornimenti.",
        "en": "At least 2 refills needed.",
        "de": "Mindestens 2 Tankstopps nötig.",
        "fr": "Au moins 2 pleins requis.",
        "es": "Se necesitan al menos 2 repostajes.",
    },

    # ---------- Settings ----------
    "settings_title": {"it": "Impostazioni", "en": "Settings", "de": "Einstellungen", "fr": "Paramètres", "es": "Ajustes"},
    "language": {"it": "Lingua", "en": "Language", "de": "Sprache", "fr": "Langue", "es": "Idioma"},
    "language_saved": {
        "it": "Lingua aggiornata.", "en": "Language updated.",
        "de": "Sprache aktualisiert.", "fr": "Langue mise à jour.",
        "es": "Idioma actualizado.",
    },
    "currency": {"it": "Valuta", "en": "Currency", "de": "Währung", "fr": "Devise", "es": "Moneda"},
    "currency_saved": {
        "it": "Valuta aggiornata.", "en": "Currency updated.",
        "de": "Währung aktualisiert.", "fr": "Devise mise à jour.",
        "es": "Moneda actualizada.",
    },
    "reminder_section": {"it": "Promemoria scadenze", "en": "Deadline reminders", "de": "Fristen-Erinnerungen", "fr": "Rappels d'échéance", "es": "Recordatorios"},
    "days_before": {
        "it": "Giorni prima della scadenza per la notifica",
        "en": "Days before deadline for notification",
        "de": "Tage vor Frist für Benachrichtigung",
        "fr": "Jours avant l'échéance pour la notification",
        "es": "Días antes del vencimiento para la notificación",
    },
    "save_threshold": {"it": "💾 Salva soglia", "en": "💾 Save threshold", "de": "💾 Schwelle speichern", "fr": "💾 Enregistrer seuil", "es": "💾 Guardar umbral"},
    "saved": {"it": "Salvato.", "en": "Saved.", "de": "Gespeichert.", "fr": "Enregistré.", "es": "Guardado."},
    "email_section": {"it": "Notifiche email (opzionale)", "en": "Email notifications (optional)", "de": "E-Mail-Benachrichtigungen (optional)", "fr": "Notifications email (optionnel)", "es": "Notificaciones email (opcional)"},
    "email_help": {
        "it": "Configura il tuo SMTP per ricevere un'email con le scadenze imminenti. Per Gmail usa una *App Password*.",
        "en": "Configure SMTP to receive emails with upcoming deadlines. For Gmail use an *App Password*.",
        "de": "SMTP konfigurieren, um E-Mails mit anstehenden Fristen zu erhalten. Bei Gmail ein *App-Passwort* verwenden.",
        "fr": "Configurez SMTP pour recevoir un email avec les échéances. Pour Gmail utilisez un *mot de passe d'application*.",
        "es": "Configura SMTP para recibir emails con vencimientos. Para Gmail usa una *contraseña de aplicación*.",
    },
    "email_dest": {"it": "Indirizzo email destinatario", "en": "Recipient email", "de": "Empfänger-E-Mail", "fr": "Email destinataire", "es": "Email destinatario"},
    "save_email_config": {"it": "💾 Salva configurazione email", "en": "💾 Save email config", "de": "💾 E-Mail-Konfiguration speichern", "fr": "💾 Enregistrer config", "es": "💾 Guardar configuración"},
    "config_saved": {"it": "Configurazione salvata.", "en": "Configuration saved.", "de": "Konfiguration gespeichert.", "fr": "Configuration enregistrée.", "es": "Configuración guardada."},
    "send_reminders_now": {"it": "Invia promemoria scadenze ora", "en": "Send reminders now", "de": "Erinnerungen jetzt senden", "fr": "Envoyer les rappels", "es": "Enviar recordatorios ahora"},
    "configure_email_first": {"it": "Configura prima l'email qui sopra.", "en": "Configure email above first.", "de": "Bitte zuerst E-Mail oben konfigurieren.", "fr": "Configurez d'abord l'email ci-dessus.", "es": "Configura primero el email arriba."},
    "no_upcoming_to_notify": {"it": "Nessuna scadenza imminente da segnalare.", "en": "No upcoming deadlines to notify.", "de": "Keine anstehenden Fristen.", "fr": "Aucune échéance à signaler.", "es": "Sin vencimientos para notificar."},
    "found_n_deadlines": {
        "it": "Trovate **{n}** scadenze entro {days} giorni.",
        "en": "Found **{n}** deadlines within {days} days.",
        "de": "**{n}** Fristen innerhalb {days} Tagen gefunden.",
        "fr": "**{n}** échéances dans {days} jours.",
        "es": "**{n}** vencimientos en {days} días.",
    },
    "send_now": {"it": "📧 Invia ora", "en": "📧 Send now", "de": "📧 Jetzt senden", "fr": "📧 Envoyer", "es": "📧 Enviar ahora"},
    "email_sent_to": {"it": "Email inviata a {to}.", "en": "Email sent to {to}.", "de": "E-Mail an {to} gesendet.", "fr": "Email envoyé à {to}.", "es": "Email enviado a {to}."},
    "send_error": {"it": "Errore invio: {err}", "en": "Send error: {err}", "de": "Sendefehler: {err}", "fr": "Erreur envoi: {err}", "es": "Error de envío: {err}"},
    "email_subject": {
        "it": "CAMPERappPLUS — {n} scadenze imminenti",
        "en": "CAMPERappPLUS — {n} upcoming deadlines",
        "de": "CAMPERappPLUS — {n} anstehende Fristen",
        "fr": "CAMPERappPLUS — {n} échéances",
        "es": "CAMPERappPLUS — {n} vencimientos próximos",
    },
    "email_intro": {
        "it": "Ciao!\nQueste sono le scadenze imminenti:\n\n",
        "en": "Hi!\nHere are the upcoming deadlines:\n\n",
        "de": "Hallo!\nHier die anstehenden Fristen:\n\n",
        "fr": "Bonjour!\nVoici les échéances à venir:\n\n",
        "es": "¡Hola!\nEstos son los vencimientos próximos:\n\n",
    },

    # ---------- Chat ----------
    "chat_title": {
        "it": "Chat con amici e famiglia", "en": "Chat with friends and family",
        "de": "Chat mit Freunden und Familie", "fr": "Chat avec amis et famille",
        "es": "Chat con amigos y familia",
    },
    "nickname": {
        "it": "Nickname", "en": "Nickname", "de": "Spitzname",
        "fr": "Pseudo", "es": "Apodo",
    },
    "set_nickname_first": {
        "it": "Imposta prima un nickname per usare la chat.",
        "en": "Set a nickname first to use the chat.",
        "de": "Bitte zuerst einen Spitznamen festlegen.",
        "fr": "Définissez d'abord un pseudo pour utiliser le chat.",
        "es": "Define primero un apodo para usar el chat.",
    },
    "save_nickname": {
        "it": "Salva nickname", "en": "Save nickname", "de": "Spitznamen speichern",
        "fr": "Enregistrer le pseudo", "es": "Guardar apodo",
    },
    "nickname_saved": {
        "it": "Nickname salvato.", "en": "Nickname saved.",
        "de": "Spitzname gespeichert.", "fr": "Pseudo enregistré.",
        "es": "Apodo guardado.",
    },
    "create_room": {
        "it": "➕ Crea nuova stanza", "en": "➕ Create new room",
        "de": "➕ Neuen Raum erstellen", "fr": "➕ Créer un salon",
        "es": "➕ Crear sala nueva",
    },
    "room_name": {
        "it": "Nome stanza", "en": "Room name", "de": "Raumname",
        "fr": "Nom du salon", "es": "Nombre de la sala",
    },
    "create_btn": {
        "it": "Crea", "en": "Create", "de": "Erstellen",
        "fr": "Créer", "es": "Crear",
    },
    "join_room": {
        "it": "🔑 Entra con codice invito", "en": "🔑 Join with invite code",
        "de": "🔑 Mit Einladungscode beitreten",
        "fr": "🔑 Rejoindre avec code d'invitation",
        "es": "🔑 Unirse con código de invitación",
    },
    "invite_code": {
        "it": "Codice invito", "en": "Invite code", "de": "Einladungscode",
        "fr": "Code d'invitation", "es": "Código de invitación",
    },
    "join_btn": {
        "it": "Entra", "en": "Join", "de": "Beitreten",
        "fr": "Rejoindre", "es": "Unirse",
    },
    "code_not_found": {
        "it": "Codice non valido o stanza non trovata.",
        "en": "Invalid code or room not found.",
        "de": "Ungültiger Code oder Raum nicht gefunden.",
        "fr": "Code invalide ou salon introuvable.",
        "es": "Código no válido o sala no encontrada.",
    },
    "your_rooms": {
        "it": "Le tue stanze", "en": "Your rooms", "de": "Deine Räume",
        "fr": "Vos salons", "es": "Tus salas",
    },
    "no_rooms_yet": {
        "it": "Nessuna stanza. Creane una o entra con un codice invito.",
        "en": "No rooms yet. Create one or join with an invite code.",
        "de": "Noch keine Räume. Erstelle einen oder tritt mit Code bei.",
        "fr": "Aucun salon. Créez-en un ou rejoignez avec un code.",
        "es": "Sin salas. Crea una o únete con un código.",
    },
    "open_room": {
        "it": "Apri", "en": "Open", "de": "Öffnen",
        "fr": "Ouvrir", "es": "Abrir",
    },
    "leave_room": {
        "it": "Esci", "en": "Leave", "de": "Verlassen",
        "fr": "Quitter", "es": "Salir",
    },
    "type_message": {
        "it": "Scrivi un messaggio…", "en": "Type a message…",
        "de": "Nachricht schreiben…", "fr": "Écrire un message…",
        "es": "Escribe un mensaje…",
    },
    "back_to_rooms": {
        "it": "← Indietro", "en": "← Back", "de": "← Zurück",
        "fr": "← Retour", "es": "← Atrás",
    },
    "share_code": {
        "it": "Condividi questo codice con chi vuoi invitare:",
        "en": "Share this code with the people you want to invite:",
        "de": "Teile diesen Code mit den Personen, die du einladen willst:",
        "fr": "Partagez ce code avec ceux que vous voulez inviter:",
        "es": "Comparte este código con quien quieras invitar:",
    },
    "no_messages": {
        "it": "Nessun messaggio ancora. Inizia tu! 👋",
        "en": "No messages yet. Start the conversation! 👋",
        "de": "Noch keine Nachrichten. Fang an! 👋",
        "fr": "Pas encore de messages. Lancez la conversation! 👋",
        "es": "Aún no hay mensajes. ¡Empieza tú! 👋",
    },
    "trip_chat": {
        "it": "💬 Chat viaggio", "en": "💬 Trip chat",
        "de": "💬 Reise-Chat", "fr": "💬 Chat voyage",
        "es": "💬 Chat del viaje",
    },
    "create_trip_chat": {
        "it": "💬 Crea chat per questo viaggio", "en": "💬 Create chat for this trip",
        "de": "💬 Chat für diese Reise erstellen",
        "fr": "💬 Créer un chat pour ce voyage",
        "es": "💬 Crear chat para este viaje",
    },
    "trip_chat_created": {
        "it": "Chat viaggio creata. Codice invito: {code}",
        "en": "Trip chat created. Invite code: {code}",
        "de": "Reise-Chat erstellt. Einladungscode: {code}",
        "fr": "Chat voyage créé. Code d'invitation: {code}",
        "es": "Chat del viaje creado. Código de invitación: {code}",
    },
    "open_chat": {
        "it": "Apri chat", "en": "Open chat", "de": "Chat öffnen",
        "fr": "Ouvrir le chat", "es": "Abrir chat",
    },

    # ---------- Chat (extended) ----------
    "members": {
        "it": "Membri", "en": "Members", "de": "Mitglieder",
        "fr": "Membres", "es": "Miembros",
    },
    "you": {
        "it": "tu", "en": "you", "de": "du", "fr": "vous", "es": "tú",
    },
    "online": {
        "it": "online", "en": "online", "de": "online",
        "fr": "en ligne", "es": "en línea",
    },
    "offline": {
        "it": "offline", "en": "offline", "de": "offline",
        "fr": "hors ligne", "es": "sin conexión",
    },
    "last_seen_at": {
        "it": "visto {when}", "en": "seen {when}",
        "de": "gesehen {when}", "fr": "vu {when}", "es": "visto {when}",
    },
    "edit": {
        "it": "Modifica", "en": "Edit", "de": "Bearbeiten",
        "fr": "Modifier", "es": "Editar",
    },
    "delete": {
        "it": "Elimina", "en": "Delete", "de": "Löschen",
        "fr": "Supprimer", "es": "Eliminar",
    },
    "reply": {
        "it": "Rispondi", "en": "Reply", "de": "Antworten",
        "fr": "Répondre", "es": "Responder",
    },
    "react": {
        "it": "Reagisci", "en": "React", "de": "Reagieren",
        "fr": "Réagir", "es": "Reaccionar",
    },
    "edit_message": {
        "it": "Modifica messaggio", "en": "Edit message",
        "de": "Nachricht bearbeiten", "fr": "Modifier le message",
        "es": "Editar mensaje",
    },
    "save": {
        "it": "Salva", "en": "Save", "de": "Speichern",
        "fr": "Enregistrer", "es": "Guardar",
    },
    "cancel": {
        "it": "Annulla", "en": "Cancel", "de": "Abbrechen",
        "fr": "Annuler", "es": "Cancelar",
    },
    "edited_label": {
        "it": "modificato", "en": "edited", "de": "bearbeitet",
        "fr": "modifié", "es": "editado",
    },
    "replying_to": {
        "it": "Stai rispondendo a", "en": "Replying to",
        "de": "Antwort an", "fr": "Réponse à", "es": "Respondiendo a",
    },
    "cancel_reply": {
        "it": "✕", "en": "✕", "de": "✕", "fr": "✕", "es": "✕",
    },
    "load_older": {
        "it": "⬆️ Carica messaggi precedenti",
        "en": "⬆️ Load older messages",
        "de": "⬆️ Ältere Nachrichten laden",
        "fr": "⬆️ Charger les messages précédents",
        "es": "⬆️ Cargar mensajes anteriores",
    },
    "no_older": {
        "it": "Nessun messaggio precedente.",
        "en": "No older messages.",
        "de": "Keine älteren Nachrichten.",
        "fr": "Aucun message plus ancien.",
        "es": "No hay mensajes anteriores.",
    },
    "you_were_mentioned": {
        "it": "Sei stato menzionato in {n} messaggi non letti.",
        "en": "You were mentioned in {n} unread message(s).",
        "de": "Du wurdest in {n} ungelesenen Nachrichten erwähnt.",
        "fr": "Vous avez été mentionné dans {n} message(s) non lu(s).",
        "es": "Te mencionaron en {n} mensaje(s) sin leer.",
    },
    "user_joined": {
        "it": "👋 {nick} è entrato nella stanza",
        "en": "👋 {nick} joined the room",
        "de": "👋 {nick} ist dem Raum beigetreten",
        "fr": "👋 {nick} a rejoint le salon",
        "es": "👋 {nick} se unió a la sala",
    },
    "today": {
        "it": "Oggi", "en": "Today", "de": "Heute",
        "fr": "Aujourd'hui", "es": "Hoy",
    },
    "yesterday": {
        "it": "Ieri", "en": "Yesterday", "de": "Gestern",
        "fr": "Hier", "es": "Ayer",
    },
    "deleted_message": {
        "it": "_messaggio eliminato_",
        "en": "_message deleted_",
        "de": "_Nachricht gelöscht_",
        "fr": "_message supprimé_",
        "es": "_mensaje eliminado_",
    },
    "confirm_delete_msg": {
        "it": "Eliminare il messaggio?",
        "en": "Delete this message?",
        "de": "Nachricht löschen?",
        "fr": "Supprimer ce message ?",
        "es": "¿Eliminar el mensaje?",
    },
    "yes": {
        "it": "Sì", "en": "Yes", "de": "Ja", "fr": "Oui", "es": "Sí",
    },
    "no": {
        "it": "No", "en": "No", "de": "Nein", "fr": "Non", "es": "No",
    },
    "no_members": {
        "it": "Nessun membro ancora.",
        "en": "No members yet.",
        "de": "Noch keine Mitglieder.",
        "fr": "Aucun membre pour l'instant.",
        "es": "Aún no hay miembros.",
    },
    "avatar": {
        "it": "Immagine profilo", "en": "Profile picture",
        "de": "Profilbild", "fr": "Photo de profil",
        "es": "Foto de perfil",
    },
    "change_avatar": {
        "it": "Cambia immagine profilo",
        "en": "Change profile picture",
        "de": "Profilbild ändern",
        "fr": "Changer la photo de profil",
        "es": "Cambiar foto de perfil",
    },
    "upload_image": {
        "it": "Carica un'immagine (PNG/JPG)",
        "en": "Upload an image (PNG/JPG)",
        "de": "Bild hochladen (PNG/JPG)",
        "fr": "Téléverser une image (PNG/JPG)",
        "es": "Sube una imagen (PNG/JPG)",
    },
    "avatar_saved": {
        "it": "Immagine profilo aggiornata.",
        "en": "Profile picture updated.",
        "de": "Profilbild aktualisiert.",
        "fr": "Photo de profil mise à jour.",
        "es": "Foto de perfil actualizada.",
    },
    "remove_avatar": {
        "it": "Rimuovi immagine",
        "en": "Remove picture",
        "de": "Bild entfernen",
        "fr": "Supprimer la photo",
        "es": "Quitar foto",
    },
    "avatar_removed": {
        "it": "Immagine rimossa.",
        "en": "Picture removed.",
        "de": "Bild entfernt.",
        "fr": "Photo supprimée.",
        "es": "Foto quitada.",
    },
    "invalid_image": {
        "it": "Immagine non valida.",
        "en": "Invalid image.",
        "de": "Ungültiges Bild.",
        "fr": "Image invalide.",
        "es": "Imagen no válida.",
    },
    "set_nick_to_set_avatar": {
        "it": "Imposta un nickname prima di caricare un'immagine.",
        "en": "Set a nickname before uploading a picture.",
        "de": "Lege einen Nickname fest, bevor du ein Bild hochlädst.",
        "fr": "Définissez un pseudo avant de téléverser une photo.",
        "es": "Define un apodo antes de subir una foto.",
    },
    "or_pick_emoji": {
        "it": "Oppure scegli una faccina:",
        "en": "Or pick an emoji:",
        "de": "Oder wähle ein Emoji:",
        "fr": "Ou choisis une émoji :",
        "es": "O elige un emoji:",
    },
    "remove_emoji": {
        "it": "Rimuovi faccina",
        "en": "Remove emoji",
        "de": "Emoji entfernen",
        "fr": "Supprimer l'émoji",
        "es": "Quitar emoji",
    },
    "emoji_saved": {
        "it": "Faccina aggiornata.",
        "en": "Emoji updated.",
        "de": "Emoji aktualisiert.",
        "fr": "Émoji mis à jour.",
        "es": "Emoji actualizado.",
    },

    # ---------- Map ----------
    "map_title": {
        "it": "Posizione — apri in Google Maps", "en": "Location — open in Google Maps",
        "de": "Standort — in Google Maps öffnen", "fr": "Position — ouvrir dans Google Maps",
        "es": "Ubicación — abrir en Google Maps",
    },
    "map_caption": {
        "it": "Premi 📍 per leggere la tua posizione, poi apri Google Maps "
              "(GPS più preciso, soprattutto da smartphone).",
        "en": "Press 📍 to read your position, then open Google Maps "
              "(more precise GPS, especially on mobile).",
        "de": "Drücke 📍, um deinen Standort zu lesen, dann Google Maps öffnen "
              "(genaueres GPS, vor allem auf dem Smartphone).",
        "fr": "Appuyez sur 📍 pour lire votre position, puis ouvrez Google Maps "
              "(GPS plus précis, surtout sur smartphone).",
        "es": "Pulsa 📍 para leer tu ubicación, luego abre Google Maps "
              "(GPS más preciso, sobre todo en móvil).",
    },
    "click_locate": {
        "it": "Clicca il pulsante 📍 qui sopra per leggere la tua posizione.",
        "en": "Click the 📍 button above to read your position.",
        "de": "Klicke oben auf 📍, um deinen Standort zu lesen.",
        "fr": "Cliquez sur 📍 ci-dessus pour lire votre position.",
        "es": "Pulsa el botón 📍 arriba para leer tu ubicación.",
    },
    "open_gmaps_direct": {
        "it": "🗺️ Apri Google Maps", "en": "🗺️ Open Google Maps",
        "de": "🗺️ Google Maps öffnen", "fr": "🗺️ Ouvrir Google Maps",
        "es": "🗺️ Abrir Google Maps",
    },
    "gmaps_more_precise": {
        "it": "Google Maps userà il proprio GPS, in genere più preciso del browser.",
        "en": "Google Maps will use its own GPS, usually more precise than the browser.",
        "de": "Google Maps nutzt eigenes GPS, meist genauer als der Browser.",
        "fr": "Google Maps utilisera son propre GPS, en général plus précis.",
        "es": "Google Maps usará su propio GPS, normalmente más preciso.",
    },
    "latitude": {"it": "Latitudine", "en": "Latitude", "de": "Breitengrad", "fr": "Latitude", "es": "Latitud"},
    "longitude": {"it": "Longitudine", "en": "Longitude", "de": "Längengrad", "fr": "Longitude", "es": "Longitud"},
    "accuracy_m": {
        "it": "Precisione (m)", "en": "Accuracy (m)", "de": "Genauigkeit (m)",
        "fr": "Précision (m)", "es": "Precisión (m)",
    },
    "altitude_m": {
        "it": "Altitudine (m)", "en": "Altitude (m)", "de": "Höhe (m)",
        "fr": "Altitude (m)", "es": "Altitud (m)",
    },
    "speed_kmh": {
        "it": "Velocità (km/h)", "en": "Speed (km/h)", "de": "Geschwindigkeit (km/h)",
        "fr": "Vitesse (km/h)", "es": "Velocidad (km/h)",
    },
    "open_in_gmaps": {
        "it": "🗺️ Apri in Google Maps", "en": "🗺️ Open in Google Maps",
        "de": "🗺️ In Google Maps öffnen", "fr": "🗺️ Ouvrir dans Google Maps",
        "es": "🗺️ Abrir en Google Maps",
    },

    # ---------- PDF ----------
    "pdf_title": {"it": "Libretto digitale camper", "en": "Camper digital logbook", "de": "Digitales Wartungsheft", "fr": "Carnet d'entretien camping-car", "es": "Libro digital autocaravana"},
    "pdf_generated_on": {"it": "Generato il {date}", "en": "Generated on {date}", "de": "Erstellt am {date}", "fr": "Généré le {date}", "es": "Generado el {date}"},
    "pdf_no_deadlines": {"it": "Nessuna scadenza registrata.", "en": "No deadlines.", "de": "Keine Fristen.", "fr": "Aucune échéance.", "es": "Sin vencimientos."},
    "pdf_no_interventions": {"it": "Nessun intervento registrato.", "en": "No interventions.", "de": "Keine Wartungen.", "fr": "Aucune intervention.", "es": "Sin intervenciones."},
    "pdf_no_trips": {"it": "Nessun viaggio registrato.", "en": "No trips.", "de": "Keine Reisen.", "fr": "Aucun voyage.", "es": "Sin viajes."},
    "pdf_no_fuel": {"it": "Nessun rifornimento registrato.", "en": "No refills.", "de": "Keine Tankstopps.", "fr": "Aucun plein.", "es": "Sin repostajes."},
    "pdf_section_deadlines": {"it": "Scadenze", "en": "Deadlines", "de": "Fristen", "fr": "Échéances", "es": "Vencimientos"},
    "pdf_section_maintenance": {"it": "Interventi e manutenzione", "en": "Interventions and maintenance", "de": "Wartung", "fr": "Interventions et entretien", "es": "Intervenciones y mantenimiento"},
    "pdf_section_trips": {"it": "Viaggi", "en": "Trips", "de": "Reisen", "fr": "Voyages", "es": "Viajes"},
    "pdf_section_fuel": {"it": "Rifornimenti", "en": "Refills", "de": "Tankstopps", "fr": "Pleins", "es": "Repostajes"},

    # ---------- Costi e km ----------
    "km_owned": {
        "it": "Km posseduti", "en": "Owned km", "de": "Gefahrene km",
        "fr": "Km parcourus", "es": "Km recorridos",
    },
    "eur_per_km": {
        "it": "{sym}/km", "en": "{sym}/km", "de": "{sym}/km", "fr": "{sym}/km", "es": "{sym}/km",
    },
    "eur_per_km_help": {
        "it": "{sym}/km = costi totali / km percorsi da quando possiedi il camper. Imposta i 'km iniziali' del camper per renderlo accurato.",
        "en": "{sym}/km = total costs / km driven since you own the camper. Set the camper's 'initial km' to make it accurate.",
        "de": "{sym}/km = Gesamtkosten / km seit Besitz. Setze die 'Anfangs-km' für genaue Werte.",
        "fr": "{sym}/km = coûts totaux / km parcourus depuis l'acquisition. Définissez les 'km initiaux' pour plus de précision.",
        "es": "{sym}/km = costes totales / km recorridos desde la compra. Define los 'km iniciales' para mayor precisión.",
    },

    # ---------- Km iniziali ----------
    "km_iniziale_help": {
        "it": "Imposta i km del camper al momento dell'acquisto: servono per calcolare {sym}/km reali.",
        "en": "Set the camper's km when you bought it: needed for accurate {sym}/km.",
        "de": "Anfangs-km zum Zeitpunkt des Kaufs eingeben: nötig für genaue {sym}/km.",
        "fr": "Indiquez les km au moment de l'achat : nécessaires pour le {sym}/km réel.",
        "es": "Define los km al momento de la compra: necesarios para el {sym}/km real.",
    },
    "edit_km_iniziale": {
        "it": "✏️ Modifica km iniziali",
        "en": "✏️ Edit initial km",
        "de": "✏️ Anfangs-km bearbeiten",
        "fr": "✏️ Modifier les km initiaux",
        "es": "✏️ Editar km iniciales",
    },
    "km_iniziale_label": {
        "it": "Km iniziali (data acquisto)",
        "en": "Initial km (purchase date)",
        "de": "Anfangs-km (Kaufdatum)",
        "fr": "Km initiaux (date d'achat)",
        "es": "Km iniciales (fecha de compra)",
    },

    # ---------- Pieno carburante ----------
    "full_tank": {
        "it": "Pieno", "en": "Full tank", "de": "Volltanken",
        "fr": "Plein", "es": "Lleno",
    },
    "full_tank_short": {
        "it": "Pieno?", "en": "Full?", "de": "Voll?", "fr": "Plein?", "es": "¿Lleno?",
    },
    "full_tank_help": {
        "it": "Spunta solo se hai fatto il pieno. Il consumo l/100km viene calcolato solo tra rifornimenti completi.",
        "en": "Check only if you filled up the tank. l/100km is computed only between full fillups.",
        "de": "Nur ankreuzen, wenn vollgetankt. Verbrauch wird nur zwischen Volltankungen berechnet.",
        "fr": "Cochez uniquement si plein effectué. La consommation est calculée entre pleins complets.",
        "es": "Marca solo si hiciste el lleno. El consumo se calcula solo entre llenos completos.",
    },

    # ---------- Categorie intervento ----------
    "int_revisione": {"it": "Revisione", "en": "Inspection", "de": "Hauptuntersuchung", "fr": "Contrôle technique", "es": "ITV"},
    "int_tagliando": {"it": "Tagliando", "en": "Service", "de": "Inspektion", "fr": "Révision", "es": "Mantenimiento"},
    "int_gomme": {"it": "Gomme", "en": "Tires", "de": "Reifen", "fr": "Pneus", "es": "Neumáticos"},
    "int_freni": {"it": "Freni", "en": "Brakes", "de": "Bremsen", "fr": "Freins", "es": "Frenos"},
    "int_elettrico": {"it": "Elettrico", "en": "Electrical", "de": "Elektrik", "fr": "Électrique", "es": "Eléctrico"},
    "int_idraulico": {"it": "Idraulico/Acqua", "en": "Plumbing/Water", "de": "Wasseranlage", "fr": "Plomberie/Eau", "es": "Fontanería/Agua"},
    "int_carrozzeria": {"it": "Carrozzeria", "en": "Body", "de": "Karosserie", "fr": "Carrosserie", "es": "Carrocería"},
    "int_motore": {"it": "Motore", "en": "Engine", "de": "Motor", "fr": "Moteur", "es": "Motor"},
    "int_altro": {"it": "Altro", "en": "Other", "de": "Sonstiges", "fr": "Autre", "es": "Otro"},

    # ---------- Backup / Ripristino ----------
    "backup_section": {
        "it": "💾 Backup e ripristino", "en": "💾 Backup & restore",
        "de": "💾 Sicherung & Wiederherstellung", "fr": "💾 Sauvegarde & restauration",
        "es": "💾 Copia y restauración",
    },
    "backup_help": {
        "it": "Esporta tutti i tuoi dati e documenti in un file ZIP, oppure ripristina un backup precedente. Utile quando cambi PC.",
        "en": "Export all your data and documents to a ZIP, or restore a previous backup. Useful when switching computers.",
        "de": "Alle Daten und Dokumente als ZIP exportieren oder ein Backup wiederherstellen. Nützlich bei PC-Wechsel.",
        "fr": "Exportez données et documents en ZIP, ou restaurez une sauvegarde. Utile pour changer d'ordinateur.",
        "es": "Exporta todos tus datos y documentos a ZIP, o restaura una copia. Útil al cambiar de PC.",
    },
    "backup_export": {
        "it": "Esporta", "en": "Export", "de": "Export", "fr": "Exporter", "es": "Exportar",
    },
    "backup_prepare": {
        "it": "📦 Prepara backup", "en": "📦 Prepare backup", "de": "📦 Backup vorbereiten",
        "fr": "📦 Préparer la sauvegarde", "es": "📦 Preparar copia",
    },
    "backup_download": {
        "it": "⬇️ Scarica ZIP", "en": "⬇️ Download ZIP", "de": "⬇️ ZIP herunterladen",
        "fr": "⬇️ Télécharger le ZIP", "es": "⬇️ Descargar ZIP",
    },
    "backup_import": {
        "it": "Importa", "en": "Import", "de": "Import", "fr": "Importer", "es": "Importar",
    },
    "backup_import_help": {
        "it": "⚠️ L'import sostituisce TUTTI i dati attuali. Operazione irreversibile.",
        "en": "⚠️ Import REPLACES all current data. Cannot be undone.",
        "de": "⚠️ Der Import ERSETZT alle aktuellen Daten. Nicht rückgängig zu machen.",
        "fr": "⚠️ L'import REMPLACE toutes les données actuelles. Irréversible.",
        "es": "⚠️ La importación REEMPLAZA todos los datos. Acción irreversible.",
    },
    "backup_zip_file": {
        "it": "File ZIP di backup", "en": "Backup ZIP file", "de": "Backup-ZIP-Datei",
        "fr": "Fichier ZIP de sauvegarde", "es": "Archivo ZIP de copia",
    },
    "backup_import_confirm": {
        "it": "Confermo: sostituisci tutti i dati con il backup",
        "en": "I confirm: replace all data with this backup",
        "de": "Ich bestätige: alle Daten durch das Backup ersetzen",
        "fr": "Je confirme : remplacer toutes les données par cette sauvegarde",
        "es": "Confirmo: reemplazar todos los datos con esta copia",
    },
    "backup_restore_now": {
        "it": "🔁 Ripristina ora", "en": "🔁 Restore now", "de": "🔁 Jetzt wiederherstellen",
        "fr": "🔁 Restaurer maintenant", "es": "🔁 Restaurar ahora",
    },
    "backup_imported": {
        "it": "Backup ripristinato.", "en": "Backup restored.",
        "de": "Backup wiederhergestellt.", "fr": "Sauvegarde restaurée.",
        "es": "Copia restaurada.",
    },
    "backup_invalid": {
        "it": "Backup non valido: {err}", "en": "Invalid backup: {err}",
        "de": "Ungültiges Backup: {err}", "fr": "Sauvegarde invalide : {err}",
        "es": "Copia no válida: {err}",
    },

    # ---------- Promemoria automatici ----------
    "auto_email_toggle": {
        "it": "Invia promemoria automaticamente all'avvio",
        "en": "Send reminders automatically on startup",
        "de": "Erinnerungen beim Start automatisch senden",
        "fr": "Envoyer les rappels automatiquement au démarrage",
        "es": "Enviar recordatorios automáticamente al iniciar",
    },
    "auto_email_help": {
        "it": "Quando attivo, all'avvio dell'app le scadenze imminenti vengono inviate via email. Cooldown 24h per evitare email duplicate.",
        "en": "When enabled, upcoming deadlines are emailed at app startup. 24h cooldown to avoid duplicates.",
        "de": "Wenn aktiv, werden anstehende Fristen beim Start per E-Mail gesendet. 24h Cooldown verhindert Duplikate.",
        "fr": "Si activé, les échéances proches sont envoyées par e-mail au démarrage. Cooldown 24h.",
        "es": "Si está activo, las fechas próximas se envían por correo al iniciar. Cooldown de 24h.",
    },
    "auto_email_sent": {
        "it": "Promemoria inviato ({n} scadenze)",
        "en": "Reminder sent ({n} deadlines)",
        "de": "Erinnerung gesendet ({n} Fristen)",
        "fr": "Rappel envoyé ({n} échéances)",
        "es": "Recordatorio enviado ({n} vencimientos)",
    },
    "auto_email_error": {
        "it": "Invio automatico non riuscito",
        "en": "Auto-send failed",
        "de": "Automatischer Versand fehlgeschlagen",
        "fr": "Envoi automatique échoué",
        "es": "Envío automático fallido",
    },
    "last_sent_on": {
        "it": "Ultimo invio: {when}",
        "en": "Last sent: {when}",
        "de": "Zuletzt gesendet: {when}",
        "fr": "Dernier envoi : {when}",
        "es": "Último envío: {when}",
    },
    "never_sent": {
        "it": "Mai inviato.", "en": "Never sent.", "de": "Nie gesendet.",
        "fr": "Jamais envoyé.", "es": "Nunca enviado.",
    },

    # ---------- Aree sosta / POI mappa ----------
    "poi_section": {
        "it": "📍 Aree sosta e camper service nelle vicinanze",
        "en": "📍 Camper sites & service points nearby",
        "de": "📍 Stell- und Versorgungsplätze in der Nähe",
        "fr": "📍 Aires camping-car & vidange à proximité",
        "es": "📍 Áreas y servicios de autocaravana cercanos",
    },
    "poi_caption": {
        "it": "Dati da OpenStreetMap. La prima ricerca puo' richiedere qualche secondo; risultati in cache per 24h.",
        "en": "Data from OpenStreetMap. First search may take a few seconds; results cached 24h.",
        "de": "Daten von OpenStreetMap. Erste Suche kann etwas dauern; Ergebnisse 24h zwischengespeichert.",
        "fr": "Données OpenStreetMap. La 1re recherche peut prendre un instant ; mise en cache 24h.",
        "es": "Datos de OpenStreetMap. La primera búsqueda puede tardar; resultados en caché 24h.",
    },
    "poi_caravan_site": {
        "it": "🅿️ Area sosta camper", "en": "🅿️ Caravan site",
        "de": "🅿️ Wohnmobil-Stellplatz", "fr": "🅿️ Aire camping-car",
        "es": "🅿️ Área de autocaravanas",
    },
    "poi_sanitary_dump": {
        "it": "🚽 Camper service (scarico)", "en": "🚽 Sanitary dump station",
        "de": "🚽 Entsorgungsstation", "fr": "🚽 Station de vidange",
        "es": "🚽 Vaciado de aguas",
    },
    "poi_camp_site": {
        "it": "⛺ Campeggio", "en": "⛺ Camp site", "de": "⛺ Campingplatz",
        "fr": "⛺ Camping", "es": "⛺ Camping",
    },
    "poi_greenzone": {
        "it": "🌳 Aree verdi (picnic)",
        "en": "🌳 Green zones (picnic)",
        "de": "🌳 Grünflächen (Picknick)",
        "fr": "🌳 Zones vertes (pique-nique)",
        "es": "🌳 Zonas verdes (picnic)",
    },
    "poi_types": {
        "it": "Cosa cercare", "en": "What to search", "de": "Wonach suchen",
        "fr": "Que chercher", "es": "Qué buscar",
    },
    "poi_radius": {
        "it": "Raggio (km)", "en": "Radius (km)", "de": "Umkreis (km)",
        "fr": "Rayon (km)", "es": "Radio (km)",
    },
    "poi_search": {
        "it": "🔎 Cerca", "en": "🔎 Search", "de": "🔎 Suchen",
        "fr": "🔎 Chercher", "es": "🔎 Buscar",
    },
    "poi_searching": {
        "it": "Sto cercando...", "en": "Searching...", "de": "Suche...",
        "fr": "Recherche...", "es": "Buscando...",
    },
    "poi_error": {
        "it": "Errore nella ricerca: {err}", "en": "Search error: {err}",
        "de": "Suchfehler: {err}", "fr": "Erreur de recherche : {err}",
        "es": "Error de búsqueda: {err}",
    },
    "poi_none_found": {
        "it": "Nessuna area trovata in questa zona. Prova ad ampliare il raggio.",
        "en": "No areas found nearby. Try a larger radius.",
        "de": "Keine Bereiche gefunden. Probiere einen grosseren Umkreis.",
        "fr": "Aucune aire trouvee. Essayez un rayon plus grand.",
        "es": "Sin resultados cercanos. Prueba un radio mayor.",
    },
    "poi_found": {
        "it": "Trovate {n} aree.", "en": "Found {n} areas.",
        "de": "{n} Plätze gefunden.", "fr": "{n} aires trouvées.",
        "es": "{n} áreas encontradas.",
    },
    "poi_no_name": {
        "it": "(senza nome)", "en": "(unnamed)", "de": "(ohne Namen)",
        "fr": "(sans nom)", "es": "(sin nombre)",
    },
    "poi_fee": {
        "it": "A pagamento", "en": "Fee", "de": "Gebührenpflichtig",
        "fr": "Payant", "es": "De pago",
    },
    "poi_website": {
        "it": "Sito web", "en": "Website", "de": "Webseite",
        "fr": "Site web", "es": "Sitio web",
    },
    "poi_book_booking": {
        "it": "🏨 Prenota su Booking",
        "en": "🏨 Book on Booking",
        "de": "🏨 Auf Booking buchen",
        "fr": "🏨 Réserver sur Booking",
        "es": "🏨 Reservar en Booking",
    },
    "affiliate_disclosure": {
        "it": "ⓘ I link 'Prenota su Booking' sono affiliati: se prenoti riceviamo una piccola commissione, senza costi extra per te.",
        "en": "ⓘ 'Book on Booking' links are affiliate links: we earn a small commission if you book, at no extra cost to you.",
        "de": "ⓘ Die 'Auf Booking buchen'-Links sind Affiliate-Links: Wir erhalten eine kleine Provision bei einer Buchung, ohne Mehrkosten für dich.",
        "fr": "ⓘ Les liens 'Réserver sur Booking' sont affiliés : nous touchons une petite commission si vous réservez, sans frais supplémentaires pour vous.",
        "es": "ⓘ Los enlaces 'Reservar en Booking' son afiliados: recibimos una pequeña comisión si reservas, sin coste adicional para ti.",
    },
    "poi_list": {
        "it": "Elenco", "en": "List", "de": "Liste", "fr": "Liste", "es": "Lista",
    },
    "poi_truncated": {
        "it": "Mostrate {shown} su {total}.",
        "en": "Showing {shown} of {total}.",
        "de": "Zeige {shown} von {total}.",
        "fr": "Affichage de {shown} sur {total}.",
        "es": "Mostrando {shown} de {total}.",
    },
    "you_are_here": {
        "it": "Sei qui", "en": "You are here", "de": "Du bist hier",
        "fr": "Vous êtes ici", "es": "Estás aquí",
    },
    "manual_location_label": {
        "it": "🔍 Cerca per nome citta o luogo",
        "en": "🔍 Search by city or place name",
        "de": "🔍 Nach Stadt oder Ort suchen",
        "fr": "🔍 Rechercher par ville ou lieu",
        "es": "🔍 Buscar por ciudad o lugar",
    },
    "manual_location_placeholder": {
        "it": "es. Verona, Lago di Garda, Roma...",
        "en": "e.g. Verona, Lake Garda, Rome...",
        "de": "z.B. Verona, Gardasee, Rom...",
        "fr": "ex. Vérone, Lac de Garde, Rome...",
        "es": "p.ej. Verona, Lago de Garda, Roma...",
    },
    "manual_location_help": {
        "it": "Utile quando il GPS del browser e' impreciso (PC fisso, VPN). Lasciare vuoto per usare il GPS.",
        "en": "Useful when browser GPS is inaccurate (desktop, VPN). Leave empty to use GPS.",
        "de": "Nützlich, wenn der Browser-GPS ungenau ist (Desktop, VPN). Leer lassen für GPS.",
        "fr": "Utile quand le GPS du navigateur est imprécis. Laisser vide pour utiliser le GPS.",
        "es": "Útil cuando el GPS del navegador es impreciso. Deja vacío para usar GPS.",
    },
    "manual_or_gps": {
        "it": "Oppure clicca l'icona qui sotto per usare il GPS del browser:",
        "en": "Or click the icon below to use browser GPS:",
        "de": "Oder klicke unten auf das Symbol für Browser-GPS:",
        "fr": "Ou cliquez sur l'icône ci-dessous pour le GPS du navigateur :",
        "es": "O haz clic en el icono para usar el GPS del navegador:",
    },
    "manual_searching": {
        "it": "Cerco la posizione...", "en": "Searching location...",
        "de": "Suche Standort...", "fr": "Recherche de la position...",
        "es": "Buscando ubicación...",
    },
    "manual_not_found": {
        "it": "Posizione non trovata. Prova un altro nome.",
        "en": "Location not found. Try another name.",
        "de": "Standort nicht gefunden. Probiere einen anderen Namen.",
        "fr": "Position introuvable. Essayez un autre nom.",
        "es": "Ubicación no encontrada. Prueba otro nombre.",
    },
    "manual_found": {
        "it": "📍 {place}", "en": "📍 {place}", "de": "📍 {place}",
        "fr": "📍 {place}", "es": "📍 {place}",
    },

    # ---------- Notifiche desktop ----------
    "desktop_section": {
        "it": "🔔 Notifiche desktop Windows",
        "en": "🔔 Windows desktop notifications",
        "de": "🔔 Windows-Desktop-Benachrichtigungen",
        "fr": "🔔 Notifications Windows",
        "es": "🔔 Notificaciones de escritorio",
    },
    "desktop_help": {
        "it": "Mostra una notifica nativa di Windows con le scadenze imminenti. Funziona senza configurare l'email.",
        "en": "Shows a native Windows toast with upcoming deadlines. No email setup needed.",
        "de": "Zeigt eine native Windows-Benachrichtigung mit kommenden Fristen. Keine E-Mail-Konfiguration noetig.",
        "fr": "Affiche une notification Windows native avec les échéances à venir. Aucune configuration e-mail requise.",
        "es": "Muestra una notificación nativa de Windows. No requiere configurar correo.",
    },
    "desktop_unsupported": {
        "it": "Le notifiche desktop sono disponibili solo su Windows.",
        "en": "Desktop notifications are only available on Windows.",
        "de": "Desktop-Benachrichtigungen sind nur unter Windows verfügbar.",
        "fr": "Les notifications de bureau ne sont disponibles que sur Windows.",
        "es": "Las notificaciones de escritorio solo están disponibles en Windows.",
    },
    "auto_desktop_toggle": {
        "it": "Mostra notifica desktop all'avvio",
        "en": "Show desktop notification on startup",
        "de": "Desktop-Benachrichtigung beim Start anzeigen",
        "fr": "Afficher la notification au démarrage",
        "es": "Mostrar notificación al iniciar",
    },
    "auto_desktop_help": {
        "it": "Quando attivo, all'avvio dell'app appare un toast Windows se ci sono scadenze entro la soglia. Cooldown 24h.",
        "en": "When enabled, a Windows toast pops up at startup if deadlines are coming. 24h cooldown.",
        "de": "Wenn aktiv, erscheint beim Start ein Windows-Toast bei kommenden Fristen. 24h Cooldown.",
        "fr": "Si activé, un toast Windows apparaît au démarrage en cas d'échéances proches. Cooldown 24h.",
        "es": "Si está activo, aparece una notificación al iniciar. Cooldown 24h.",
    },
    "auto_desktop_sent": {
        "it": "Notifica desktop mostrata ({n} scadenze)",
        "en": "Desktop notification shown ({n} deadlines)",
        "de": "Desktop-Benachrichtigung angezeigt ({n} Fristen)",
        "fr": "Notification affichée ({n} échéances)",
        "es": "Notificación mostrada ({n} vencimientos)",
    },
    "auto_desktop_error": {
        "it": "Notifica desktop non riuscita",
        "en": "Desktop notification failed",
        "de": "Desktop-Benachrichtigung fehlgeschlagen",
        "fr": "Notification échouée",
        "es": "Notificación fallida",
    },
    "desktop_test": {
        "it": "🔔 Prova notifica",
        "en": "🔔 Test notification",
        "de": "🔔 Test-Benachrichtigung",
        "fr": "🔔 Tester la notification",
        "es": "🔔 Probar notificación",
    },
    "desktop_test_sent": {
        "it": "Notifica di prova inviata. Controlla il centro notifiche di Windows.",
        "en": "Test notification sent. Check the Windows action center.",
        "de": "Test-Benachrichtigung gesendet. Pruefe das Info-Center.",
        "fr": "Notification test envoyée. Vérifiez le centre de notifications.",
        "es": "Notificación de prueba enviada. Revisa el centro de notificaciones.",
    },
    "toast_test_title": {
        "it": "CAMPERappPLUS — Test notifica",
        "en": "CAMPERappPLUS — Test notification",
        "de": "CAMPERappPLUS — Test",
        "fr": "CAMPERappPLUS — Test",
        "es": "CAMPERappPLUS — Prueba",
    },
    "toast_test_body": {
        "it": "Le notifiche desktop funzionano correttamente.",
        "en": "Desktop notifications are working.",
        "de": "Desktop-Benachrichtigungen funktionieren.",
        "fr": "Les notifications fonctionnent.",
        "es": "Las notificaciones funcionan.",
    },
    "toast_title": {
        "it": "CAMPERappPLUS — {n} scadenze in arrivo",
        "en": "CAMPERappPLUS — {n} upcoming deadlines",
        "de": "CAMPERappPLUS — {n} anstehende Fristen",
        "fr": "CAMPERappPLUS — {n} échéances à venir",
        "es": "CAMPERappPLUS — {n} vencimientos próximos",
    },
    "toast_more_items": {
        "it": "...e altre {n}",
        "en": "...and {n} more",
        "de": "...und {n} weitere",
        "fr": "...et {n} autres",
        "es": "...y {n} más",
    },

    # ---------- Meteo ----------
    "weather_section": {
        "it": "🌤️ Meteo nella tua zona",
        "en": "🌤️ Weather at your location",
        "de": "🌤️ Wetter an deinem Standort",
        "fr": "🌤️ Météo à votre position",
        "es": "🌤️ Tiempo en tu zona",
    },
    "weather_caption": {
        "it": "Dati Open-Meteo. Cache locale 30 minuti.",
        "en": "Data from Open-Meteo. Cached locally 30 min.",
        "de": "Daten von Open-Meteo. 30 Min lokal zwischengespeichert.",
        "fr": "Données Open-Meteo. Mise en cache 30 min.",
        "es": "Datos de Open-Meteo. Caché local 30 min.",
    },
    "weather_temp": {
        "it": "Temperatura", "en": "Temperature", "de": "Temperatur",
        "fr": "Température", "es": "Temperatura",
    },
    "weather_condition": {
        "it": "Condizione", "en": "Condition", "de": "Bedingung",
        "fr": "Conditions", "es": "Condición",
    },
    "weather_wind": {
        "it": "Vento", "en": "Wind", "de": "Wind", "fr": "Vent", "es": "Viento",
    },
    "weather_humidity": {
        "it": "Umidità", "en": "Humidity", "de": "Luftfeuchtigkeit",
        "fr": "Humidité", "es": "Humedad",
    },
    "weather_forecast_5d": {
        "it": "Previsioni 5 giorni",
        "en": "5-day forecast",
        "de": "5-Tage-Vorhersage",
        "fr": "Prévisions 5 jours",
        "es": "Previsión 5 días",
    },
    "weather_error": {
        "it": "Meteo non disponibile: {err}",
        "en": "Weather unavailable: {err}",
        "de": "Wetter nicht verfügbar: {err}",
        "fr": "Météo indisponible : {err}",
        "es": "Tiempo no disponible: {err}",
    },
    "weather_source": {
        "it": "Fonte: open-meteo.com",
        "en": "Source: open-meteo.com",
        "de": "Quelle: open-meteo.com",
        "fr": "Source : open-meteo.com",
        "es": "Fuente: open-meteo.com",
    },

    # ---------- Codici WMO (condizioni meteo) ----------
    "wmo_clear": {"it": "Sereno", "en": "Clear", "de": "Klar", "fr": "Dégagé", "es": "Despejado"},
    "wmo_mainly_clear": {"it": "Quasi sereno", "en": "Mainly clear", "de": "Überwiegend klar", "fr": "Plutôt dégagé", "es": "Mayormente despejado"},
    "wmo_partly_cloudy": {"it": "Parzialmente nuvoloso", "en": "Partly cloudy", "de": "Teilweise bewölkt", "fr": "Partiellement nuageux", "es": "Parcialmente nublado"},
    "wmo_overcast": {"it": "Nuvoloso", "en": "Overcast", "de": "Bedeckt", "fr": "Couvert", "es": "Nublado"},
    "wmo_fog": {"it": "Nebbia", "en": "Fog", "de": "Nebel", "fr": "Brouillard", "es": "Niebla"},
    "wmo_drizzle": {"it": "Pioviggine", "en": "Drizzle", "de": "Nieselregen", "fr": "Bruine", "es": "Llovizna"},
    "wmo_freezing_drizzle": {"it": "Pioviggine gelata", "en": "Freezing drizzle", "de": "Gefrierender Nieselregen", "fr": "Bruine verglaçante", "es": "Llovizna helada"},
    "wmo_rain": {"it": "Pioggia", "en": "Rain", "de": "Regen", "fr": "Pluie", "es": "Lluvia"},
    "wmo_rain_heavy": {"it": "Pioggia forte", "en": "Heavy rain", "de": "Starker Regen", "fr": "Pluie forte", "es": "Lluvia fuerte"},
    "wmo_freezing_rain": {"it": "Pioggia gelata", "en": "Freezing rain", "de": "Gefrierender Regen", "fr": "Pluie verglaçante", "es": "Lluvia helada"},
    "wmo_snow": {"it": "Neve", "en": "Snow", "de": "Schnee", "fr": "Neige", "es": "Nieve"},
    "wmo_snow_heavy": {"it": "Neve forte", "en": "Heavy snow", "de": "Starker Schnee", "fr": "Neige forte", "es": "Nieve fuerte"},
    "wmo_snow_grains": {"it": "Granuli di neve", "en": "Snow grains", "de": "Schneegriesel", "fr": "Grains de neige", "es": "Cinarra"},
    "wmo_showers": {"it": "Rovesci", "en": "Showers", "de": "Schauer", "fr": "Averses", "es": "Chubascos"},
    "wmo_showers_heavy": {"it": "Rovesci forti", "en": "Heavy showers", "de": "Starke Schauer", "fr": "Averses fortes", "es": "Chubascos fuertes"},
    "wmo_snow_showers": {"it": "Rovesci di neve", "en": "Snow showers", "de": "Schneeschauer", "fr": "Averses de neige", "es": "Chubascos de nieve"},
    "wmo_thunder": {"it": "Temporale", "en": "Thunderstorm", "de": "Gewitter", "fr": "Orage", "es": "Tormenta"},
    "wmo_thunder_hail": {"it": "Temporale con grandine", "en": "Thunderstorm with hail", "de": "Gewitter mit Hagel", "fr": "Orage avec grêle", "es": "Tormenta con granizo"},
    "wmo_unknown": {"it": "Sconosciuto", "en": "Unknown", "de": "Unbekannt", "fr": "Inconnu", "es": "Desconocido"},
}


def t(key: str, lang: str = "it", **kwargs) -> str:
    """Restituisce la stringa tradotta. Fallback su italiano se manca.
    Inietta sym='€' come default per i placeholder valuta cosi' i callsite
    legacy continuano a funzionare anche dopo aver introdotto {sym}."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key  # chiave mancante, ritorna la chiave per debug
    text = entry.get(lang) or entry.get("it") or key
    kwargs.setdefault("sym", "€")
    try:
        return text.format(**kwargs)
    except (KeyError, IndexError):
        return text
