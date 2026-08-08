# -*- coding: utf-8 -*-
"""Genera la landing multilingua in docs/ a partire da site/.

    python scripts/build_site.py

Sorgenti:
    site/template.html   markup e stile, con segnaposto {{...}} e attributi data-i18n
    site/i18n.json       le cinque lingue, stesse chiavi

Prodotti (da non modificare a mano, si rigenerano):
    docs/index.html      italiano, sulla radice
    docs/en|de|fr|es/index.html
    docs/sitemap.xml

Perche' cartelle vere e non ?lang=xx: Google indicizza un URL, non uno stato
JavaScript. Con il vecchio schema le cinque lingue vivevano tutte sullo stesso
URL, il canonical le riportava tutte alla radice e Search Console le scartava
come "pagina alternativa con tag canonical appropriato". Qui ogni lingua ha un
URL suo, e' gia' tradotta nell'HTML servito, si dichiara canonical di se stessa
e rimanda alle altre con hreflang.

Nota: le pagine generate non contengono piu' il JS che sceglieva la lingua da
localStorage o dal browser. E' voluto. Reindirizzare da soli in base alla lingua
del browser nasconde le altre versioni al crawler, che parte sempre da en-US; la
scelta ora e' un link che l'utente clicca, e ogni lingua resta raggiungibile.
"""
from __future__ import print_function

import io
import json
import os
import re
import sys
from datetime import date

# Dominio e sottocartella del sito. Se un giorno passi a un dominio tuo,
# qui cambi due righe e il resto si adegua da solo.
ORIGINE = "https://alessandro70077007-maker.github.io"
RADICE = "/camperappplus/"

# ordine = ordine dei link nella barra in alto
LINGUE = [
    # codice, sottocartella, locale Open Graph, bandiera, nome nella sua lingua
    ("it", "",   "it_IT", u"\U0001F1EE\U0001F1F9", u"Italiano"),
    ("en", "en", "en_GB", u"\U0001F1EC\U0001F1E7", u"English"),
    ("de", "de", "de_DE", u"\U0001F1E9\U0001F1EA", u"Deutsch"),
    ("fr", "fr", "fr_FR", u"\U0001F1EB\U0001F1F7", u"Français"),
    ("es", "es", "es_ES", u"\U0001F1EA\U0001F1F8", u"Español"),
]

QUI = os.path.dirname(os.path.abspath(__file__))
PROGETTO = os.path.dirname(QUI)
SITE = os.path.join(PROGETTO, "site")
DOCS = os.path.join(PROGETTO, "docs")

BANNER = (
    "<!-- Generato da scripts/build_site.py — non modificare a mano.\n"
    "     Le modifiche vanno in site/template.html e site/i18n.json. -->\n"
)


def esc_testo(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s):
    return esc_testo(s).replace('"', "&quot;")


def url_di(sottocartella):
    return ORIGINE + RADICE + (sottocartella + "/" if sottocartella else "")


def blocco_hreflang():
    """Identico su tutte le pagine: ogni lingua deve elencare tutte le altre,
    se stessa compresa, altrimenti Google ignora l'intero gruppo."""
    righe = [
        '<link rel="alternate" hreflang="%s" href="%s">' % (cod, url_di(sub))
        for cod, sub, _, _, _ in LINGUE
    ]
    righe.append('<link rel="alternate" hreflang="x-default" href="%s">' % url_di(""))
    return "\n".join(righe)


def switcher(corrente, sub_corrente):
    """Link relativi, non assoluti: cosi' la barra funziona anche in anteprima
    locale (python -m http.server dentro docs/) e non si rompe se il sito
    cambia dominio o sottocartella."""
    su = "../" if sub_corrente else ""
    righe = ['<nav class="lang-switcher" role="navigation" aria-label="Language">']
    for cod, sub, _, bandiera, nome in LINGUE:
        attivo = cod == corrente
        destinazione = su + (sub + "/" if sub else "")
        righe.append(
            '  <a href="%s" hreflang="%s" title="%s"%s>%s</a>'
            % (
                destinazione or "./",
                cod,
                esc_attr(nome),
                ' class="active" aria-current="page"' if attivo else "",
                bandiera,
            )
        )
    righe.append("</nav>")
    return "\n".join(righe)


def og_locale_alt(corrente):
    return "\n".join(
        '<meta property="og:locale:alternate" content="%s">' % loc
        for cod, _, loc, _, _ in LINGUE
        if cod != corrente
    )


