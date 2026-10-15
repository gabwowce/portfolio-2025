#!/usr/bin/env python3
"""
Build the redesigned codeart.lt pages, LT and EN, from one place.

The design handoff lives in _redesign/handoff/. Its mockups are a visual
and content spec, not code: this script turns them into plain semantic
HTML that uses css/site.css and js/site.js only. Both languages share
every template below, so the two versions cannot drift apart.

Writes:
  lt/index.html, en/index.html                     home (for clients)
  lt/portfolio.html, en/portfolio.html             CV + portfolio (employers)
  lt/projektai/*.html, en/projects/*.html          project pages
  lt/cv.html, en/cv.html                           the A4 CV sheet
  lt/about|services|contact.html, en/about|contact.html, portfolio/index.html
                                                   redirects for old URLs
  sitemap.xml

Run:  python3 tools/build-site.py
Then: node tools/build-cv-pdf.mjs    (prints the CV sheets to PDF)

Text in [square brackets] is a placeholder the owner still has to fill
in. It is rendered on purpose so it cannot be forgotten.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://codeart.lt"
EMAIL = "gt1230112301@gmail.com"
GITHUB = "https://github.com/gabwowce"
LINKEDIN = "https://www.linkedin.com/in/gabriel%C4%97-tama%C5%A1evi%C4%8Di%C5%ABt%C4%97-06712526b/"
TIKTOK = "https://www.tiktok.com/@gabiebuilds"
FORMSPREE = "https://formspree.io/f/xeorkyne"
YEAR = "2026"

ROUTES = {
    "home": {"lt": "lt/index.html", "en": "en/index.html"},
    "portfolio": {"lt": "lt/portfolio.html", "en": "en/portfolio.html"},
    "p_lang": {"lt": "lt/projektai/kalbu-platforma.html", "en": "en/projects/language-platform.html"},
    "p_tik": {"lt": "lt/projektai/tikmaker.html", "en": "en/projects/tikmaker.html"},
    "p_loy": {"lt": "lt/projektai/lojalumo-sistema.html", "en": "en/projects/loyalty-system.html"},
    "services": {"lt": "lt/services.html", "en": "en/services.html"},
    "about": {"lt": "lt/about.html", "en": "en/about.html"},
    "contact": {"lt": "lt/contact.html", "en": "en/contact.html"},
    "cv": {"lt": "lt/cv.html", "en": "en/cv.html"},
}


def url(key, lang):
    return "/" + ROUTES[key][lang].replace("index.html", "")


def pdf(lang):
    return f"/{lang}/cv.pdf"


def esc(s):
    return html.escape(s, quote=True)


def todo(text):
    """Wrap every [placeholder] so it stays visible but reads as a note."""
    return re.sub(r"(\[[^\]]+\])", r'<span class="todo">\1</span>', text)


# --------------------------------------------------------------------------
# Organic blob shapes (from the design handoff, viewBox -2 -2 104 104)
# --------------------------------------------------------------------------

PATHS = {
    "hero": "M93.8 48.3C93.1 52.9 93.6 58.0 91.9 63.3C90.2 68.5 87.2 76.0 83.7 79.9C80.2 83.8 75.2 84.7 71.0 86.6C66.7 88.5 63.3 90.9 58.4 91.5C53.4 92.0 45.5 91.4 41.2 90.2C37.0 88.9 36.8 85.8 32.9 84.0C29.1 82.1 23.4 82.0 18.4 78.9C13.3 75.8 5.7 70.4 2.8 65.2C-0.2 60.1 0.3 53.8 0.6 48.1C0.8 42.3 2.2 35.0 4.3 30.5C6.4 26.0 8.9 23.3 13.3 21.0C17.7 18.7 25.6 18.1 30.7 16.6C35.7 15.2 39.3 13.6 43.7 12.3C48.0 11.0 52.1 8.8 56.6 8.9C61.0 9.0 65.0 11.0 70.3 12.9C75.6 14.9 83.9 16.5 88.2 20.4C92.4 24.3 95.0 31.6 95.9 36.3C96.9 40.9 94.5 43.8 93.8 48.3Z",
    "a": "M88.0 51.1C87.3 55.3 88.4 56.6 87.3 61.2C86.2 65.9 84.1 74.6 81.2 79.2C78.4 83.8 73.8 86.0 70.0 88.9C66.2 91.9 63.2 95.6 58.4 96.8C53.7 98.0 46.3 97.5 41.6 96.1C37.0 94.7 35.1 91.1 30.6 88.6C26.2 86.1 18.8 85.1 15.0 81.0C11.2 76.8 9.1 69.2 8.0 63.8C6.9 58.4 8.0 53.3 8.5 48.5C9.0 43.7 9.6 39.0 11.0 35.2C12.3 31.3 13.6 28.2 16.7 25.3C19.9 22.4 25.3 21.6 29.9 17.9C34.6 14.2 39.9 6.0 44.5 3.1C49.1 0.2 52.4 -0.2 57.4 0.5C62.5 1.2 69.9 4.7 74.9 7.3C79.9 10.0 84.5 11.7 87.2 16.5C89.9 21.3 90.9 30.3 91.1 36.1C91.2 41.9 88.6 46.9 88.0 51.1Z",
    "b": "M94.6 48.5C94.5 53.7 94.0 61.9 92.6 67.3C91.3 72.7 89.5 77.3 86.6 80.8C83.7 84.2 80.1 86.4 75.2 88.2C70.2 90.0 62.5 91.5 56.9 91.7C51.3 91.9 45.6 90.9 41.6 89.3C37.6 87.6 37.2 84.2 32.9 81.9C28.7 79.5 21.0 78.0 16.2 75.1C11.4 72.2 6.7 68.1 4.3 64.3C1.9 60.6 1.8 57.9 1.8 52.7C1.8 47.5 1.7 39.0 4.1 33.3C6.5 27.6 12.2 21.4 16.1 18.3C20.0 15.2 23.4 15.8 27.6 14.6C31.8 13.4 36.4 12.2 41.3 11.2C46.3 10.2 52.3 8.2 57.1 8.6C61.9 8.9 66.1 11.3 70.2 13.4C74.3 15.5 77.9 17.4 81.8 21.2C85.7 25.0 91.4 31.7 93.5 36.3C95.6 40.8 94.8 43.3 94.6 48.5Z",
    "c": "M89.9 51.8C88.7 57.3 88.0 61.8 86.3 65.5C84.6 69.1 82.2 70.4 79.5 73.6C76.8 76.9 73.5 81.2 70.1 84.9C66.8 88.7 64.4 94.4 59.5 96.3C54.5 98.2 45.2 97.6 40.2 96.4C35.3 95.2 34.0 91.9 29.9 89.3C25.7 86.7 19.0 85.2 15.3 80.9C11.5 76.7 8.7 69.2 7.2 63.6C5.7 58.1 6.0 52.6 6.2 47.7C6.5 42.8 6.5 38.0 8.5 34.1C10.4 30.2 14.3 27.3 18.0 24.4C21.8 21.4 26.7 19.1 30.8 16.5C35.0 13.9 38.7 10.3 43.1 8.6C47.5 7.0 51.8 6.5 57.2 6.6C62.7 6.6 70.2 7.1 75.8 8.9C81.5 10.7 88.2 13.5 91.1 17.5C94.1 21.5 93.8 27.1 93.6 32.8C93.4 38.5 91.2 46.4 89.9 51.8Z",
}


def blob(shape, tone):
    return (f'<div class="blob blob--{tone}" aria-hidden="true">'
            f'<svg viewBox="-2 -2 104 104" preserveAspectRatio="none" focusable="false">'
            f'<path d="{PATHS[shape]}"/></svg></div>')


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------

IMAGES = {
    "hero": ("hero-dashboard", 1672, 941, 840),
    "kalbos": ("kalbos-mokinys", 1663, 880, 840),
    "kalbos_admin": ("kalbos-admin", 1664, 878, 840),
    "kalbos_task": ("kalbos-uzduotis", 1662, 879, 840),
    "tik": ("tikmaker-editor", 1400, 812, 760),
    "loy_cards": ("loyalty-cards", 1400, 773, 760),
    "loy_promo": ("loyalty-promotions", 1400, 774, 760),
    "about": ("about-photo", 1122, 1402, 600),
    "kalbos_import": ("kalbos-import", 1100, 600, 760),
    "tik_library": ("tikmaker-library", 1000, 525, 760),
    "tik_voice": ("tikmaker-voice", 840, 530, 760),
}


def img(key, alt, sizes, lazy=True, priority=False):
    name, w, h, small = IMAGES[key]
    attrs = [
        f'src="/img/site/{name}.webp"',
        f'srcset="/img/site/{name}-{small}.webp {small}w, /img/site/{name}.webp {w}w"',
        f'sizes="{sizes}"',
        f'width="{w}" height="{h}"',
        f'alt="{esc(alt)}"',
        'decoding="async"',
    ]
    if lazy:
        attrs.append('loading="lazy"')
    if priority:
        attrs.append('fetchpriority="high"')
    return "<img " + " ".join(attrs) + ">"


def frame_bar():
    return '<div class="frame__bar" aria-hidden="true"><span></span><span></span><span></span></div>'


def framed(key, alt, sizes, dark=False, crop=True):
    cls = "frame frame--dark" if dark else "frame"
    image = img(key, alt, sizes)
    body = f'<div class="frame__screen">{image}</div>' if crop else image
    return f'<div class="{cls}">{frame_bar()}{body}</div>'


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

ICON_MENU = ('<svg aria-hidden="true" width="22" height="22" viewBox="0 0 22 22" fill="none" '
             'stroke="currentColor" stroke-width="1.6"><path d="M3 7h16M3 15h16"/></svg>')
ICON_CLOSE = ('<svg aria-hidden="true" width="22" height="22" viewBox="0 0 22 22" fill="none" '
              'stroke="currentColor" stroke-width="1.6"><path d="M5 5l12 12M17 5L5 17"/></svg>')
ICON_PLUS = ('<svg aria-hidden="true" width="18" height="18" viewBox="0 0 18 18" fill="none" '
             'stroke="currentColor" stroke-width="1.5"><path d="M9 3v12M3 9h12"/></svg>')


def lang_link(lang, key, cls="lang"):
    other = "en" if lang == "lt" else "lt"
    label = ("Kalba: lietuvių. Perjungti į anglų" if lang == "lt"
             else "Language: English. Switch to Lithuanian")
    # Wrapped in a span: as direct flex children the bold and plain runs
    # would lose the spaces around the slash.
    text = "<span><b>LT</b> / EN</span>" if lang == "lt" else "<span>LT / <b>EN</b></span>"
    return (f'<a class="{cls}" href="{url(key, other)}" hreflang="{other}" '
            f'aria-label="{label}">{text}</a>')


def asset(path):
    """Root-relative URL with a content hash, so a new deploy is never
    hidden behind a stylesheet or script the browser has cached."""
    import hashlib
    digest = hashlib.md5((ROOT / path.lstrip("/")).read_bytes()).hexdigest()[:8]
    return f"{path}?v={digest}"


def head(lang, key, title, desc, *, noindex=False, jsonld=None, og_type="website"):
    canonical = SITE + url(key, lang)
    alts = ""
    if not noindex:
        alts = (f'<link rel="alternate" hreflang="lt" href="{SITE + url(key, "lt")}">\n'
                f'<link rel="alternate" hreflang="en" href="{SITE + url(key, "en")}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE + url(key, "lt")}">\n')
    robots = "noindex,follow" if noindex else "index,follow"
    locale = "lt_LT" if lang == "lt" else "en_GB"
    ld = ""
    for block in jsonld or []:
        ld += ('<script type="application/ld+json">\n'
               + json.dumps(block, ensure_ascii=False, indent=2) + "\n</script>\n")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{alts}<meta name="theme-color" content="#F6F0E6">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Codeart">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/img/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/schibsted-grotesk/schibsted-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset("/css/site.css")}">
<script>
  /* Hide reveal-on-scroll content only once we know JS runs. If site.js
     never arrives, put everything back after a moment. */
  document.documentElement.classList.add("js");
  setTimeout(function () {{ if (!window.__site) document.documentElement.classList.remove("js"); }}, 3000);
</script>
<script src="{asset("/js/site.js")}" defer></script>
{ld}</head>
"""


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path)


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

