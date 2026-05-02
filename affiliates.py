"""Integrazione Booking.com Affiliate Partner Programme.

Imposta BOOKING_AID con il tuo Affiliate ID (es. "1234567") quando
l'iscrizione su partner.booking.com e' stata approvata.

Stringa vuota = link affiliate disabilitati: l'app continua a funzionare
identica, semplicemente i link 'Prenota su Booking' non vengono mostrati.
"""
from urllib.parse import quote_plus


BOOKING_AID = ""


_BOOKING_LANG = {
    "it": "it", "en": "en-gb", "de": "de", "fr": "fr", "es": "es",
}


def booking_search_url(name: str, lat: float | None = None,
                       lon: float | None = None, lang: str = "it") -> str | None:
    """Deeplink di ricerca Booking pre-compilato sul nome del POI e, se
    forniti, sulle coordinate. Aggiunge label di tracking per distinguere
    il traffico CAMPERappPLUS in dashboard partner."""
    if not BOOKING_AID:
        return None
    booking_lang = _BOOKING_LANG.get(lang, "en-gb")
    params = [
        f"aid={BOOKING_AID}",
        "label=camperapp_poi",
        f"ss={quote_plus(name or '')}",
        f"lang={booking_lang}",
    ]
    if lat is not None and lon is not None:
        params.append(f"latitude={lat}")
        params.append(f"longitude={lon}")
        params.append("dest_type=latlong")
    return "https://www.booking.com/searchresults.html?" + "&".join(params)
