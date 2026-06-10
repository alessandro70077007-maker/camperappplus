"""Integrazione Booking.com via CJ Affiliate (Commission Junction).

I deeplink CJ wrappano l'URL Booking dentro il click-server CJ per tracciare
le conversioni e attribuire la commissione al publisher.

Formato:
  https://{click_server}/click-{PID}-{AID}?url=<URL_ENCODED>&sid=<SUBID>

Kill-switch: se CJ_PUBLISHER_ID o CJ_ADVERTISER_ID sono vuoti,
booking_search_url() restituisce None e i link non vengono mostrati - l'app
continua a funzionare identica.
"""
from urllib.parse import quote, quote_plus


# Credenziali CJ Commission Junction per il programma Booking.com.
CJ_PUBLISHER_ID = "7945140"
CJ_ADVERTISER_ID = "4347401"
# Click-server CJ associato a questo programma. Se i deeplink generati dalla
# UI CJ usano un dominio diverso (es. tkqlhce.com, dpbolvw.net, kqzyfj.com),
# basta aggiornare questa costante.
CJ_CLICK_SERVER = "www.anrdoezrs.net"

# Sub-ID per tracciare le conversioni provenienti dai popup POI nella mappa.
# Consente di distinguere in dashboard CJ il traffico camperapp da altri canali.
_CJ_SUB_ID = "camperapp_poi"

# Banner CJ per Acronis Cyber Protect: stesso annuncio presente nella landing
# page GitHub Pages (property ID 101739837, link ID 14426269).
_ACRONIS_CLICK_URL = "https://www.tkqlhce.com/click-101739837-14426269"


_BOOKING_LANG = {
    "it": "it", "en": "en-gb", "de": "de", "fr": "fr", "es": "es",
}


def is_enabled() -> bool:
    return bool(CJ_PUBLISHER_ID and CJ_ADVERTISER_ID and CJ_CLICK_SERVER)


def acronis_banner_url(sid: str = "camperapp_mobile") -> str:
    """Click-link CJ del banner Acronis Cyber Protect. Il sub-ID distingue
    in dashboard CJ i click dell'app mobile da quelli della landing page."""
    return f"{_ACRONIS_CLICK_URL}?sid={sid}"


def booking_search_url(name: str, lat: float | None = None,
                       lon: float | None = None, lang: str = "it") -> str | None:
    """Deeplink CJ -> Booking pre-compilato sul nome del POI e, se forniti,
    sulle coordinate. Ritorna None se le credenziali CJ non sono impostate."""
    if not is_enabled():
        return None
    booking_lang = _BOOKING_LANG.get(lang, "en-gb")
    booking_params = [
        f"ss={quote_plus(name or '')}",
        f"lang={booking_lang}",
    ]
    if lat is not None and lon is not None:
        booking_params.append(f"latitude={lat}")
        booking_params.append(f"longitude={lon}")
        booking_params.append("dest_type=latlong")
    booking_url = (
        "https://www.booking.com/searchresults.html?" + "&".join(booking_params)
    )
    return (
        f"https://{CJ_CLICK_SERVER}/click-{CJ_PUBLISHER_ID}-{CJ_ADVERTISER_ID}"
        f"?url={quote(booking_url, safe='')}&sid={_CJ_SUB_ID}"
    )