T = {
    "lt": {
        "skip": "Pereiti prie turinio",
        "nav_label": "Pagrindinė navigacija",
        "menu_open": "Atidaryti meniu",
        "menu_close": "Uždaryti meniu",
        "menu": "Meniu",
        "cta": "Aptarti projektą",
        "read_more": "Skaityti plačiau",
        "ids": {"work": "darbai", "services": "paslaugos", "about": "apie", "faq": "duk", "contact": "kontaktai"},
        "nav": {"work": "Darbai", "services": "Paslaugos", "about": "Apie", "faq": "DUK"},
        "home_title": "Verslo sistemų ir web aplikacijų kūrimas | Programuotoja Vilniuje",
        "home_desc": "Vidiniai įrankiai, valdymo skydeliai ir web aplikacijos nuo idėjos iki paleidimo. Fiksuota kaina, sutarta prieš pradedant. Programuotoja Vilniuje.",
        "h1": "Verslo sistemų ir web aplikacijų kūrimas",
        "lead": "Vidiniai įrankiai, valdymo skydeliai ir web aplikacijos nuo idėjos iki paleidimo. Fiksuota kaina, sutarta prieš pradedant.",
        "see_work": "Peržiūrėti darbus",
        "hero_note": "React, TypeScript, .NET · API ir AI funkcijos",
        "hero_alt": "Pavyzdinė transporto valdymo sistema: transporto priemonių sąrašas, maršrutas žemėlapyje ir paskutinės lokacijos",
        "work_h": "Atlikti darbai",
        "all_projects": "Visi projektai →",
        "works": [
            ("p_lang", "a", "rose", "kalbos", False, "Kalbų mokymosi platforma",
             "Vieša svetainė, mokinio platforma ir turinio valdymas vienoje sistemoje. Administratorius kursus kuria pats, o užduotys sudaromos automatiškai iš žodyno.",
             "Next.js · Supabase",
             "Kalbų platformos mokinio pradžios ekranas: kurso žemėlapis, tęsiama pamoka, kartojimas ir progresas"),
            ("p_tik", "b", "lavender", "tik", True, "TikMaker",
             "Trumpų vertikalių vaizdo įrašų redaktorius: video surenkamas iš paruoštų scenų, o balsas ir subtitrai sukuriami iš teksto.",
             "React · Remotion · ElevenLabs",
             "TikMaker redaktorius: scenos, peržiūra ir laiko juosta su keliomis eilėmis"),
            ("p_loy", "c", "sand", "loy_cards", False, "Lojalumo valdymo sistema",
             "Kortelės, klientai, akcijos ir kuponai vienoje administravimo sistemoje.",
             "React · TypeScript · .NET",
             "Lojalumo sistema: kortelių sąrašas ir pasirinktos kortelės detalės, duomenys uždengti"),
        ],
        "services_h": "Su kuo galiu padėti",
        "services": [
            ("Nauja sistema nuo nulio", "Tinka, kai reikia ne puslapio, o veikiančio produkto.",
             "Padedu išgryninti sprendimą, suprojektuoju sąsają ir sukuriu sistemą nuo frontendo iki API ir duomenų bazės."),
            ("Esamos sistemos gerinimas", "Tinka, kai sistema veikia, bet lėta ar sunkiai vystoma.",
             "Pirmiausia randu, kur problema, tada tvarkau tai, kas iš tikrųjų trukdo."),
            ("Naujos funkcijos esamai sistemai", "Tinka, kai produkto nereikia perrašyti.",
             "Perprantu esamą kodą ir kuriu naujas funkcijas, negriaudama to, kas jau veikia."),
        ],
        "steps_h": "Kaip vyksta darbas",
        "steps": [
            ("Parašote", "Aprašote idėją ar problemą."),
            ("Planas ir kaina", "Per 24 val. po pokalbio gaunate planą ir fiksuotą kainą raštu."),
            ("Kūrimas", "Progresą matote nuolat, ne tik pabaigoje."),
            ("Paleidimas", "Įdiegiu sistemą ir paruošiu instrukcijas, kaip ja naudotis. Mano darbui taikoma 3 mėn. garantija."),
        ],
        "about_h": "Apie mane",
        "about_alt": "Gabrielė Tamaševičiūtė",
        "about_text": "Esu Gabrielė. Man patinka kurti sistemas, kurios žmonėms iš tikrųjų padeda: sutaupo laiko, sumažina chaosą ir leidžia susitelkti į tai, kas svarbu. Labiausiai džiaugiuosi, kai matau, kad mano darbu žmonės naudojasi kasdien ir yra juo patenkinti.",
        "facts": ["3+ metai kuriant sistemas", "Frontend, backend, API ir AI", "Nuo idėjos iki paleidimo"],
        "about_more": "Daugiau apie mane →",
        "faq_h": "Dažni klausimai",
        "faq": [
            ("Kiek kainuoja projektas?", "Kaina priklauso nuo apimties, integracijų ir to, ką sistema turi mokėti. Po trumpo pokalbio per 24 val. atsiunčiu darbų planą ir fiksuotą kainą raštu: perkate rezultatą, ne valandas."),
            ("Kiek laiko trunka?", "Priklauso nuo apimties: nedidelis patobulinimas gali užtrukti kelias dienas, nauja sistema – nuo kelių savaičių. Tikslų terminą nurodau plane kartu su kaina, dar prieš pradedant darbus."),
            ("Ar galite perimti jau veikiančią sistemą?", "Taip. Nebūtina visko kurti iš naujo: galiu tęsti darbą su jūsų esama sistema, sutvarkyti tai, kas neveikia ar trukdo, ir pridėti naujų funkcijų."),
            ("Ar kaina gali pasikeisti eigoje?", "Ne, sutarta kaina nesikeičia. Jei darbo eigoje sugalvojate ką nors naujo ir didesnio, tai aptariame atskirai. Smulkius pageidavimus dažniausiai tiesiog įtraukiu: man svarbu, kad sistema jums tiktų."),
            ("Ar galite į sistemą įdiegti AI funkcijas?", "Taip. Pavyzdžiui, galiu sukurti pokalbių asistentą, kuris atsako klientams į klausimus pagal jūsų informaciją, automatiškai rašyti tekstus ar produktų aprašymus, apibendrinti dokumentus ir laiškus, išversti turinį į kitas kalbas ar padėti greičiau rasti reikiamą informaciją. Jei turite savo idėją, kaip AI galėtų palengvinti jūsų darbą, parašykite: kartu įvertinsime, kaip ją įgyvendinti."),
            ("Ar paruošiate instrukcijas, kaip naudotis sistema?", "Taip. Kartu su sistema paruošiu naudojimo instrukcijas ir reikalingą dokumentaciją, o pageidaujant ir video mokymus jūsų komandai, kad visi greitai perprastų naują sistemą."),
        ],
        "contact_h": "Turite projekto idėją?",
        "contact_lead": "Parašykite kelis sakinius apie savo projektą. Paprastai atsakau per 24 val.",
        "f_name": "Vardas",
        "f_email": "El. paštas",
        "f_msg": "Žinutė",
        "f_send": "Siųsti",
        "f_hp": "Šio lauko nepildykite",
        "f_subject": "Nauja žinutė iš codeart.lt",
        "f_sending": "Siunčiama…",
        "f_ok": "Ačiū! Žinutė išsiųsta, atsakysiu el. paštu.",
        "f_fail": "Nepavyko išsiųsti. Parašykite tiesiai el. paštu: " + EMAIL,
        "f_invalid": "Užpildykite visus laukus ir patikrinkite el. pašto adresą.",
        "footer_cv": "CV ir portfolio",
        "menu_nums": {"work": "01", "services": "02", "about": "04", "faq": "05"},
    },
    "en": {
        "skip": "Skip to content",
        "nav_label": "Main navigation",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "menu": "Menu",
        "cta": "Discuss a project",
        "read_more": "Read more",
        "ids": {"work": "work", "services": "services", "about": "about", "faq": "faq", "contact": "contact"},
        "nav": {"work": "Work", "services": "Services", "about": "About", "faq": "FAQ"},
        "home_title": "Business systems and web app development | Developer in Vilnius",
        "home_desc": "Internal tools, admin dashboards and web applications from idea to launch. Fixed price, agreed before we start. Developer based in Vilnius.",
        "h1": "Business systems and web application development",
        "lead": "Internal tools, admin dashboards and web applications from idea to launch. Fixed price, agreed before we start.",
        "see_work": "See my work",
        "hero_note": "React, TypeScript, .NET · APIs and AI features",
        "hero_alt": "Sample fleet management system: a vehicle list, a route on the map and the latest locations",
        "work_h": "Selected work",
        "all_projects": "All projects →",
        "works": [
            ("p_lang", "a", "rose", "kalbos", False, "Language learning platform",
             "A public website, a learner platform and content management in one system. The admin builds courses on their own, and exercises are generated automatically from the vocabulary.",
             "Next.js · Supabase",
             "The learner home screen of the language platform: course map, lesson in progress, review and progress"),
            ("p_tik", "b", "lavender", "tik", True, "TikMaker",
             "An editor for short vertical videos: a video is assembled from ready-made scenes, and the voice-over and subtitles are generated from text.",
             "React · Remotion · ElevenLabs",
             "The TikMaker editor: scenes, preview and a multi-row timeline"),
            ("p_loy", "c", "sand", "loy_cards", False, "Loyalty management system",
             "Cards, customers, promotions and coupons in one admin system.",
             "React · TypeScript · .NET",
             "Loyalty system: the card list and the selected card's details, data masked"),
        ],
        "services_h": "How I can help",
        "services": [
            ("A new system from scratch", "When you need a working product, not a web page.",
             "I help pin down the solution, design the interface and build the system from frontend to API and database."),
            ("Improving an existing system", "When the system works but is slow or hard to develop further.",
             "First I find where the problem is, then I fix what actually gets in the way."),
            ("New features for an existing system", "When the product doesn't need a rewrite.",
             "I get to know the existing code and build new features without breaking what already works."),
        ],
        "steps_h": "How the work goes",
        "steps": [
            ("You write", "You describe the idea or problem."),
            ("Plan and price", "Within 24 hours of our call you get a plan and a fixed price in writing."),
            ("Building", "You see progress all along, not only at the end."),
            ("Launch", "I deploy the system and prepare guides on how to use it. My work comes with a 3-month warranty."),
        ],
        "about_h": "About me",
        "about_alt": "Gabrielė Tamaševičiūtė",
        "about_text": "I'm Gabrielė. I love building systems that genuinely help people: they save time, cut down the chaos and let people focus on what matters. What makes me happiest is seeing people use my work every day and be glad they have it.",
        "facts": ["3+ years building systems", "Frontend, backend, APIs and AI", "From idea to launch"],
        "about_more": "More about me →",
        "faq_h": "Frequently asked questions",
        "faq": [
            ("How much does a project cost?", "It depends on the scope, the integrations and what the system needs to do. After a short call I send a work plan and a fixed price in writing within 24 hours: you pay for the result, not for hours."),
            ("How long does it take?", "It depends on the scope: a small improvement can take a few days, a new system from a few weeks. I give the exact timeline in the plan, together with the price, before any work starts."),
            ("Can you take over a system that's already running?", "Yes. There's no need to start from scratch: I can keep working on your existing system, fix what doesn't work or gets in the way, and add new features."),
            ("Can the price change along the way?", "No, the agreed price doesn't change. If you come up with something new and bigger along the way, we discuss it separately. Small requests I usually just include: what matters to me is that the system suits you."),
            ("Can you add AI features to the system?", "Yes. For example, I can build a chat assistant that answers your customers' questions from your own information, write texts or product descriptions automatically, summarise documents and emails, translate content into other languages, or help people find what they need faster. If you have your own idea of how AI could make your work easier, get in touch and we'll work out how to make it happen."),
            ("Do you prepare guides on how to use the system?", "Yes. Along with the system I prepare user guides and the documentation you need, and on request video training for your team, so everyone gets comfortable with the new system quickly."),
        ],
        "contact_h": "Have a project idea?",
        "contact_lead": "Write a few sentences about your project. I usually reply within 24 hours.",
        "f_name": "Name",
        "f_email": "Email",
        "f_msg": "Message",
        "f_send": "Send",
        "f_hp": "Leave this field empty",
        "f_subject": "New message from codeart.lt (EN)",
        "f_sending": "Sending…",
        "f_ok": "Thank you! Your message has been sent, I'll reply by email.",
        "f_fail": "Sending failed. Please email me directly: " + EMAIL,
        "f_invalid": "Please fill in all fields and check the email address.",
        "footer_cv": "CV and portfolio",
        "menu_nums": {"work": "01", "services": "02", "about": "04", "faq": "05"},
    },
}


# --------------------------------------------------------------------------
# Icons (24px grid, stroke follows currentColor)
# --------------------------------------------------------------------------

ICONS = {
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "phone": '<path d="M5 4h3.5l2 5-2.4 1.6a11 11 0 0 0 5.3 5.3L15 13.5l5 2V19a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V17M8 7.5v.01M12 17v-3.5a2.5 2.5 0 0 1 5 0V17M12 10.5V17"/>',
    "github": '<path d="M9 19c-4 1.5-4-2.5-6-3m12 6v-3.9a3.4 3.4 0 0 0-.9-2.6c3.1-.4 6.4-1.5 6.4-7A5.4 5.4 0 0 0 19 3.8 5.1 5.1 0 0 0 18.9 1S17.7.7 15 2.5a13.4 13.4 0 0 0-6 0C6.3.7 5.1 1 5.1 1A5.1 5.1 0 0 0 5 3.8a5.4 5.4 0 0 0-1.5 3.7c0 5.5 3.3 6.6 6.4 7A3.4 3.4 0 0 0 9 18.1V22"/>',
    "tiktok": '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.4 2.6 2.4 4.6 5 5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "plus": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/>',
    "system": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="m7.5 11 2.5-2.5 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    "shield": '<path d="M12 3 20 6v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 12v6M9 15l3 3 3-3"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
}


def icon(name, size=20):
    return (f'<svg class="ico" aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONS[name]}</svg>')


def icon_blob(name, tone):
    """A line icon sitting on a small organic blob, used on cards."""
    return (f'<span class="ico-blob ico-blob--{tone}" aria-hidden="true">'
            f'<svg class="ico-blob__shape" viewBox="-2 -2 104 104" preserveAspectRatio="none">'
            f'<path d="{PATHS["a"]}"/></svg>{icon(name, 24)}</span>')


# --------------------------------------------------------------------------
# Content shared by the new pages
# --------------------------------------------------------------------------

PHONE = "+370 672 70403"
PHONE_HREF = "tel:+37067270403"

