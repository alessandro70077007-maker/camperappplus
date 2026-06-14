"""Banner affiliato Acronis Cyber Protect via CJ Affiliate (Commission Junction).

Il click-link CJ traccia le conversioni e attribuisce la commissione al
publisher. Lo stesso annuncio è presente anche nella landing page GitHub Pages.
"""

# Banner CJ per Acronis Cyber Protect (property ID 101739837, link ID 14426269).
_ACRONIS_CLICK_URL = "https://www.tkqlhce.com/click-101739837-14426269"


def acronis_banner_url(sid: str = "camperapp_mobile") -> str:
    """Click-link CJ del banner Acronis Cyber Protect. Il sub-ID distingue
    in dashboard CJ i click delle varie superfici (mobile, desktop, landing)."""
    return f"{_ACRONIS_CLICK_URL}?sid={sid}"