RE_I18N = re.compile(
    r'<(?P<tag>[a-zA-Z][\w-]*)(?P<attr>[^>]*\sdata-i18n="(?P<chiave>[^"]+)"[^>]*)>'
    r"(?P<corpo>.*?)</(?P=tag)>",
    re.S,
)
RE_TOGLI_ATTR = re.compile(r'\sdata-i18n="[^"]+"')


def traduci_corpo(html, dizionario, mancanti):
    def sost(m):
        chiave = m.group("chiave")
        if chiave not in dizionario:
            mancanti.append(chiave)
            return m.group(0)
        attr = RE_TOGLI_ATTR.sub("", m.group("attr"))
        return "<%s%s>%s</%s>" % (m.group("tag"), attr, esc_testo(dizionario[chiave]), m.group("tag"))

    return RE_I18N.sub(sost, html)


def genera_pagina(template, cod, sub, locale, dizionario):
    canonico = url_di(sub)
    fuori = template
    for segnaposto, valore in [
        ("{{LANG}}", cod),
        ("{{PAGE_TITLE}}", esc_attr(dizionario["page_title"])),
        ("{{PAGE_DESC}}", esc_attr(dizionario["page_desc"])),
        ("{{CANONICAL}}", canonico),
        ("{{HREFLANG}}", blocco_hreflang()),
        ("{{OG_LOCALE}}", locale),
        ("{{OG_LOCALE_ALT}}", og_locale_alt(cod)),
        # dalle sottocartelle le immagini stanno una cartella piu' su
        ("{{ASSET}}", "../" if sub else ""),
        ("{{LANG_SWITCHER}}", switcher(cod, sub)),
    ]:
        fuori = fuori.replace(segnaposto, valore)

    mancanti = []
    fuori = traduci_corpo(fuori, dizionario, mancanti)
    if mancanti:
        sys.exit("[%s] chiavi assenti in i18n.json: %s" % (cod, ", ".join(sorted(set(mancanti)))))

    rimasti = re.findall(r"\{\{[A-Z_]+\}\}", fuori)
    if rimasti:
        sys.exit("[%s] segnaposto non sostituiti: %s" % (cod, ", ".join(sorted(set(rimasti)))))
    if "data-i18n" in fuori:
        sys.exit("[%s] sono rimasti attributi data-i18n" % cod)

    return fuori.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + BANNER, 1)


def genera_sitemap(oggi):
    alternate = "\n".join(
        '      <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (cod, url_di(sub))
        for cod, sub, _, _, _ in LINGUE
    )
    alternate += '\n      <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url_di("")

    voci = []
    for cod, sub, _, _, _ in LINGUE:
        voci.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>%s</priority>\n"
            "%s\n"
            "  </url>" % (url_di(sub), oggi, "1.0" if not sub else "0.8", alternate)
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(voci)
        + "\n</urlset>\n"
    )


def scrivi(percorso, contenuto):
    cartella = os.path.dirname(percorso)
    if not os.path.isdir(cartella):
        os.makedirs(cartella)
    with io.open(percorso, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("  %-28s %6d byte" % (os.path.relpath(percorso, PROGETTO), len(contenuto.encode("utf-8"))))


def main():
    with io.open(os.path.join(SITE, "template.html"), encoding="utf-8") as f:
        template = f.read()
    with io.open(os.path.join(SITE, "i18n.json"), encoding="utf-8") as f:
        i18n = json.load(f)

    attese = set(cod for cod, _, _, _, _ in LINGUE)
    if attese - set(i18n):
        sys.exit("i18n.json non ha le lingue: %s" % ", ".join(sorted(attese - set(i18n))))

    # tutte le lingue devono avere le stesse chiavi, se no una pagina esce monca
    base = set(i18n["it"])
    for cod in sorted(attese):
        if set(i18n[cod]) != base:
            manca = base - set(i18n[cod])
            piu = set(i18n[cod]) - base
            sys.exit("[%s] chiavi diverse dall'italiano — mancano: %s | in piu': %s"
                     % (cod, sorted(manca), sorted(piu)))

    print("Genero la landing in docs/")
    for cod, sub, locale, _, _ in LINGUE:
        pagina = genera_pagina(template, cod, sub, locale, i18n[cod])
        scrivi(os.path.join(DOCS, sub, "index.html") if sub else os.path.join(DOCS, "index.html"), pagina)

    scrivi(os.path.join(DOCS, "sitemap.xml"), genera_sitemap(date.today().isoformat()))
    print("Fatto: %d pagine + sitemap." % len(LINGUE))


if __name__ == "__main__":
    main()