C = {
    "lt": {
        "nav": [("portfolio", "Portfolio"), ("services", "Paslaugos"), ("about", "Apie"),
                ("contact", "Kontaktai")],
        "home": "Pagrindinis",
        "links_h": "Nuorodos",
        "rights": "Visos teisės saugomos",
        "cta_h": "Turite projekto idėją?",
        "cta_p": "Trumpai papasakokite apie projektą. Atsakau per 24 val. su darbų planu ir kaina.",
        "cta_btn": "Susisiekti",
        "contact_items": [
            ("mail", "El. paštas", EMAIL, "mailto:" + EMAIL),
            ("phone", "Telefonas", PHONE, PHONE_HREF),
            ("linkedin", "LinkedIn", "Gabrielė Tamaševičiūtė", LINKEDIN),
            ("github", "GitHub", "github.com/gabwowce", GITHUB),
            ("tiktok", "TikTok", "@gabiebuilds", TIKTOK),
            ("pin", "Vieta", "Vilnius, Lietuva", None),
        ],
        "reply": "Paprastai atsakau per 24 val.",
        "services_more": "Visos paslaugos →",
        "svc_cta": "Aptarti projektą →",
        "includes": "Apima",
        "steps_cta_note": "Planą ir fiksuotą kainą raštu gaunate per 24 val. po pokalbio.",
        # services page
        "svc_title": "Paslaugos | Gabrielė Tamaševičiūtė · Codeart",
        "svc_desc": "Naujos sistemos nuo nulio, esamų sistemų gerinimas ir naujos funkcijos. Fiksuota kaina, sutarta prieš pradedant, ir 3 mėn. garantija.",
        "svc_eyebrow": "Paslaugos",
        "svc_h1": "Su kuo galiu padėti",
        "svc_lead": "Dirbu su sistemomis, o ne su pavieniais puslapiais. Galiu startuoti nuo nulio arba perimti tai, kas jau veikia.",
        "svc_list_h": "Ką darau",
        "price_h": "Kaina ir garantija",
        "price": [
            ("tag", "Fiksuota kaina", "Kiekvienam projektui pateikiu fiksuotą kainos pasiūlymą, sutartą prieš pradedant: perkate rezultatą, ne valandas, ir sąskaitoje nebūna netikėtumų. Kaina priklauso nuo apimties, integracijų ir to, ką sistema turi mokėti."),
            ("shield", "3 mėn. garantija", "Jei per 3 mėnesius po paleidimo paaiškėja klaida, atsiradusi dėl mano įgyvendinto sprendimo, ją ištaisau be papildomo mokesčio."),
        ],
        "expect_h": "Ko galite tikėtis",
        "expect": ["Fiksuota sutarta kaina", "Jokių netikėtų papildomų darbų", "Nuolat matomas progresas",
                   "Sprendimai, kurie turi tikslą", "UX, kuriuo patogu naudotis", "Instrukcijos, dokumentacija ir, jei reikia, video mokymai", "3 mėn. garantija mano darbui"],
        # about page
        "about_title": "Apie mane | Gabrielė Tamaševičiūtė · Codeart",
        "about_desc": "Gabrielė Tamaševičiūtė, programuotoja iš Vilniaus: kaip dirbu, vertybės, patirtis ir išsilavinimas.",
        "about_eyebrow": "Apie mane",
        "about_h1": "Esu Gabrielė",
        "about_paras": [
            "Man patinka kurti sistemas, kurios žmonėms iš tikrųjų padeda: sutaupo laiko, sumažina chaosą ir leidžia susitelkti į tai, kas svarbu. Labiausiai džiaugiuosi, kai matau, kad mano darbu žmonės naudojasi kasdien ir yra juo patenkinti.",
            "Kuriu web ir mobilias sistemas nuo idėjos iki veikiančio produkto ir dirbu per visą jų grandinę: projektuoju vartotojo sąsajas, sistemos architektūrą, API sąveikas ir duomenų struktūras.",
            "Šiuo metu nuo nulio vystau vidinę verslo sistemą kaip vienintelė frontend programuotoja. Pati išsigryninau poreikius, suprojektavau architektūrą ir vartotojo patirtį, aprašau backend funkcionalumą bei derinu techninius sprendimus su backend programuotoju.",
        ],
        "about_cv": "CV ir portfolio",
        "about_pdf": "Atsisiųsti CV (PDF)",
        "how_h": "Kaip dirbu",
        "how": [
            ("system", "Galvoju apie visą sistemą", "Žiūriu ne tik į ekraną, kurį tuo metu kuriu. Vertinu duomenų srautą, API, būsenas, naudotojų teises ir tai, kaip sprendimas paveiks kitas sistemos dalis."),
            ("search", "Pirma suprantu problemą", "Kai kažkas neveikia ar veikia blogai, pirmiausia ieškau priežasties. Tik tada keičiu kodą. Tai ypač svarbu dirbant su jau veikiančiomis ir didesnėmis sistemomis."),
            ("code", "Galiu dirbti su esamu kodu", "Nebūtina visko pradėti iš naujo. Galiu perprasti svetimą kodą, esamą architektūrą ir palaipsniui sistemą gerinti ar papildyti."),
            ("spark", "Seku šiuolaikines technologijas", "Naudoju AI įrankius kūrimo procese ir integruoju AI funkcijas į pačius produktus: nuo paprastų LLM funkcijų iki agentų, galinčių naudotis sistemos API."),
        ],
        "values_h": "Vertybės",
        "values": [
            ("eye", "Aiškumas", "Jokių dviprasmybių, iš karto aišku, ko reikia."),
            ("list", "Struktūra", "Darbas žingsniais, ne chaosu."),
            ("shield", "Patikimumas", "Ką pažadu, tą ir padarau."),
            ("chat", "Komunikacija", "Greiti atsakymai, visada aiškus statusas."),
            ("code", "Kodo kokybė", "Švarus, testuotas, pernaudojamas kodas."),
            ("target", "Atsakomybė", "Man rūpi rezultatas, ne tik užduotis."),
        ],
        "exp_h": "Patirtis",
        "exp": [
            ("Programuotoja (Mid)", "UVS", "2026 kov. – dabar", "Vilnius · React, TypeScript, C#/.NET",
             "Kuriu vidinę verslo sistemą nuo nulio kaip vienintelė frontend programuotoja komandoje: pati suprojektavau architektūrą ir sąsają, išsiaiškinau poreikius ir suplanavau backend struktūrą. Deleguoju užduotis backend kolegai, tikrinu rezultatą ir atsakau už visą frontend dalį."),
            ("Web ir mobile app programuotoja", "Laisvai samdoma", "2025 kov. – dabar", "Vilnius · React, Next.js, TypeScript, Tailwind, WordPress, Figma",
             "Kuriu web ir mobiliąsias aplikacijas nuo idėjos iki veikiančio produkto: projektuoju architektūrą ir duomenų struktūrą, kuriu frontend, backend ir API, autentifikaciją bei duomenų bazės logiką. Esu kūrusi „Kibinukai“ užsakymų sistemą ir kelionių aplikaciją, kuriose buvau atsakinga už techninę architektūrą ir pilną funkcionalumo įgyvendinimą. Projektus savarankiškai vedu nuo poreikių išgryninimo iki paleidimo."),
            ("Jaunesnioji programuotoja", "UVS", "2024 birž. – 2026 vas.", "Vilnius · C#/.NET, WPF (XAML), UI prieinamumas",
             "Dirbau su WPF pagrindu sukurta SCO sistema: kūriau ir tobulinau aplikacijos ekranus naudodama XAML/XML ir C#, įgyvendinau naują funkcionalumą bei taisiau esamus sprendimus. Analizavau klaidas, debug'inau aplikaciją ir logus, ieškojau problemų priežasčių bei jas sprendžiau. Taip pat projektavau ekranų dizainą, rūpinausi UI prieinamumu ir ruošiau vizualinius elementus sistemai."),
            ("Planuotoja", "Girteka Europe West", "2021 spal. – 2023 rugp.", "Vilnius · Planavimas, prioritetai, komunikacija", ""),
            ("Administratorė", "UAB „Jarinta“", "2021 kov. – 2021 rugs.", "Vilnius", ""),
        ],
        "edu_h": "Išsilavinimas",
        "edu": ("Vilniaus kolegija", "Programų sistemos", "2023–2027 · studijuoju"),
        "lang_h": "Kalbos",
        "langs": [("Lietuvių", "gimtoji"), ("Anglų", "B2"), ("Rusų", "B2")],
        # contact page
        "contact_title": "Kontaktai | Gabrielė Tamaševičiūtė · Codeart",
        "contact_desc": "Parašykite apie savo projektą: el. paštas, telefonas ir kontaktų forma. Paprastai atsakau per 24 val.",
        "contact_eyebrow": "Kontaktai",
        "contact_h1": "Turite projekto idėją?",
        "contact_lead": "Papasakokite apie savo projektą: ką norite sukurti ar kokią problemą išspręsti.",
        "direct_h": "Tiesiogiai",
        "f_phone": "Tel. numeris (nebūtina)",
        "next_h": "Kas bus toliau",
        "next": [
            ("Parašote", "Trumpai papasakojate apie savo projektą ar idėją."),
            ("Trumpas pokalbis", "Per 20 min. išsigryniname poreikį, apimtį ir ar galiu būti tinkamas žmogus jūsų projektui."),
            ("Aiškus planas ir kaina", "Per 24 val. atsiunčiu darbų planą, terminus ir fiksuotą kainą. Pradedame tik tada, kai viskas aišku abiem pusėms."),
        ],
    },
    "en": {
        "nav": [("portfolio", "Portfolio"), ("services", "Services"), ("about", "About"),
                ("contact", "Contact")],
        "home": "Home",
        "links_h": "Links",
        "rights": "All rights reserved",
        "cta_h": "Have a project idea?",
        "cta_p": "Tell me briefly about your project. I reply within 24 hours with a work plan and a price.",
        "cta_btn": "Get in touch",
        "contact_items": [
            ("mail", "Email", EMAIL, "mailto:" + EMAIL),
            ("phone", "Phone", PHONE, PHONE_HREF),
            ("linkedin", "LinkedIn", "Gabrielė Tamaševičiūtė", LINKEDIN),
            ("github", "GitHub", "github.com/gabwowce", GITHUB),
            ("tiktok", "TikTok", "@gabiebuilds", TIKTOK),
            ("pin", "Location", "Vilnius, Lithuania", None),
        ],
        "reply": "I usually reply within 24 hours.",
        "services_more": "All services →",
        "svc_cta": "Discuss a project →",
        "includes": "Includes",
        "steps_cta_note": "You get a plan and a fixed price in writing within 24 hours of our call.",
        "svc_title": "Services | Gabrielė Tamaševičiūtė · Codeart",
        "svc_desc": "New systems from scratch, improving existing systems and new features. A fixed price agreed before we start, and a 3-month warranty.",
        "svc_eyebrow": "Services",
        "svc_h1": "How I can help",
        "svc_lead": "I work on systems, not one-off pages. I can start from scratch or take over what's already running.",
        "svc_list_h": "What I do",
        "price_h": "Price and warranty",
        "price": [
            ("tag", "Fixed price", "For every project I give a fixed price, agreed before we start: you pay for the result, not for hours, and there are no surprises on the invoice. The price depends on the scope, the integrations and what the system needs to do."),
            ("shield", "3-month warranty", "If within 3 months of launch a bug turns up that comes from my implementation, I fix it at no extra cost."),
        ],
        "expect_h": "What you can expect",
        "expect": ["A fixed, agreed price", "No unexpected extra work", "Progress you can always see",
                   "Decisions with a purpose", "UX that's comfortable to use", "Guides, documentation and video training if needed", "A 3-month warranty on my work"],
        "about_title": "About me | Gabrielė Tamaševičiūtė · Codeart",
        "about_desc": "Gabrielė Tamaševičiūtė, a developer in Vilnius: how I work, values, experience and education.",
        "about_eyebrow": "About me",
        "about_h1": "I'm Gabrielė",
        "about_paras": [
            "I love building systems that genuinely help people: they save time, cut down the chaos and let people focus on what matters. What makes me happiest is seeing people use my work every day and be glad they have it.",
            "I build web and mobile systems from idea to a working product and work across the whole chain: user interfaces, system architecture, API interactions and data structures.",
            "I'm currently building an internal business system from scratch as the sole frontend developer. I worked out the requirements myself, designed the architecture and user experience, spec out backend functionality, and align technical decisions with the backend developer.",
        ],
        "about_cv": "CV and portfolio",
        "about_pdf": "Download CV (PDF)",
        "how_h": "How I work",
        "how": [
            ("system", "I think about the whole system", "I look beyond the screen I'm building. I consider the data flow, the API, states, user permissions and how a decision will affect other parts of the system."),
            ("search", "I understand the problem first", "When something doesn't work or works badly, I look for the cause first. Only then do I change the code. This matters most with existing and larger systems."),
            ("code", "I can work with existing code", "Not everything has to start from scratch. I can get to grips with someone else's code and existing architecture, and improve or extend the system step by step."),
            ("spark", "I keep up with modern technology", "I use AI tools in development and build AI features into products themselves, from simple LLM features to agents that can use the system's API."),
        ],
        "values_h": "Values",
        "values": [
            ("eye", "Clarity", "No ambiguity, clear on what's needed from the start."),
            ("list", "Structure", "Work broken into steps, not chaos."),
            ("shield", "Reliability", "I do what I say I will."),
            ("chat", "Communication", "Quick replies, status always clear."),
            ("code", "Code quality", "Clean, tested, reusable code."),
            ("target", "Ownership", "I care about the outcome, not just the task."),
        ],
        "exp_h": "Experience",
        "exp": [
            ("Developer (Mid)", "UVS", "Mar 2026 – present", "Vilnius · React, TypeScript, C#/.NET",
             "Building an internal business system from scratch as the sole frontend developer on the team: I designed the architecture and interface myself, worked out the requirements and planned the backend structure. I hand off tasks to a backend colleague, review the result, and own the frontend end to end."),
            ("Web & mobile app developer", "Self-employed", "Mar 2025 – present", "Vilnius · React, Next.js, TypeScript, Tailwind, WordPress, Figma",
             "Building web and mobile apps from idea to working product: I design the architecture and data structure, and build the frontend, backend and API, authentication and database logic. I built the “Kibinukai” ordering system and a travel app, where I owned the technical architecture and the full implementation. I run projects independently, from scoping the requirements to launch."),
            ("Junior developer", "UVS", "Jun 2024 – Feb 2026", "Vilnius · C#/.NET, WPF (XAML), UI accessibility",
             "Worked on a WPF-based SCO system: built and improved application screens using XAML/XML and C#, implemented new functionality and fixed existing issues. Analysed bugs, debugged the application and logs, and tracked down and resolved root causes. Also designed screen layouts, worked on UI accessibility, and prepared visual assets for the system."),
            ("Planner", "Girteka Europe West", "Oct 2021 – Aug 2023", "Vilnius · Planning, priorities, communication", ""),
            ("Administrator", "UAB “Jarinta”", "Mar 2021 – Sep 2021", "Vilnius", ""),
        ],
        "edu_h": "Education",
        "edu": ("Vilnius University of Applied Sciences", "Software Systems", "2023–2027 · in progress"),
        "lang_h": "Languages",
        "langs": [("Lithuanian", "native"), ("English", "B2"), ("Russian", "B2")],
        "contact_title": "Contact | Gabrielė Tamaševičiūtė · Codeart",
        "contact_desc": "Tell me about your project: email, phone and a contact form. I usually reply within 24 hours.",
        "contact_eyebrow": "Contact",
        "contact_h1": "Have a project idea?",
        "contact_lead": "Tell me about your project: what you'd like to build or which problem you want to solve.",
        "direct_h": "Directly",
        "f_phone": "Phone (optional)",
        "next_h": "What happens next",
        "next": [
            ("You write", "You tell me briefly about your project or idea."),
            ("A short call", "In 20 minutes we pin down the need, the scope and whether I'm the right person for your project."),
            ("A clear plan and price", "Within 24 hours I send a work plan, timeline and a fixed price. We start only once everything is clear to both sides."),
        ],
    },
}

SERVICES = {
    "lt": [
        ("layers", "sand", "Nauja sistema nuo nulio", "Tinka, kai reikia ne puslapio, o veikiančio produkto.",
         "Padedu išgryninti sprendimą, suprojektuoju sąsają ir sukuriu sistemą nuo frontendo iki API ir duomenų bazės.",
         "Kai reikia ne dar vieno puslapio, o pilnai veikiančio produkto. Padedu išgryninti sprendimą, suprojektuoju vartotojo sąsają ir realizuoju sistemą nuo frontendo iki API bei duomenų.",
         ["React / TypeScript", "API ir backend", "Autentifikacija ir teisės", "Duomenų modelis", "Integracijos", "AI funkcijos"]),
        ("wrench", "rose", "Esamos sistemos gerinimas", "Tinka, kai sistema veikia, bet lėta ar sunkiai vystoma.",
         "Pirmiausia randu, kur problema, tada tvarkau tai, kas iš tikrųjų trukdo.",
         "Jei sistema jau veikia, bet yra lėta, sudėtinga, pilna pasikartojančio kodo ar sunkiai vystoma, pirmiausia išsiaiškinu, kur problema, o tada tvarkau tai, kas iš tikrųjų trukdo.",
         ["Našumo gerinimas", "Kodo refaktoringas", "Bug'ų paieška ir taisymas", "UX problemos", "API optimizavimas", "AI integracijos"]),
        ("plus", "lavender", "Naujos funkcijos esamai sistemai", "Tinka, kai produkto nereikia perrašyti.",
         "Perprantu esamą kodą ir kuriu naujas funkcijas, negriaudama to, kas jau veikia.",
         "Kai produkto nereikia perrašyti, reikia tiesiog gerai į jį įsilieti. Perprantu esamą architektūrą, prisitaikau prie projekto struktūros ir kuriu naujas funkcijas negriaudama to, kas jau veikia.",
         ["Nauji moduliai", "Frontend funkcijos", "Backend funkcijos", "Nauji API endpointai", "Integracijos", "AI agentai ir LLM"]),
    ],
    "en": [
        ("layers", "sand", "A new system from scratch", "When you need a working product, not a web page.",
         "I help pin down the solution, design the interface and build the system from frontend to API and database.",
         "When you need a fully working product, not another web page. I help pin down the solution, design the user interface and build the system from frontend to API and data.",
         ["React / TypeScript", "API and backend", "Authentication and permissions", "Data model", "Integrations", "AI features"]),
        ("wrench", "rose", "Improving an existing system", "When the system works but is slow or hard to develop further.",
         "First I find where the problem is, then I fix what actually gets in the way.",
         "If the system already works but is slow, complicated, full of repeated code or hard to develop further, I first find out where the problem is, then fix what actually gets in the way.",
         ["Performance", "Refactoring", "Finding and fixing bugs", "UX problems", "API optimisation", "AI integrations"]),
        ("plus", "lavender", "New features for an existing system", "When the product doesn't need a rewrite.",
         "I get to know the existing code and build new features without breaking what already works.",
         "When the product doesn't need a rewrite, new work just has to fit in well. I learn the existing architecture, adapt to the project's structure and build new features without breaking what already works.",
         ["New modules", "Frontend features", "Backend features", "New API endpoints", "Integrations", "AI agents and LLMs"]),
    ],
}


# --------------------------------------------------------------------------
# Shared chrome: header, footer, closing call to action
# --------------------------------------------------------------------------

def nav_href(key, lang):
    return url(key, lang)


def brand(lang):
    return (f'<a class="brand" href="{url("home", lang)}" aria-label="Gabrielė Tamaševičiūtė · Codeart, '
            f'{C[lang]["home"].lower()}">'
            '<span class="brand__mark" aria-hidden="true">GT</span>'
            '<span class="brand__text"><span class="brand__name">Gabrielė <span class="brand__surname">'
            'Tamaševičiūtė</span></span><span class="brand__co">Codeart</span></span></a>')


def site_header(lang, key, current=None):
    t, c = T[lang], C[lang]
    links = []
    menu = []
    for i, (k, label) in enumerate(c["nav"], 1):
        cur = ' aria-current="page"' if k == current else ""
        links.append(f'<a href="{nav_href(k, lang)}"{cur}>{label}</a>')
        menu.append(f'<a href="{nav_href(k, lang)}"{cur}><span class="mono" aria-hidden="true">0{i}</span>{label}</a>')
    return f"""<a class="skip-link" href="#main">{t["skip"]}</a>
<header class="site-header">
<div class="container site-header__in">
{brand(lang)}
<nav class="site-nav" aria-label="{t["nav_label"]}">
<div class="site-nav__links">
{chr(10).join(links)}
</div>
{lang_link(lang, key)}
<a class="btn" href="{url("contact", lang)}">{t["cta"]}</a>
</nav>
<button class="menu-toggle" type="button" data-menu-open aria-controls="mobile-menu" aria-expanded="false" aria-label="{t["menu_open"]}">{ICON_MENU}</button>
</div>
</header>
<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="{t["menu"]}" hidden>
<div class="mobile-menu__bar">
{brand(lang)}
<button class="menu-toggle" type="button" data-menu-close aria-label="{t["menu_close"]}">{ICON_CLOSE}</button>
</div>
<nav class="mobile-menu__nav" aria-label="{t["nav_label"]}">
{chr(10).join(menu)}
</nav>
<div class="mobile-menu__foot">
{lang_link(lang, key)}
<a class="btn" href="{url("contact", lang)}">{t["cta"]}</a>
</div>
</div>"""


def contact_form(lang, *, phone=False, cls="form"):
    t, c = T[lang], C[lang]
    phone_field = ""
    if phone:
        phone_field = f'<label class="field">{c["f_phone"]}<input type="tel" name="phone" autocomplete="tel"></label>'
    return f"""<form class="{cls}" data-contact action="{FORMSPREE}" method="POST" data-msg-sending="{esc(t["f_sending"])}" data-msg-ok="{esc(t["f_ok"])}" data-msg-fail="{esc(t["f_fail"])}" data-msg-invalid="{esc(t["f_invalid"])}">
<div class="form__row">
<label class="field">{t["f_name"]}<input type="text" name="name" autocomplete="name" required></label>
<label class="field">{t["f_email"]}<input type="email" name="email" autocomplete="email" required></label>
</div>
{phone_field}
<label class="field">{t["f_msg"]}<textarea name="message" rows="6" required></textarea></label>
<div class="form__hp" aria-hidden="true"><label>{t["f_hp"]}<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="_subject" value="{esc(t["f_subject"])}">
<div><button class="btn btn--lg" type="submit">{t["f_send"]}</button></div>
<p class="form__status" role="status" aria-live="polite"></p>
</form>"""


def contact_list(lang, keys=None, cls="contact-list"):
    items = []
    for ico, label, value, href in C[lang]["contact_items"]:
        if keys and ico not in keys:
            continue
        ext = ' target="_blank" rel="me noopener"' if href and href.startswith("http") else ""
        val = f'<a href="{href}"{ext}>{value}</a>' if href else f"<span>{value}</span>"
        items.append(f'<li><span class="contact-list__ico">{icon(ico)}</span>'
                     f'<span class="contact-list__body"><span class="contact-list__label">{label}</span>{val}</span></li>')
    return f'<ul class="{cls}">' + "".join(items) + "</ul>"


def socials(lang):
    out = []
    for ico, label, value, href in C[lang]["contact_items"]:
        if ico in ("github", "linkedin", "tiktok", "mail"):
            ext = ' target="_blank" rel="me noopener"' if href.startswith("http") else ""
            out.append(f'<a class="social" href="{href}"{ext} aria-label="{label}" title="{label}">{icon(ico)}</a>')
    return '<div class="socials">' + "".join(out) + "</div>"


def cta_band(lang):
    c = C[lang]
    return f"""<section class="cta-band" aria-labelledby="cta-title">
<div class="container cta-band__in" data-reveal>
<div class="cta-band__blob">{blob("b", "apricot")}</div>
<div class="cta-band__text">
<h2 class="h2" id="cta-title">{c["cta_h"]}</h2>
<p class="lead">{c["cta_p"]}</p>
</div>
<a class="btn btn--lg" href="{url("contact", lang)}">{c["cta_btn"]} {icon("arrow", 18)}</a>
</div>
</section>"""


def site_footer(lang, key):
    t, c = T[lang], C[lang]
    links = [f'<li><a href="{url("home", lang)}">{c["home"]}</a></li>'] + [
        f'<li><a href="{nav_href(k, lang)}">{label}</a></li>' for k, label in c["nav"]]
    return f"""<footer class="footer">
<div class="container footer__grid">
<div class="footer__brand">
{brand(lang)}
{socials(lang)}
</div>
<nav class="footer__links" aria-label="{c["links_h"]}">
<h2 class="footer__h">{c["links_h"]}</h2>
<ul>{"".join(links)}</ul>
</nav>
<div class="footer__contact">
<h2 class="footer__h">{c["direct_h"]}</h2>
{contact_list(lang, keys=("mail", "phone", "pin"), cls="contact-list contact-list--compact")}
</div>
</div>
<div class="container">
<div class="footer__bottom">
<span>© {YEAR} Gabrielė Tamaševičiūtė · Codeart. {c["rights"]}.</span>
<span class="footer__bottom-links"><a href="mailto:{EMAIL}">{EMAIL}</a>{lang_link(lang, key)}</span>
</div>
</div>
</footer>"""


def page_intro(eyebrow, h1, lead):
    return f"""<section class="page-intro">
<div class="container">
<p class="mono page-intro__eyebrow" data-reveal>{eyebrow}</p>
<h1 data-reveal class="d1">{h1}</h1>
<p class="lead page-intro__lead d2" data-reveal>{lead}</p>
</div>
</section>"""


def service_cards(lang, *, long=False):
    c = C[lang]
    cards = []
    for i, (ico, tone, h, fit, short, longtext, tags) in enumerate(SERVICES[lang]):
        tag_li = "".join(f"<li>{x}</li>" for x in tags)
        link = (f'<a class="link service-card__link" href="{url("contact", lang)}">{c["svc_cta"]}</a>'
                if long else "")
        cards.append(f"""<article class="service-card{(' d' + str(i)) if i else ''}" data-reveal>
{icon_blob(ico, tone)}
<h3>{h}</h3>
<p class="small service-card__fit">{fit}</p>
<p class="service-card__text">{longtext if long else short}</p>
<p class="label-mono service-card__inc">{c["includes"]}</p>
<ul class="tags service-card__tags">{tag_li}</ul>
{link}
</article>""")
    return '<div class="service-cards">' + "\n".join(cards) + "</div>"


def timeline(steps, *, cols=4):
    items = "\n".join(
        f"""<li class="tl__step{(' d' + str(i)) if i else ''}" data-reveal>
<span class="tl__num">{i + 1:02d}</span>
<h3>{h}</h3>
<p>{p}</p>
</li>""" for i, (h, p) in enumerate(steps))
    return f'<ol class="tl tl--{cols}">\n{items}\n</ol>'


def faq_block(lang, prefix="faq"):
    items = []
    for i, (q, a) in enumerate(T[lang]["faq"], 1):
        items.append(f"""<div class="faq__item">
<h3 class="faq__q"><button class="faq__btn" type="button" data-faq aria-expanded="true" aria-controls="{prefix}-{i}">{q}{ICON_PLUS}</button></h3>
<div class="faq__a" id="{prefix}-{i}"><p>{a}</p></div>
</div>""")
    return '<div class="faq">\n' + "\n".join(items) + "\n</div>"


def sec_head(num, title, hid, extra=""):
    return (f'<div class="sec-head{extra}" data-reveal><span class="mono" aria-hidden="true">{num} —</span>'
            f'<h2 class="h2" id="{hid}">{title}</h2></div>')


def assemble(lang, key, title, desc, body, *, jsonld=None, og_type="website", body_class="", current=None, cta=False):
    page = head(lang, key, title, desc, jsonld=jsonld, og_type=og_type)
    cls = f' class="{body_class}"' if body_class else ""
    page += f"<body{cls}>\n{site_header(lang, key, current)}\n<main id=\"main\">\n{body}\n</main>\n"
    if cta:
        page += cta_band(lang) + "\n"
    page += site_footer(lang, key) + "\n</body>\n</html>\n"
    write(ROUTES[key][lang], page)


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------

def home(lang):
    t, c = T[lang], C[lang]
    ids = t["ids"]

    hero = f"""<section class="hero" aria-labelledby="hero-title">
<div class="container grid hero__grid">
<div class="hero__copy">
<h1 class="hero__title" id="hero-title" data-reveal>{t["h1"]}</h1>
<p class="lead hero__lead d1" data-reveal>{t["lead"]}</p>
<div class="hero__ctas d2" data-reveal>
<a class="btn btn--lg" href="{url("contact", lang)}">{t["cta"]}</a>
<a class="link-underline" href="#{ids["work"]}">{t["see_work"]}</a>
</div>
<p class="small hero__note d3" data-reveal>{t["hero_note"]}</p>
</div>
<div class="hero__stage d1" data-reveal="far">
{blob("hero", "hero")}
<img class="hero__plant" src="/img/site/plant.webp" width="760" height="857" alt="" decoding="async">
<div class="laptop">
<div class="laptop__lid">{img("hero", t["hero_alt"], "(max-width: 759px) 92vw, 600px", lazy=False, priority=True)}</div>
<div class="laptop__base" aria-hidden="true"></div>
</div>
</div>
</div>
</section>"""

    rows = []
    for key, shape, tone, image, dark, title, desc, tags, alt in t["works"]:
        rows.append(f"""<article class="grid work work--{shape}">
<div class="work__text" data-reveal>
<h3 class="work__title"><a href="{url(key, lang)}">{title}</a></h3>
<p class="work__desc">{desc}</p>
<p class="mono work__tags">{tags}</p>
<a class="link" href="{url(key, lang)}" aria-label="{t["read_more"]}: {title}">{t["read_more"]} →</a>
</div>
<div class="work__media d1" data-reveal="far">
{blob(shape, tone)}
{framed(image, alt, "(max-width: 759px) 92vw, 680px", dark=dark)}
</div>
</article>""")
    works = f"""<section class="section section--raised" id="{ids["work"]}" aria-labelledby="work-title">
<div class="container">
{sec_head("01", t["work_h"], "work-title")}
{chr(10).join(rows)}
<div class="work-all"><a class="link" href="{url("portfolio", lang)}">{t["all_projects"]}</a></div>
</div>
</section>"""

    services = f"""<section class="section" id="{ids["services"]}" aria-labelledby="services-title">
<div class="container">
{sec_head("02", t["services_h"], "services-title")}
{service_cards(lang)}
<div class="work-all"><a class="link" href="{url("services", lang)}">{c["services_more"]}</a></div>
</div>
</section>"""

    steps = f"""<section class="section section--raised" aria-labelledby="steps-title">
<div class="container">
{sec_head("03", t["steps_h"], "steps-title")}
{timeline(t["steps"])}
<div class="tl-cta" data-reveal>
<p>{icon("clock")}{c["steps_cta_note"]}</p>
<a class="btn btn--lg" href="{url("contact", lang)}">{t["cta"]}</a>
</div>
</div>
</section>"""

    facts = "".join(f"<li>{icon('check', 18)}{f}</li>" for f in t["facts"])
    about = f"""<section class="section" id="{ids["about"]}" aria-labelledby="about-title">
<div class="container grid about">
<div class="about__media" data-reveal="far">
{blob("a", "apricot")}
{img("about", t["about_alt"], "(max-width: 759px) 88vw, 340px").replace("<img ", '<img class="organic" ')}
</div>
<div class="about__text d1" data-reveal>
{sec_head("04", t["about_h"], "about-title", " sec-head--tight")}
<p class="lead">{t["about_text"]}</p>
<ul class="facts">{facts}</ul>
<div class="about__links">
<a class="link" href="{url("about", lang)}">{t["about_more"]}</a>
<a class="link" href="{url("portfolio", lang)}">{c["about_cv"]} →</a>
</div>
</div>
</div>
</section>"""

    faq = f"""<section class="section section--raised" id="{ids["faq"]}" aria-labelledby="faq-title">
<div class="container grid">
<div class="faq-wrap" data-reveal>
{sec_head("05", t["faq_h"], "faq-title").replace(' data-reveal', '')}
{faq_block(lang)}
</div>
</div>
</section>"""

    contact = f"""<section class="section" id="{ids["contact"]}" aria-labelledby="contact-title">
<div class="container grid contact">
<div class="contact__text" data-reveal>
{sec_head("06", t["contact_h"], "contact-title", " sec-head--tight").replace(' data-reveal', '')}
<p class="lead">{t["contact_lead"]}</p>
{contact_list(lang, keys=("mail", "phone", "linkedin", "github"))}
</div>
<div class="contact__form d1" data-reveal>
{contact_form(lang)}
</div>
</div>
</section>"""

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Codeart — Gabrielė Tamaševičiūtė",
            "url": SITE + url("home", lang),
            "inLanguage": lang,
        },
        {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "@id": SITE + "/#business",
            "name": "Codeart — Gabrielė Tamaševičiūtė",
            "description": t["home_desc"],
            "url": SITE + url("home", lang),
            "image": SITE + "/img/og-cover.jpg",
            "email": EMAIL,
            "telephone": PHONE,
            "priceRange": "$$",
            "address": {"@type": "PostalAddress", "addressLocality": "Vilnius", "addressCountry": "LT"},
            "areaServed": [{"@type": "Country", "name": "Lietuva" if lang == "lt" else "Lithuania"}],
            "availableLanguage": ["lt", "en"],
            "founder": {"@id": SITE + "/#person"},
            "sameAs": [GITHUB, TIKTOK, LINKEDIN],
        },
        person_ld(lang),
    ]
    assemble(lang, "home", t["home_title"], t["home_desc"],
             "\n".join([hero, works, services, steps, about, faq, contact]), jsonld=jsonld)


# --------------------------------------------------------------------------
# Services, About and Contact pages
# --------------------------------------------------------------------------

def services_page(lang):
    t, c = T[lang], C[lang]
    price = "\n".join(f"""<article class="info-card{(' d' + str(i)) if i else ''}" data-reveal>
{icon_blob(ico, "sand" if i == 0 else "rose")}
<h3>{h}</h3>
<p>{p}</p>
</article>""" for i, (ico, h, p) in enumerate(c["price"]))
    expect = "".join(f"<li>{icon('check', 18)}{x}</li>" for x in c["expect"])
    body = f"""{page_intro(c["svc_eyebrow"], c["svc_h1"], c["svc_lead"])}
<section class="section section--raised" aria-labelledby="svc-list">
<div class="container">
{sec_head("01", c["svc_list_h"], "svc-list")}
{service_cards(lang, long=True)}
</div>
</section>
<section class="section" aria-labelledby="svc-steps">
<div class="container">
{sec_head("02", t["steps_h"], "svc-steps")}
{timeline(t["steps"])}
</div>
</section>
<section class="section section--raised" aria-labelledby="svc-price">
<div class="container">
{sec_head("03", c["price_h"], "svc-price")}
<div class="info-cards">
{price}
<article class="info-card info-card--list d2" data-reveal>
<h3>{c["expect_h"]}</h3>
<ul class="checklist">{expect}</ul>
</article>
</div>
</div>
</section>
<section class="section" aria-labelledby="svc-faq">
<div class="container grid">
<div class="faq-wrap" data-reveal>
<div class="sec-head"><span class="mono" aria-hidden="true">04 —</span><h2 class="h2" id="svc-faq">{t["faq_h"]}</h2></div>
{faq_block(lang)}
</div>
</div>
</section>"""
    assemble(lang, "services", c["svc_title"], c["svc_desc"], body, current="services", cta=True)


def about_page(lang):
    t, c = T[lang], C[lang]
    paras = "".join(f"<p>{p}</p>" for p in c["about_paras"])
    facts = "".join(f"<li>{icon('check', 18)}{f}</li>" for f in t["facts"])
    how = "\n".join(f"""<article class="principle{(' d' + str(i % 2)) if i % 2 else ''}" data-reveal>
{icon_blob(ico, ("sand", "rose", "lavender", "apricot")[i])}
<div><h3>{h}</h3><p>{p}</p></div>
</article>""" for i, (ico, h, p) in enumerate(c["how"]))
    values = "\n".join(f"""<li class="value{(' d' + str(i % 3)) if i % 3 else ''}" data-reveal>
<span class="value__ico">{icon(ico)}</span>
<div><h3>{h}</h3><p>{p}</p></div>
</li>""" for i, (ico, h, p) in enumerate(c["values"]))
    exp = "\n".join(f"""<li class="job" data-reveal>
<div class="job__when"><span class="mono">{when}</span></div>
<div class="job__body">
<h3>{role} <span class="job__org">· {org}</span></h3>
<p class="mono job__meta">{meta}</p>
{f'<p class="job__text">{text}</p>' if text else ''}
</div>
</li>""" for role, org, when, meta, text in c["exp"])
    uni, prog, years = c["edu"]
    langs = "".join(f"<li><span>{a}</span><span class=\"mono\">{b}</span></li>" for a, b in c["langs"])
    body = f"""<section class="page-intro page-intro--about">
<div class="container grid about">
<div class="about__media" data-reveal="far">
{blob("a", "apricot")}
{img("about", t["about_alt"], "(max-width: 759px) 88vw, 340px", lazy=False).replace("<img ", '<img class="organic" ')}
</div>
<div class="about__text d1" data-reveal>
<p class="mono page-intro__eyebrow">{c["about_eyebrow"]}</p>
<h1>{c["about_h1"]}</h1>
<div class="about__paras">{paras}</div>
<ul class="facts">{facts}</ul>
<div class="about__links">
<a class="btn btn--lg" href="{url("portfolio", lang)}">{c["about_cv"]}</a>
<a class="link" href="{pdf(lang)}">{icon("file", 18)} {c["about_pdf"]}</a>
</div>
</div>
</div>
</section>
<section class="section section--raised" aria-labelledby="how-title">
<div class="container">
{sec_head("01", c["how_h"], "how-title")}
<div class="principles">
{how}
</div>
</div>
</section>
<section class="section" aria-labelledby="values-title">
<div class="container">
{sec_head("02", c["values_h"], "values-title")}
<ul class="values">
{values}
</ul>
</div>
</section>
<section class="section section--raised" aria-labelledby="exp-title">
<div class="container">
{sec_head("03", c["exp_h"], "exp-title")}
<ol class="jobs">
{exp}
</ol>
<div class="edu" data-reveal>
<div class="edu__block">
<span class="edu__ico">{icon("cap")}</span>
<div><h3>{c["edu_h"]}</h3><p><strong>{uni}</strong> · {prog}</p><p class="mono">{years}</p></div>
</div>
<div class="edu__block">
<span class="edu__ico">{icon("globe")}</span>
<div><h3>{c["lang_h"]}</h3><ul class="langs">{langs}</ul></div>
</div>
</div>
</div>
</section>"""
    assemble(lang, "about", c["about_title"], c["about_desc"], body, current="about", cta=True,
             jsonld=[person_ld(lang)], og_type="profile")


def contact_page(lang):
    t, c = T[lang], C[lang]
    body = f"""{page_intro(c["contact_eyebrow"], c["contact_h1"], c["contact_lead"])}
<section class="section section--raised" aria-label="{c["contact_eyebrow"]}">
<div class="container grid contact contact--page">
<div class="contact__text" data-reveal>
<h2 class="contact__h">{c["direct_h"]}</h2>
{contact_list(lang)}
<div class="contact__meta">
<p>{icon("clock", 18)}{c["reply"]}</p>
</div>
</div>
<div class="contact__form d1" data-reveal>
{contact_form(lang, phone=True)}
</div>
</div>
</section>
<section class="section" aria-labelledby="next-title">
<div class="container">
{sec_head("01", c["next_h"], "next-title")}
{timeline(c["next"], cols=3)}
</div>
</section>"""
    assemble(lang, "contact", c["contact_title"], c["contact_desc"], body, current="contact")


def person_ld(lang):
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": SITE + "/#person",
        "name": "Gabrielė Tamaševičiūtė",
        "jobTitle": "Full-stack programuotoja" if lang == "lt" else "Full-stack developer",
        "url": SITE + url("portfolio", lang),
        "email": EMAIL,
        "knowsLanguage": ["lt", "en"],
        "address": {"@type": "PostalAddress", "addressLocality": "Vilnius", "addressCountry": "LT"},
        "sameAs": [GITHUB, LINKEDIN, TIKTOK],
        "knowsAbout": ["React", "TypeScript", "Next.js", "Web application development",
                       "Internal business systems", "API integration", "Supabase", ".NET"],
    }


# --------------------------------------------------------------------------
# /portfolio – CV summary for employers
# --------------------------------------------------------------------------

P = {
    "lt": {
        "title": "Gabrielė Tamaševičiūtė – CV ir portfolio | Full-stack programuotoja",
        "desc": "Full-stack programuotoja, daugiausia dirbanti su frontend: atrinkti darbai, patirtis, technologijos ir CV.",
        "eyebrow": "CV ir portfolio",
        "enlarge": "Padidinti nuotrauką",
        "close": "Uždaryti",
        "role": "Full-stack programuotoja, daugiausia dirbanti su frontend",
        "where": "Vilnius",
        "contacts_label": "Kontaktai",
        "cv_pdf": "CV (PDF)",
        "cv_dl": "Atsisiųsti CV (PDF)",
        "facts_label": "Trumpai",
        "facts": [("Dabar", "Programuotoja (Mid), UVS"), ("Patirtis", "3+ m. profesionaliai"),
                  ("Fokusas", "Vidinės verslo sistemos"), ("Stackas", "React, TypeScript, Next.js")],
        "works_h": "Atrinkti darbai",
        "what": "Kas tai:", "role_l": "Rolė:", "fact": "Faktas:",
        "tags_label": "Technologijos",
        "read_more": "Skaityti plačiau",
        "cards": [
            ("p_lang", "a", "rose", "kalbos", "Kalbų mokymosi platforma",
             "kalbų mokymosi platforma su turinio valdymo sistema", "viena, visa sistema",
             "9 užduočių tipai iš vieno žodyno · 433 testai",
             ["Next.js", "TypeScript", "Supabase", "PostgreSQL"],
             "Kalbų platformos mokinio pradžios ekranas su kurso žemėlapiu"),
            ("p_tik", "b", "lavender", "tik", "TikMaker",
             "vaizdo redaktorius ir dizaino sistema TikTok / Reels įrašams", "viena, visas įrankis",
             "laiko juosta su keyframe'ais · AI balsas su žodžių subtitrais",
             ["React", "TypeScript", "Remotion", "tRPC", "ElevenLabs"],
             "TikMaker redaktorius su laiko juosta"),
            ("p_loy", "c", "sand", "loy_cards", "Lojalumo valdymo sistema",
             "B2B administravimo sistema lojalumo programoms", "pagrindinė frontend programuotoja komandoje",
             "komandinis projektas · ~730 frontend testų",
             ["React", "TypeScript", "RTK Query", ".NET", "SQL Server"],
             "Lojalumo sistema: kortelių sąrašas, duomenys uždengti"),
        ],
        "others_h": "Kiti darbai",
        "others": [
            ("Kidcan", "Tėvų ir vaikų aplikacijų pora vaiko vietai matyti realiu laiku",
             "React Native · Expo · Kotlin · Supabase", "2025",
             [("Parents", "https://github.com/gabwowce/KidcanParentsExpo"), ("Kids", "https://github.com/gabwowce/KidcanKids")]),
            ("Kibinai Vilnius", "Restorano svetainė, kurios turinį verslas redaguoja pats",
             "React · WordPress (headless)", "2025",
             [("Live", "https://kibinaivilnius.lt/"), ("GitHub", "https://github.com/gabwowce/Kibinukai")]),
            ("AutoRent", "Automobilių nuomos platforma su pilnu rezervacijos srautu",
             "React · FastAPI · PostgreSQL", "2025",
             [("Live", "https://car-rental-frontend-v2.vercel.app/"), ("GitHub", "https://github.com/gabwowce/car-rental-frontend")]),
            ("LTSA", "Viktorina, kurios atsakymai patys suvedami į Google Sheets",
             "HTML · CSS · JS", "2026", [("Live", "https://ltsa.vercel.app/")]),
            ("Travel App", "Kelionių planavimo aplikacijos pagrindas Android ir iOS",
             "React Native · Expo", "2025", [("GitHub", "https://github.com/gabwowce/travel-app-front")]),
            ("ConvertClimb", "Laipiojimo sudėtingumo laipsnių konverteris, veikia be interneto",
             "React Native · Expo", "2025", [("GitHub", "https://github.com/gabwowce/ConvertClimb")]),
        ],
        "exp_h": "Patirtis",
        "exp": [
            ("2026 kov. – dabar", "Programuotoja (Mid), UVS", "Vidinė verslo sistema nuo nulio, vienintelė frontend programuotoja", False),
            ("2025 kov. – dabar", "Laisvai samdoma programuotoja", "Web ir mobile aplikacijos nuo idėjos iki paleidimo", False),
            ("2024 birž. – 2026 vas.", "Jaunesnioji programuotoja, UVS", "C#/.NET, WPF sistemos ekranai ir funkcionalumas", False),
            ("2021–2023", "Ankstesnė patirtis", "Planuotoja (Girteka), administratorė (Jarinta)", True),
        ],
        "tech_h": "Technologijos",
        "tech": [
            ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "HTML / CSS", "Tailwind CSS", "shadcn/ui",
                          "Redux Toolkit / RTK Query", "TanStack Query", "Zustand", "React Hook Form + Zod",
                          "AG Grid", "Recharts / ECharts", "Remotion"]),
            ("Backend ir API", ["C# / .NET (ASP.NET Core)", "Entity Framework Core", "Node.js", "Express", "tRPC",
                                "REST API / OpenAPI", "Next.js Server Actions", "FastAPI"]),
            ("Duomenų bazės", ["SQL", "PostgreSQL", "SQL Server", "Supabase (Auth, Storage, RLS)"]),
            ("Mobile ir desktop", ["React Native", "Expo", "Kotlin", "WPF (XAML)"]),
            ("Testavimas ir kokybė", ["Vitest", "Playwright", "Testing Library", "MSW", "xUnit", "ESLint", "Prettier"]),
            ("AI", ["LLM integracijos", "AI agentai", "ElevenLabs API"]),
            ("Įrankiai ir dizainas", ["Git / GitHub", "Vite", "Vercel", "Stripe", "WordPress (headless)", "Figma"]),
        ],
        "tech_cv": [
            ("Frontend", ["React", "TypeScript", "Next.js", "Tailwind CSS", "RTK Query", "TanStack Query", "Zustand", "AG Grid"]),
            ("Backend ir API", ["C# / .NET", "Node.js", "Express", "tRPC", "REST API / OpenAPI"]),
            ("Duomenų bazės", ["SQL", "PostgreSQL", "SQL Server", "Supabase", "EF Core"]),
            ("Mobile ir desktop", ["React Native", "Expo", "WPF"]),
            ("Testavimas", ["Vitest", "Playwright", "Testing Library", "xUnit"]),
            ("AI ir įrankiai", ["LLM integracijos", "AI agentai", "Git", "Figma", "Vercel"]),
        ],
        "edu_l": "Išsilavinimas",
        "edu": "Vilniaus kolegija, Programų sistemos, 2023–2027 (studijuoju)",
        "more": "Daugiau darbų (Kidcan, Kibinai Vilnius, AutoRent ir kt.) ir išsamūs aprašymai: codeart.lt/portfolio",
        "sheet_title": "Gabrielė Tamaševičiūtė – CV",
        "sheet_foot": "Gabrielė Tamaševičiūtė · CV",
    },
    "en": {
        "title": "Gabrielė Tamaševičiūtė – CV and portfolio | Full-stack developer",
        "desc": "Full-stack developer with a frontend focus: selected work, experience, technologies and CV.",
        "eyebrow": "CV and portfolio",
        "enlarge": "Enlarge image",
        "close": "Close",
        "role": "Full-stack developer with a frontend focus",
        "where": "Vilnius",
        "contacts_label": "Contacts",
        "cv_pdf": "CV (PDF)",
        "cv_dl": "Download CV (PDF)",
        "facts_label": "In short",
        "facts": [("Now", "Developer (Mid), UVS"), ("Experience", "3+ years professionally"),
                  ("Focus", "Internal business systems"), ("Stack", "React, TypeScript, Next.js")],
        "works_h": "Selected work",
        "what": "What:", "role_l": "Role:", "fact": "Fact:",
        "tags_label": "Technologies",
        "read_more": "Read more",
        "cards": [
            ("p_lang", "a", "rose", "kalbos", "Language learning platform",
             "language learning platform with a content management system", "solo, the whole system",
             "9 exercise types from one vocabulary · 433 tests",
             ["Next.js", "TypeScript", "Supabase", "PostgreSQL"],
             "The learner home screen of the language platform with the course map"),
            ("p_tik", "b", "lavender", "tik", "TikMaker",
             "video editor and design system for TikTok / Reels videos", "solo, the whole tool",
             "timeline with keyframes · AI voice with word-level subtitles",
             ["React", "TypeScript", "Remotion", "tRPC", "ElevenLabs"],
             "The TikMaker editor with its timeline"),
            ("p_loy", "c", "sand", "loy_cards", "Loyalty management system",
             "B2B admin system for loyalty programmes", "lead frontend developer in a team",
             "team project · ~730 frontend tests",
             ["React", "TypeScript", "RTK Query", ".NET", "SQL Server"],
             "Loyalty system: the card list, data masked"),
        ],
        "others_h": "Other work",
        "others": [
            ("Kidcan", "A pair of parent and child apps for seeing a child's location in real time",
             "React Native · Expo · Kotlin · Supabase", "2025",
             [("Parents", "https://github.com/gabwowce/KidcanParentsExpo"), ("Kids", "https://github.com/gabwowce/KidcanKids")]),
            ("Kibinai Vilnius", "A restaurant website whose content the business edits itself",
             "React · WordPress (headless)", "2025",
             [("Live", "https://kibinaivilnius.lt/"), ("GitHub", "https://github.com/gabwowce/Kibinukai")]),
            ("AutoRent", "A car rental platform with a full booking flow",
             "React · FastAPI · PostgreSQL", "2025",
             [("Live", "https://car-rental-frontend-v2.vercel.app/"), ("GitHub", "https://github.com/gabwowce/car-rental-frontend")]),
            ("LTSA", "A quiz whose answers go straight into Google Sheets",
             "HTML · CSS · JS", "2026", [("Live", "https://ltsa.vercel.app/")]),
            ("Travel App", "The foundation of a trip planning app for Android and iOS",
             "React Native · Expo", "2025", [("GitHub", "https://github.com/gabwowce/travel-app-front")]),
            ("ConvertClimb", "A climbing grade converter that works offline",
             "React Native · Expo", "2025", [("GitHub", "https://github.com/gabwowce/ConvertClimb")]),
        ],
        "exp_h": "Experience",
        "exp": [
            ("Mar 2026 – present", "Developer (Mid), UVS", "Internal business system from scratch, the only frontend developer", False),
            ("Mar 2025 – present", "Freelance developer", "Web and mobile apps from idea to launch", False),
            ("Jun 2024 – Feb 2026", "Junior developer, UVS", "C#/.NET, WPF system screens and features", False),
            ("2021–2023", "Earlier experience", "Planner (Girteka), administrator (Jarinta)", True),
        ],
        "tech_h": "Technologies",
        "tech": [
            ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "HTML / CSS", "Tailwind CSS", "shadcn/ui",
                          "Redux Toolkit / RTK Query", "TanStack Query", "Zustand", "React Hook Form + Zod",
                          "AG Grid", "Recharts / ECharts", "Remotion"]),
            ("Backend and APIs", ["C# / .NET (ASP.NET Core)", "Entity Framework Core", "Node.js", "Express", "tRPC",
                                  "REST API / OpenAPI", "Next.js Server Actions", "FastAPI"]),
            ("Databases", ["SQL", "PostgreSQL", "SQL Server", "Supabase (Auth, Storage, RLS)"]),
            ("Mobile and desktop", ["React Native", "Expo", "Kotlin", "WPF (XAML)"]),
            ("Testing and quality", ["Vitest", "Playwright", "Testing Library", "MSW", "xUnit", "ESLint", "Prettier"]),
            ("AI", ["LLM integrations", "AI agents", "ElevenLabs API"]),
            ("Tools and design", ["Git / GitHub", "Vite", "Vercel", "Stripe", "WordPress (headless)", "Figma"]),
        ],
        "tech_cv": [
            ("Frontend", ["React", "TypeScript", "Next.js", "Tailwind CSS", "RTK Query", "TanStack Query", "Zustand", "AG Grid"]),
            ("Backend and APIs", ["C# / .NET", "Node.js", "Express", "tRPC", "REST API / OpenAPI"]),
            ("Databases", ["SQL", "PostgreSQL", "SQL Server", "Supabase", "EF Core"]),
            ("Mobile and desktop", ["React Native", "Expo", "WPF"]),
            ("Testing", ["Vitest", "Playwright", "Testing Library", "xUnit"]),
            ("AI and tools", ["LLM integrations", "AI agents", "Git", "Figma", "Vercel"]),
        ],
        "edu_l": "Education",
        "edu": "Vilnius University of Applied Sciences (Vilniaus kolegija), Software Systems, 2023–2027 (in progress)",
        "more": "More work (Kidcan, Kibinai Vilnius, AutoRent and others) and full write-ups: codeart.lt/en/portfolio.html",
        "sheet_title": "Gabrielė Tamaševičiūtė – CV",
        "sheet_foot": "Gabrielė Tamaševičiūtė · CV",
    },
}


# Screenshot files for "Other work": name -> (file stem, large w, h, thumb w, h)
OTHER_SHOTS = {
    "Kidcan": ("kidcan", 1538, 1045, 240, 163),
    "Kibinai Vilnius": ("kibinai", 1600, 1002, 240, 150),
    "AutoRent": ("autorent", 1600, 1227, 240, 184),
    "LTSA": ("ltsa", 1177, 839, 240, 171),
    "Travel App": ("travel", 1600, 954, 240, 143),
    "ConvertClimb": ("convertclimb", 1600, 954, 240, 143),
}


def portfolio(lang):
    p = P[lang]
    facts = "\n".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["facts"])

    cards = []
    for key, shape, tone, image, title, what, role, fact, tags, alt in p["cards"]:
        tag_li = "".join(f"<li>{x}</li>" for x in tags)
        cards.append(f"""<article class="card card--{shape}">
<div class="card__media">
{blob(shape, tone)}
{framed(image, alt, "(max-width: 759px) 88vw, 380px", dark=(image == "tik"))}
</div>
<h3>{title}</h3>
<dl class="card__facts">
<div><dt>{p["what"]}</dt><dd>{what}</dd></div>
<div><dt>{p["role_l"]}</dt><dd>{role}</dd></div>
<div><dt>{p["fact"]}</dt><dd>{fact}</dd></div>
</dl>
<ul class="tags" aria-label="{p["tags_label"]}">{tag_li}</ul>
<div class="card__links"><a class="link" href="{url(key, lang)}" aria-label="{p["read_more"]}: {title}">{p["read_more"]} →</a></div>
</article>""")

    others = []
    for name, desc, stack, _year, links in p["others"]:
        ls = "".join(f'<a class="link" href="{u}" target="_blank" rel="noopener" aria-label="{name}: {label}">{label} ↗</a>'
                     for label, u in links)
        shot, w, h, tw, th = OTHER_SHOTS[name]
        thumb = (f'<button class="r-thumb" type="button" data-lightbox="/img/site/others/{shot}.webp" '
                 f'data-caption="{esc(name + " – " + desc)}">'
                 f'<img src="/img/site/others/{shot}-thumb.webp" width="{tw}" height="{th}" alt="" loading="lazy" decoding="async">'
                 f'<span class="visually-hidden">{p["enlarge"]}: {name}</span></button>')
        others.append(f"""<li>{thumb}<span class="r-name">{name}</span><span class="r-desc">{desc}</span><span class="r-stack">{stack}</span><span class="r-links">{ls}</span></li>""")

    exp = "\n".join(
        f'<li{" class=\"is-past\"" if past else ""}><span class="t-date">{d}</span><span class="t-role">{r}</span><span class="t-what">{w}</span></li>'
        for d, r, w, past in p["exp"])

    tech = "\n".join(
        f'<div><dt>{g}</dt><dd>{"".join(f"<span class=\"tag\">{x}</span>" for x in items)}</dd></div>'
        for g, items in p["tech"])

    body = f"""<section class="cv-head">
<div class="container">
<div class="cv-head__row">
<div class="cv-head__id">
<div class="cv-head__photo">
{blob("a", "apricot")}
{img("about", "Gabrielė Tamaševičiūtė", "150px", lazy=False).replace("<img ", '<img class="organic" ')}
</div>
<div>
<p class="mono page-intro__eyebrow">{p["eyebrow"]}</p>
<h1>Gabrielė Tamaševičiūtė</h1>
<p class="cv-head__role">{p["role"]}</p>
<p class="cv-head__where">{p["where"]}</p>
<nav class="cv-head__links" aria-label="{p["contacts_label"]}">
<a href="{pdf(lang)}">{icon("file", 18)}{p["cv_pdf"]}</a>
<a href="{GITHUB}" target="_blank" rel="me noopener">{icon("github", 18)}GitHub</a>
<a href="{LINKEDIN}" target="_blank" rel="me noopener">{icon("linkedin", 18)}LinkedIn</a>
<a href="mailto:{EMAIL}">{icon("mail", 18)}{EMAIL}</a>
</nav>
</div>
</div>
<a class="btn btn--lg" href="{pdf(lang)}">{icon("file", 18)} {p["cv_dl"]}</a>
</div>
</div>
</section>
<div class="container">
<section class="cv-facts" aria-label="{p["facts_label"]}">
<dl>
{facts}
</dl>
</section>
<section class="cv-sec cv-sec--works" aria-labelledby="works-title">
<div class="cv-sec__head"><span class="mono" aria-hidden="true">01 —</span><h2 id="works-title">{p["works_h"]}</h2></div>
<div class="cards">
{chr(10).join(cards)}
</div>
<div class="others">
<h3>{p["others_h"]}</h3>
<ul class="rows">
{chr(10).join(others)}
</ul>
</div>
</section>
<section class="cv-sec" aria-labelledby="exp-title">
<div class="cv-sec__head"><span class="mono" aria-hidden="true">02 —</span><h2 id="exp-title">{p["exp_h"]}</h2></div>
<ol class="timeline">
{exp}
</ol>
</section>
<section class="cv-sec" aria-labelledby="tech-title">
<div class="cv-sec__head"><span class="mono" aria-hidden="true">03 —</span><h2 id="tech-title">{p["tech_h"]}</h2></div>
<dl class="stack-list">
{tech}
</dl>
</section>
<section class="cv-sec cv-edu" aria-labelledby="edu-title">
<div class="cv-sec__head"><span class="mono" aria-hidden="true">04 —</span><h2 id="edu-title">{p["edu_l"]}</h2></div>
<p class="cv-edu__line">{icon("cap")}<span>{p["edu"]}</span></p>
</section>
</div>
<dialog class="lightbox" id="lightbox" aria-label="{p["enlarge"]}">
<button class="lightbox__close" type="button" data-lightbox-close aria-label="{p["close"]}">{ICON_CLOSE}</button>
<figure><img src="" alt=""><figcaption></figcaption></figure>
</dialog>"""
    assemble(lang, "portfolio", p["title"], p["desc"], body, jsonld=[person_ld(lang)],
             og_type="profile", body_class="page-cv", current="portfolio")


# --------------------------------------------------------------------------
# The A4 CV sheet (printed to /<lang>/cv.pdf)
# --------------------------------------------------------------------------

def cv_sheet(lang):
    p = P[lang]
    facts = "\n".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["facts"])
    works = []
    for key, shape, tone, image, title, what, role, fact, tags, alt in p["cards"]:
        sentence = what[0].upper() + what[1:] + "."
        works.append(f"""<article>
<h3>{title}</h3>
<p>{sentence}</p>
<p class="gap"><span class="lbl">{p["role_l"]}</span> {role}</p>
<p><span class="lbl">{p["fact"]}</span> {fact}</p>
<p class="gap m">{" · ".join(tags)}</p>
</article>""")
    rows = "\n".join(
        f'<tr{" class=\"is-past\"" if past else ""}><td class="d">{d}</td><td class="r">{r}</td><td>{w}</td></tr>'
        for d, r, w, past in p["exp"])
    tech = "\n".join(f"<div><dt>{g}</dt><dd>{' · '.join(items)}</dd></div>" for g, items in p["tech_cv"])
    # LT has a short address of its own: /portfolio redirects to the LT page.
    site_cv = "codeart.lt/portfolio" if lang == "lt" else "codeart.lt" + url("portfolio", lang)

    body = f"""<body class="page-sheet">
<main class="sheet">
<header class="sheet__head">
<div>
<h1>Gabrielė Tamaševičiūtė</h1>
<p class="sheet__role">{p["role"]}</p>
<p class="sheet__where">{todo(p["where"])}</p>
</div>
<div class="sheet__contacts">
<div><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<div><a href="{GITHUB}">github.com/gabwowce</a></div>
<div><a href="{SITE + url("portfolio", lang)}">{site_cv}</a></div>
<div><a href="{LINKEDIN}">LinkedIn</a></div>
</div>
</header>
<dl class="sheet__facts">
{facts}
</dl>
<section>
<h2><span class="m">01 — </span>{p["works_h"]}</h2>
<div class="sheet__works">
{chr(10).join(works)}
</div>
<p class="sheet__more">{p["more"]}</p>
</section>
<section>
<h2><span class="m">02 — </span>{p["exp_h"]}</h2>
<table><tbody>
{rows}
</tbody></table>
</section>
<section>
<h2><span class="m">03 — </span>{p["tech_h"]}</h2>
<dl class="sheet__stack">
{tech}
</dl>
</section>
<section class="sheet__edu">
<p><strong>{p["edu_l"]}</strong> · {p["edu"]}</p>
</section>
<footer class="sheet__foot"><span>{p["sheet_foot"]}</span><span>{site_cv}</span></footer>
</main>
</body>
</html>
"""
    page = head(lang, "cv", p["sheet_title"], p["desc"], noindex=True)
    write(ROUTES["cv"][lang], page + body)


# --------------------------------------------------------------------------
# Project pages
# --------------------------------------------------------------------------

PROJECTS = {
    "p_lang": {
        "next": "p_tik",
        "tone": "rose",
        "lt": {
            "title": "Kalbų mokymosi platforma", "meta": "web platforma · klientinis projektas · 2026",
            "what": "Internetinė kalbų mokymosi sistema iš trijų dalių: vieša mokymų svetainė, mokinio mokymosi platforma ir turinio valdymo sistema. Kursus administratorius kuria pats, be programuotojo: sistema iš įvesto žodyno sudaro interaktyvias užduotis, valdo prieigą prie kursų per aktyvavimo kodus, seka mokinių progresą ir baigus lygį išduoda sertifikatą.",
            "status": "Aktyviai vystoma.",
            "features": [
                ("b", ("kalbos_admin", "Turinio valdymas: kairėje turinio medis, dešinėje pamokos užduočių sąrašas"),
                 "Užduotys iš žodyno automatiškai",
                 "Administratorius žodį įveda vieną kartą, o sistema iš jo pati sudaro iki aštuonių tipų užduočių.",
                 ["Užduočių tipai: kortelė, žodis su sakiniu, klausyk ir pasirink, porų sujungimas, praleistas žodis, sakinio dėliojimas, vertimas abiem kryptimis, paveikslėlio parinkimas ir rankinis klausimas.",
                  "Prieš kuriant matosi, kiek užduočių atsiras ir kurioms trūksta duomenų (pvz. garso).",
                  "Klaidingi atsakymų variantai parenkami iš tos pačios temos žodžių.",
                  "Pakartotinai sudėliojus užduotys nesidubliuoja, o rankinės išlieka.",
                  "„Išmaišyti“ sumaišo užduotis taip, kad žodžio kortelė visada eitų prieš to žodžio tikrinimą."]),
                ("c", ("kalbos_task", "Vykstanti pamoka: progreso juosta ir sakinio dėliojimo užduotis"),
                 "Mokymosi kelias mokiniui",
                 "Mokinys eina aiškiu keliu: pamokos, testai, kartojimas ir sertifikatas. Progresas saugomas serveryje ir nedingsta pakeitus įrenginį.",
                 ["Atsakymas patikrinamas iš karto; raidžių dydis ir skyryba nesvarbūs, o praleistos lietuviškos raidės ar viena rašybos klaida įskaitomos su pastaba.",
                  "Temos ir testai atsirakina nuosekliai, pagal progresą.",
                  "Testai vertinami serveryje pagal praėjimo ribą.",
                  "Žodžiai kartojami intervalais 1 → 3 → 7 → 21 diena.",
                  "Baigus lygį išduodamas PDF sertifikatas su unikaliu numeriu."]),
                ("a", ("kalbos_import", "Turinio valdymas: turinio medis ir mygtukas „Importuoti iš Excel“"),
                 "Visas kursas iš vieno Excel failo",
                 "Visą kursą galima įkelti vienu Excel failu, o sistema prieš įrašydama parodo, kas bus sukurta.",
                 ["Tuščias ir pavyzdinis šablonas atsisiunčiami iš sistemos.",
                  "Prieš importą tikrinami stulpeliai, ieškoma dublikatų ir parodoma, kur turinys bus įdėtas.",
                  "Trūkstamas garsas ar paveikslėlis susiejamas automatiškai, kai vėliau įkeliamas tokiu pačiu pavadinimu.",
                  "Importuotos pamokos gali būti iškart paskelbtos."]),
            ],
            "role": "Viena kūriau visą sistemą: duomenų bazę, serverio logiką, mokinio platformą, turinio valdymą ir testus.",
            "decisions": [
                ("Užduočių variklis iš grynų funkcijų:", "kiekvienas užduoties tipas yra viena taisyklė registre, todėl naujas tipas nereikalauja keisti variklio. Atsitiktinumas perduodamas kaip parametras, todėl logika testuojama deterministiškai. Tas pats variklis veikia pamokose, testuose ir kartojime."),
                ("Saugumas trijuose sluoksniuose:", "sąsajoje, serverio veiksmuose ir duomenų bazėje (Row Level Security kiekvienai lentelei). RLS taisyklės patikrintos atskirais integraciniais testais, nes sąsajos apsaugą galima apeiti kreipiantis tiesiai į API."),
                ("Atomiški veiksmai duomenų bazėje:", "kodo aktyvavimas ir kitos kelių žingsnių operacijos vyksta vienoje transakcijoje su eilutės užraktu, todėl tą patį kodą aktyvuoti gali tik vienas žmogus."),
                ("Griežtas duomenų sluoksnis:", "komponentas → hook'as → servisas → duomenų bazė. Kai du administratoriai redaguoja tą patį įrašą, konfliktas aptinkamas ir svetimi pakeitimai tyliai neperrašomi."),
                ("Kokybės automatika:", "patikros prieš kiekvieną commit'ą, ESLint taisyklė, saugojanti dizaino sistemą, kontaktų formos apsauga nuo šlamšto, o IP saugomas tik kaip maiša ir ištrinamas po paros."),
            ],
            "scale": "33 ekranai · 25 DB lentelės ir 64 RLS taisyklės · 9 užduočių tipai · 433 testai (iš jų 110 RLS ir 16 E2E) · 2105 vertimo raktai",
            "stack": "Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form + Zod, next-intl · Supabase (PostgreSQL, RLS, Auth, Storage), pg_cron · @react-pdf/renderer, xlsx · Vitest, Playwright",
            "desc": "Kalbų mokymosi platforma: vieša svetainė, mokinio platforma ir turinio valdymo sistema, kurioje užduotys sudaromos automatiškai iš žodyno. Next.js ir Supabase.",
        },
        "en": {
            "title": "Language learning platform", "meta": "web platform · client project · 2026",
            "what": "An online language learning system in three parts: a public course website, a learner platform and a content management system. The admin builds courses on their own, without a developer: the system turns the entered vocabulary into interactive exercises, manages course access through activation codes, tracks learner progress and issues a certificate when a level is completed.",
            "status": "Actively developed.",
            "features": [
                ("b", ("kalbos_admin", "Content management: the content tree on the left, the lesson's exercise list on the right"),
                 "Exercises generated from the vocabulary",
                 "The admin enters a word once, and the system builds up to eight types of exercises from it.",
                 ["Exercise types: flashcard, word in a sentence, listen and choose, match the pairs, missing word, sentence building, translation in both directions, picture choice and a manual question.",
                  "Before generating, you see how many exercises will be created and which are missing data (e.g. audio).",
                  "Wrong answer options are picked from words of the same topic.",
                  "Regenerating doesn't duplicate exercises, and manual ones are kept.",
                  "“Shuffle” mixes the exercises so a word's flashcard always comes before that word is tested."]),
                ("c", ("kalbos_task", "A lesson in progress: the progress bar and a sentence-building exercise"),
                 "A learning path for the learner",
                 "The learner follows a clear path: lessons, tests, review and a certificate. Progress is stored on the server and isn't lost when switching devices.",
                 ["Answers are checked instantly; letter case and punctuation don't matter, and missing Lithuanian diacritics or a single typo are accepted with a note.",
                  "Topics and tests unlock in order, based on progress.",
                  "Tests are graded on the server against a pass mark.",
                  "Words are reviewed at intervals of 1 → 3 → 7 → 21 days.",
                  "Completing a level issues a PDF certificate with a unique number."]),
                ("a", ("kalbos_import", "Content management: the content tree and the “Import from Excel” button"),
                 "A whole course from one Excel file",
                 "A whole course can be uploaded as a single Excel file, and before saving the system shows what will be created.",
                 ["A blank and a sample template can be downloaded from the system.",
                  "Before import, columns are checked, duplicates are found and the target location is shown.",
                  "Missing audio or images are linked automatically when uploaded later under the same name.",
                  "Imported lessons can be published right away."]),
            ],
            "role": "I built the whole system on my own: the database, server logic, learner platform, content management and tests.",
            "decisions": [
                ("Exercise engine built from pure functions:", "each exercise type is a single rule in a registry, so a new type doesn't require changing the engine. Randomness is passed in as a parameter, so the logic is tested deterministically. The same engine powers lessons, tests and review."),
                ("Security in three layers:", "in the interface, in server actions and in the database (Row Level Security on every table). RLS policies are covered by separate integration tests, because interface protection can be bypassed by calling the API directly."),
                ("Atomic operations in the database:", "activating a code and other multi-step operations run in a single transaction with a row lock, so the same code can only be redeemed by one person."),
                ("Strict data layer:", "component → hook → service → database. When two admins edit the same record, the conflict is detected and other people's changes are never silently overwritten."),
                ("Quality automation:", "checks before every commit, an ESLint rule that guards the design system, spam protection on the contact form, and IPs stored only as a hash and deleted after a day."),
            ],
            "scale": "33 screens · 25 DB tables and 64 RLS policies · 9 exercise types · 433 tests (110 RLS and 16 E2E among them) · 2105 translation keys",
            "stack": "Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form + Zod, next-intl · Supabase (PostgreSQL, RLS, Auth, Storage), pg_cron · @react-pdf/renderer, xlsx · Vitest, Playwright",
            "desc": "A language learning platform: a public website, a learner platform and a content management system that generates exercises from the vocabulary. Next.js and Supabase.",
        },
    },
    "p_tik": {
        "next": "p_loy",
        "tone": "lavender",
        "lt": {
            "title": "TikMaker", "meta": "vaizdo redaktorius · asmeninis projektas · 2026",
            "what": "Vaizdo įrašų redaktorius ir dizaino sistema trumpiems vertikaliems (9:16) TikTok, Reels ir Shorts įrašams. Video nebereikia montuoti rankomis: jis surenkamas iš paruoštų scenų, vizualų ir animacijų, todėl kiekvienas įrašas atrodo vientisai, o pagaminamas greičiau.",
            "status": "Darbo įrankis, kurį naudoju savo turiniui.",
            "features": [
                ("b", ("tik", "TikMaker redaktorius: scenų sąrašas, peržiūra, nustatymai ir laiko juosta su keliomis eilėmis"),
                 "Laiko juosta kaip montavimo programoje",
                 "Profesionalios montavimo programos patirtis, pritaikyta šiai sistemai: kiekvieną elementą galima tiksliai sudėlioti laike be papildomų programų.",
                 ["Klipai tempiami laike ir tarp eilučių, prisitraukia prie scenos kraštų, žymeklio ir kitų klipų.",
                  "Keyframe'ai poziciją ir mastelį keičia laike, juos galima tempti.",
                  "Kopijuoti, įklijuoti, dubliuoti (Ctrl+C / V / D), pakeisti elemento failą išlaikant animacijas.",
                  "Garso bangų formos laiko juostoje.",
                  "Bet kurį veiksmą galima atšaukti ir pakartoti."]),
                ("c", ("tik_library", "TikMaker: elementų biblioteka ir vertikalaus video peržiūra su scena"),
                 "Dizaino sistema, kuri neleidžia suklysti",
                 "Video ne piešiamas nuo nulio, o surenkamas iš patikrintų dalių. Tekstas neišlenda už kadro, scenos nenukerpamos per anksti, o stilius visada vienodas.",
                 ["7 scenų tipai, 25 vizualų tipai (terminalas, kodo pakeitimai, naršyklės ir telefono maketai, diagramos, statistika) ir 7 fonai.",
                  "Scenos trukmė apskaičiuojama automatiškai iš balso teksto ir ekrane rodomo teksto skaitymo laiko.",
                  "Išdėstymo šablonai vizualą pritaiko saugiai zonai, kurios neuždengia TikTok sąsaja.",
                  "Elementas gali sklandžiai „keliauti“ iš scenos į sceną.",
                  "Redaktorius įspėja apie per trumpą sceną, perpildytą kadrą ar per ilgas kodo eilutes."]),
                ("a", ("tik_voice", "TikMaker: peržiūra, „Render MP4“ mygtukas ir scenos įgarsinimo tekstas inspektoriuje"),
                 "Iš teksto į balsą, subtitrus ir MP4",
                 "Iš parašyto teksto sistema pati sukuria įgarsinimą ir TikTok stiliaus subtitrus, o galutinį video atvaizduoja vienu mygtuku.",
                 ["Įgarsinimas generuojamas su ElevenLabs, balso nustatymai išsaugomi.",
                  "Subtitrai kuriami iš kiekvieno žodžio laiko: 2–3 žodžių grupės, tariamas žodis paryškintas.",
                  "Perkėlus ar apkarpius garso klipą, subtitrai pasislenka kartu.",
                  "MP4 atvaizduojamas fone, matosi eigos procentai."]),
            ],
            "role": "Viena kūriau visą įrankį: redaktorių, video variklį, serverį ir testus.",
            "decisions": [
                ("Video kaip duomenys:", "visas projektas yra JSON, tikrinamas Zod schemomis. Tos pačios schemos naudojamos redaktoriuje, serverio API ir importuojant, o seni projektų failai automatiškai atnaujinami, ne atmetami. AI agentas gali sugeneruoti projekto scenarijų, ir jis patikrinamas iš karto."),
                ("Tipų saugus API:", "tRPC tarp serverio ir kliento, todėl pakeitus API klaida matoma kompiliuojant. Serverio duomenys – TanStack Query, redaguojama būsena – Zustand su atšaukimo istorija. Automatinis išsaugojimas tik tada, kai projektas pasikeitė."),
                ("Išdėstymas, kurio negalima perpildyti:", "kiekvienas vizualas žino savo natūralų dydį, o šablonai pritaiko mastelį saugiai zonai."),
                ("Viena animacijų sistema:", "įėjimai, išėjimai, keyframe'ai ir perėjimai turi po vieną įgyvendinimą, o scenų laikas skaičiuojamas vienoje vietoje."),
                ("Automatika:", "įmesti failai iškart atsiranda redaktoriuje, įkelti ekrano įrašai perkoduojami tiksliam slinkimui per kadrus, API padengtas testais."),
            ],
            "scale": "113 komponentų · 7 scenų ir 25 vizualų tipai · 44 vizualų šablonai · 109 testai · 27 API procedūros",
            "stack": "React, TypeScript, Vite, Mantine, Tailwind CSS, Zustand, TanStack Query · Remotion · Node.js, Express, tRPC, Zod · Vitest, supertest · ffmpeg · ElevenLabs",
            "desc": "TikMaker: vaizdo redaktorius ir dizaino sistema trumpiems vertikaliems vaizdo įrašams, su laiko juosta, AI įgarsinimu ir žodžių subtitrais. React, Remotion, tRPC.",
        },
        "en": {
            "title": "TikMaker", "meta": "video editor · personal project · 2026",
            "what": "A video editor and design system for short vertical (9:16) TikTok, Reels and Shorts videos. Videos no longer need to be edited by hand: they're assembled from ready-made scenes, visuals and animations, so every video looks consistent and gets made faster.",
            "status": "A working tool I use for my own content.",
            "features": [
                ("b", ("tik", "The TikMaker editor: scene list, preview, settings and a multi-row timeline"),
                 "A timeline like in an editing app",
                 "The experience of a professional editing app, adapted to this system: every element can be placed precisely in time without any other software.",
                 ["Clips are dragged in time and between rows and snap to scene edges, the playhead and other clips.",
                  "Keyframes change position and scale over time and can be dragged.",
                  "Copy, paste, duplicate (Ctrl+C / V / D), and swap an element's file while keeping its animations.",
                  "Audio waveforms on the timeline.",
                  "Any action can be undone and redone."]),
                ("c", ("tik_library", "TikMaker: the element library and the vertical video preview of a scene"),
                 "A design system that doesn't let you make mistakes",
                 "Videos aren't drawn from scratch but assembled from proven parts. Text never spills out of the frame, scenes aren't cut too early, and the style is always consistent.",
                 ["7 scene types, 25 visual types (terminal, code diffs, browser and phone mockups, diagrams, statistics) and 7 backgrounds.",
                  "Scene length is calculated automatically from the voice-over text and the reading time of on-screen text.",
                  "Layout templates fit each visual into the safe zone that TikTok's interface doesn't cover.",
                  "An element can travel smoothly from one scene to the next.",
                  "The editor warns about a scene that's too short, an overcrowded frame or code lines that are too long."]),
                ("a", ("tik_voice", "TikMaker: the preview, the “Render MP4” button and the scene's voice-over text in the inspector"),
                 "From text to voice, subtitles and MP4",
                 "From written text the system creates the voice-over and TikTok-style subtitles itself, and renders the final video with one button.",
                 ["The voice-over is generated with ElevenLabs, and voice settings are saved.",
                  "Subtitles are built from each word's timing: groups of 2–3 words with the spoken word highlighted.",
                  "When an audio clip is moved or trimmed, the subtitles move with it.",
                  "MP4 renders in the background, with progress shown in percent."]),
            ],
            "role": "I built the whole tool on my own: the editor, the video engine, the server and the tests.",
            "decisions": [
                ("Video as data:", "the whole project is JSON validated with Zod schemas. The same schemas are used in the editor, the server API and on import, and old project files are upgraded automatically rather than rejected. An AI agent can generate a project script, and it's validated straight away."),
                ("Type-safe API:", "tRPC between server and client, so an API change shows up as a compile error. Server data lives in TanStack Query, editable state in Zustand with undo history. Autosave runs only when the project has actually changed."),
                ("Layout that can't overflow:", "every visual knows its natural size, and templates scale it to the safe zone."),
                ("One animation system:", "entrances, exits, keyframes and transitions each have one implementation, and scene timing is calculated in one place."),
                ("Automation:", "dropped-in files appear in the editor immediately, uploaded screen recordings are transcoded for frame-accurate scrubbing, and the API is covered by tests."),
            ],
            "scale": "113 components · 7 scene and 25 visual types · 44 visual templates · 109 tests · 27 API procedures",
            "stack": "React, TypeScript, Vite, Mantine, Tailwind CSS, Zustand, TanStack Query · Remotion · Node.js, Express, tRPC, Zod · Vitest, supertest · ffmpeg · ElevenLabs",
            "desc": "TikMaker: a video editor and design system for short vertical videos, with a timeline, AI voice-over and word-level subtitles. React, Remotion, tRPC.",
        },
    },
    "p_loy": {
        "next": "p_lang",
        "tone": "sand",
        "lt": {
            "title": "Lojalumo valdymo sistema", "meta": "B2B backoffice · komandinis projektas · 2026",
            "what": "Administravimo sistema verslo lojalumo programoms: kortelės, klientai, akcijos ir kuponai valdomi vienoje vietoje. Projektas konfidencialus, todėl ekrano kopijose duomenys uždengti, o aprašymas trumpas.",
            "status": "Aktyviai vystoma.",
            "features": [
                ("hero", ("loy_cards", "Kortelių sąrašas kairėje ir pasirinktos kortelės detalės dešinėje, duomenys uždengti"),
                 "Kortelės ir klientai",
                 "Visa informacija apie kortelę ir jos savininką viename ekrane: sąrašas kairėje, pasirinktas įrašas dešinėje.", []),
                ("a", ("loy_promo", "Akcijų sąrašas ir akcijos išbandymas prieš paleidžiant, duomenys uždengti"),
                 "Akcijos",
                 "Akcijas galima sukurti ir išbandyti dar prieš jas paleidžiant.", []),
            ],
            "role": "Pagrindinė frontend programuotoja komandoje su backend programuotoju, taip pat dalis backend darbų.",
            "decisions": [
                ("", "API klientas generuojamas iš backend'o OpenAPI aprašo, todėl frontend ir backend tipai visada sutampa."),
                ("", "Meniu, skirtukai ir maršrutų apsauga kuriami iš vieno aprašo pagal naudotojo leidimus."),
                ("", "Integraciniai testai tikrina ekranus su skirtingais rolių leidimais."),
            ],
            "scale": "3 kalbos · ~730 frontend testų",
            "stack": "React, TypeScript, RTK Query, AG Grid, Tailwind CSS, shadcn/ui · .NET, SQL Server · Vitest, Playwright",
            "note": "Daugiau apie šį projektą galiu papasakoti pokalbio metu.",
            "desc": "Lojalumo valdymo sistema: B2B administravimo sistema lojalumo programoms. Komandinis projektas, React, TypeScript ir .NET.",
        },
        "en": {
            "title": "Loyalty management system", "meta": "B2B back office · team project · 2026",
            "what": "An admin system for business loyalty programmes: cards, customers, promotions and coupons managed in one place. The project is confidential, so data in the screenshots is masked and the description is short.",
            "status": "Actively developed.",
            "features": [
                ("hero", ("loy_cards", "The card list on the left and the selected card's details on the right, data masked"),
                 "Cards and customers",
                 "Everything about a card and its owner on one screen: the list on the left, the selected record on the right.", []),
                ("a", ("loy_promo", "The promotion list and testing a promotion before launch, data masked"),
                 "Promotions",
                 "Promotions can be created and tested before they go live.", []),
            ],
            "role": "Lead frontend developer in a team with a backend developer, plus part of the backend work.",
            "decisions": [
                ("", "The API client is generated from the backend's OpenAPI description, so frontend and backend types always match."),
                ("", "Menus, tabs and route protection are built from a single definition based on the user's permissions."),
                ("", "Integration tests check screens with different role permissions."),
            ],
            "scale": "3 languages · ~730 frontend tests",
            "stack": "React, TypeScript, RTK Query, AG Grid, Tailwind CSS, shadcn/ui · .NET, SQL Server · Vitest, Playwright",
            "note": "I can tell you more about this project in an interview.",
            "desc": "Loyalty management system: a B2B admin system for loyalty programmes. A team project built with React, TypeScript and .NET.",
        },
    },
}

PL = {
    "lt": {"back": "← Visi darbai", "what": "Kas tai", "status": "Būsena", "tech": "Techninė dalis",
           "role": "Rolė", "decisions": "Sprendimai", "scale": "Mastas", "stack": "Stackas",
           "next": "Kitas darbas", "suffix": "projektas | Gabrielė Tamaševičiūtė"},
    "en": {"back": "← All work", "what": "What it is", "status": "Status", "tech": "Technical side",
           "role": "Role", "decisions": "Decisions", "scale": "Scale", "stack": "Stack",
           "next": "Next project", "suffix": "project | Gabrielė Tamaševičiūtė"},
}


def project(key, lang):
    d = PROJECTS[key][lang]
    tone = PROJECTS[key]["tone"]
    nxt = PROJECTS[key]["next"]
    l = PL[lang]
    t = T[lang]

    feats = []
    for i, (shape, media, h, lead, items) in enumerate(d["features"]):
        flip = " feature--flip" if i % 2 else ""
        if isinstance(media, tuple):
            image_key, alt = media
            visual = framed(image_key, alt, "(max-width: 759px) 92vw, 760px",
                            dark=image_key.startswith("tik"), crop=False)
        else:
            visual = f'<div class="shot-todo" role="img" aria-label="{esc(media.strip("[]"))}">{esc(media)}</div>'
        lst = ""
        if items:
            lst = '<ul class="feature__list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
        feats.append(f"""<div class="feature{flip}">
<div class="feature__text" data-reveal>
<div class="feature__head"><span class="mono" aria-hidden="true">0{i + 1} —</span><h2>{h}</h2></div>
<p class="lead">{lead}</p>
{lst}
</div>
<figure class="feature__media d1" data-reveal="far">
{blob(shape, tone)}
{visual}
</figure>
</div>""")

    if d["decisions"][0][0]:
        dec = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in d["decisions"])
    else:
        dec = "".join(f"<li>{b}</li>" for a, b in d["decisions"])
    note = f'<p class="lead p-tech__note">{d["note"]}</p>' if d.get("note") else ""

    body = f"""<section class="p-intro">
<div class="container">
<a class="back" href="{url("portfolio", lang)}">{l["back"]}</a>
<h1>{d["title"]}</h1>
<p class="p-meta">{todo(d["meta"])}</p>
<dl class="p-summary">
<div><dt class="mono">{l["what"]}</dt><dd>{d["what"]}</dd></div>
<div><dt class="mono">{l["status"]}</dt><dd>{todo(d["status"])}</dd></div>
</dl>
</div>
</section>
<section class="p-features" aria-label="{d["title"]}">
<div class="container">
{chr(10).join(feats)}
</div>
</section>
<section class="p-tech" aria-labelledby="tech-title">
<div class="container">
<div class="p-tech__title"><h2 id="tech-title">{l["tech"]}</h2></div>
<div class="p-tech__body">
<dl class="tech-list">
<div><dt>{l["role"]}</dt><dd>{d["role"]}</dd></div>
<div><dt>{l["decisions"]}</dt><dd><ul>{dec}</ul></dd></div>
<div><dt>{l["scale"]}</dt><dd>{d["scale"]}</dd></div>
<div><dt>{l["stack"]}</dt><dd class="tech-stack">{d["stack"]}</dd></div>
</dl>
{note}
</div>
</div>
</section>
<section class="p-foot">
<div class="container">
<a class="next" href="{url(nxt, lang)}"><span class="mono">{l["next"]}</span><strong>{PROJECTS[nxt][lang]["title"]} →</strong></a>
<a class="btn btn--lg" href="{url("contact", lang)}">{t["cta"]}</a>
</div>
</section>"""
    title = f'{d["title"]} – {l["suffix"]}'
    jsonld = [{
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": d["title"],
        "description": d["desc"],
        "url": SITE + url(key, lang),
        "inLanguage": lang,
        "creator": {"@id": SITE + "/#person"},
    }, {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": SITE + url(k, lang)}
            for i, (k, name) in enumerate([
                ("home", "Pradžia" if lang == "lt" else "Home"),
                ("portfolio", "Portfolio"),
                (key, d["title"]),
            ], 1)
        ],
    }]
    assemble(lang, key, title, d["desc"], body, jsonld=jsonld, og_type="article",
             body_class="page-project", current="portfolio")


# --------------------------------------------------------------------------
# Redirects for URLs that no longer have their own page
# --------------------------------------------------------------------------

def redirect(path, target, lang):
    text = "Puslapis perkeltas" if lang == "lt" else "This page has moved"
    go = "Eiti" if lang == "lt" else "Go"
    write(path, f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{text}</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{SITE}{target.split('#')[0]}">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}");</script>
</head>
<body>
<p>{text}. <a href="{target}">{go} →</a></p>
</body>
</html>
""")


def sitemap():
    # The old game pages are not linked from the site and carry noindex, so they stay out.
    urls = []
    for key in ("home", "portfolio", "services", "about", "contact", "p_lang", "p_tik", "p_loy"):
        for lang in ("lt", "en"):
            urls.append(SITE + url(key, lang))
    body = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
""")


def main():
    for lang in ("lt", "en"):
        home(lang)
        portfolio(lang)
        cv_sheet(lang)
        services_page(lang)
        about_page(lang)
        contact_page(lang)
        for key in ("p_lang", "p_tik", "p_loy"):
            project(key, lang)

    redirect("portfolio/index.html", "/lt/portfolio.html", "lt")
    # The guides were removed; their old addresses land on the home page.
    redirect("en/resources.html", "/en/", "en")
    redirect("en/resources/claude-code-commands.html", "/en/", "en")
    redirect("en/resources/claude-code-context.html", "/en/", "en")
    redirect("en/resources/claude-code-guardrails.html", "/en/", "en")
    redirect("en/resources/claude-code-hooks.html", "/en/", "en")
    redirect("en/resources/claude-code-intro.html", "/en/", "en")
    redirect("en/resources/claude-code-mcp.html", "/en/", "en")
    redirect("en/resources/claude-code.html", "/en/", "en")
    redirect("en/resources/start-coding.html", "/en/", "en")
    redirect("lt/resources.html", "/lt/", "lt")
    redirect("lt/resources/claude-code.html", "/lt/", "lt")
    redirect("lt/resources/start-coding.html", "/lt/", "lt")
    sitemap()


if __name__ == "__main__":
    main()
