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
    "about": ("about-illustration", 900, 1173, 600),
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
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/img/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/schibsted-grotesk/schibsted-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
<script>
  /* Hide reveal-on-scroll content only once we know JS runs. If site.js
     never arrives, put everything back after a moment. */
  document.documentElement.classList.add("js");
  setTimeout(function () {{ if (!window.__site) document.documentElement.classList.remove("js"); }}, 3000);
</script>
<script src="/js/site.js" defer></script>
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
        "hero_note": "Programuotoja Vilniuje · React, TypeScript, API ir AI funkcijos · Priimu naujus projektus",
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
            ("Parašote", "Trumpai, ko reikia. Techninių terminų nereikia."),
            ("Planas ir kaina", "Per 24 val. po pokalbio gaunate planą ir fiksuotą kainą raštu."),
            ("Kūrimas", "Progresą matote nuolat, ne tik pabaigoje."),
            ("Paleidimas", "Įdiegiu sistemą. Mano darbui taikoma 3 mėn. garantija."),
        ],
        "about_h": "Apie mane",
        "about_alt": "Gabrielės iliustracija",
        "about_text": "Esu Gabrielė, programuotoja iš Vilniaus. Kuriu sistemas, kuriomis žmonės naudojasi kasdien: nuo duomenų modelio iki sąsajos. Prieš keisdama kodą pirmiausia suprantu problemą.",
        "facts": ["2+ metai kuriant sistemas", "Frontend, backend ir API", "Dirbu su esamu kodu"],
        "about_more": "Daugiau apie mane →",
        "faq_h": "Dažni klausimai",
        "faq": [
            ("Kiek kainuoja projektas?", "[Įrašyti: nuo X € / kaip skaičiuojama]"),
            ("Kiek laiko trunka?", "[Įrašyti: tipinis terminas]"),
            ("Ar galite perimti jau veikiančią sistemą?", "Taip, perprantu esamą kodą ir tobulinu jį palaipsniui."),
            ("Ar kaina gali pasikeisti eigoje?", "Ne. Patvirtinus sąmatą, kaina nesikeičia."),
            ("Ar galite į sistemą įdiegti AI funkcijas?", "Taip, nuo paprastų LLM funkcijų iki agentų, kurie naudojasi sistemos API."),
        ],
        "contact_h": "Turite projekto idėją?",
        "contact_lead": "Parašykite kelis sakinius, ko reikia. [Atsakau per X darbo dienas.]",
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
        "footer_guides": "Gidai",
        "guides_url": "/lt/resources.html",
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
        "hero_note": "Developer in Vilnius · React, TypeScript, APIs and AI features · Taking on new projects",
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
            ("You write", "Briefly, what you need. No technical terms needed."),
            ("Plan and price", "Within 24 hours of our call you get a plan and a fixed price in writing."),
            ("Building", "You see progress all along, not only at the end."),
            ("Launch", "I deploy the system. My work comes with a 3-month warranty."),
        ],
        "about_h": "About me",
        "about_alt": "Illustration of Gabrielė",
        "about_text": "I'm Gabrielė, a developer from Vilnius. I build systems people use every day, from the data model to the interface. Before changing code, I first understand the problem.",
        "facts": ["2+ years building systems", "Frontend, backend and APIs", "I work with existing code"],
        "about_more": "More about me →",
        "faq_h": "Frequently asked questions",
        "faq": [
            ("How much does a project cost?", "[To fill in: from X € / how it's calculated]"),
            ("How long does it take?", "[To fill in: typical timeline]"),
            ("Can you take over a system that's already running?", "Yes, I get to know the existing code and improve it step by step."),
            ("Can the price change along the way?", "No. Once the estimate is approved, the price doesn't change."),
            ("Can you add AI features to the system?", "Yes, from simple LLM features to agents that use the system's API."),
        ],
        "contact_h": "Have a project idea?",
        "contact_lead": "Write a few sentences about what you need. [I reply within X working days.]",
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
        "footer_guides": "Guides",
        "guides_url": "/en/resources.html",
        "menu_nums": {"work": "01", "services": "02", "about": "04", "faq": "05"},
    },
}


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------

def home(lang):
    t = T[lang]
    ids = t["ids"]
    nav_links = "\n".join(
        f'<a href="#{ids[k]}" data-nav="{ids[k]}">{t["nav"][k]}</a>'
        for k in ("work", "services", "about", "faq"))
    menu_links = "\n".join(
        f'<a href="#{ids[k]}"><span class="mono" aria-hidden="true">{t["menu_nums"][k]}</span>{t["nav"][k]}</a>'
        for k in ("work", "services", "about", "faq"))

    header = f"""<a class="skip-link" href="#main">{t["skip"]}</a>
<header class="site-header site-header--home">
<div class="container site-header__in">
<a class="brand" href="{url("home", lang)}">Gabrielė Tamaševičiūtė</a>
<nav class="site-nav" aria-label="{t["nav_label"]}">
<div class="site-nav__links">
{nav_links}
<span class="site-nav__indicator" aria-hidden="true"></span>
</div>
{lang_link(lang, "home")}
<a class="btn" href="#{ids["contact"]}">{t["cta"]}</a>
</nav>
<button class="menu-toggle" type="button" data-menu-open aria-controls="mobile-menu" aria-expanded="false" aria-label="{t["menu_open"]}">{ICON_MENU}</button>
</div>
</header>
<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="{t["menu"]}" hidden>
<div class="mobile-menu__bar">
<a class="brand" href="{url("home", lang)}">Gabrielė Tamaševičiūtė</a>
<button class="menu-toggle" type="button" data-menu-close aria-label="{t["menu_close"]}">{ICON_CLOSE}</button>
</div>
<nav class="mobile-menu__nav" aria-label="{t["nav_label"]}">
{menu_links}
</nav>
<div class="mobile-menu__foot">
{lang_link(lang, "home")}
<a class="btn" href="#{ids["contact"]}">{t["cta"]}</a>
</div>
</div>"""

    hero = f"""<section class="hero" aria-labelledby="hero-title">
<div class="container grid hero__grid">
<div class="hero__copy">
<h1 class="hero__title" id="hero-title" data-reveal>{t["h1"]}</h1>
<p class="lead hero__lead d1" data-reveal>{t["lead"]}</p>
<div class="hero__ctas d2" data-reveal>
<a class="btn btn--lg" href="#{ids["contact"]}">{t["cta"]}</a>
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
<div class="sec-head" data-reveal><span class="mono" aria-hidden="true">01 —</span><h2 class="h2" id="work-title">{t["work_h"]}</h2></div>
{chr(10).join(rows)}
<div class="work-all"><a class="link" href="{url("portfolio", lang)}">{t["all_projects"]}</a></div>
</div>
</section>"""

    svc = "\n".join(
        f"""<div class="service{(' d' + str(i)) if i else ''}" data-reveal>
<h3>{h}</h3>
<p class="small service__fit">{fit}</p>
<p class="service__text">{txt}</p>
</div>""" for i, (h, fit, txt) in enumerate(t["services"]))
    services = f"""<section class="section" id="{ids["services"]}" aria-labelledby="services-title">
<div class="container">
<div class="sec-head" data-reveal><span class="mono" aria-hidden="true">02 —</span><h2 class="h2" id="services-title">{t["services_h"]}</h2></div>
<div class="grid services">
{svc}
</div>
</div>
</section>"""

    st = "\n".join(
        f"""<li class="step{(' d' + str(i)) if i else ''}" data-reveal>
<span class="mono">{i + 1}</span>
<h3>{h}</h3>
<p>{p}</p>
</li>""" for i, (h, p) in enumerate(t["steps"]))
    steps = f"""<section class="section section--raised" aria-labelledby="steps-title">
<div class="container">
<div class="sec-head" data-reveal><span class="mono" aria-hidden="true">03 —</span><h2 class="h2" id="steps-title">{t["steps_h"]}</h2></div>
<ol class="grid steps">
{st}
</ol>
</div>
</section>"""

    facts = "".join(f"<li>{f}</li>" for f in t["facts"])
    about = f"""<section class="section" id="{ids["about"]}" aria-labelledby="about-title">
<div class="container grid about">
<div class="about__media" data-reveal="far">
{blob("a", "apricot")}
{img("about", t["about_alt"], "(max-width: 759px) 88vw, 340px")}
</div>
<div class="about__text d1" data-reveal>
<div class="sec-head sec-head--tight"><span class="mono" aria-hidden="true">04 —</span><h2 class="h2" id="about-title">{t["about_h"]}</h2></div>
<p class="lead">{t["about_text"]}</p>
<ul class="facts">{facts}</ul>
<a class="link" href="{url("portfolio", lang)}">{t["about_more"]}</a>
</div>
</div>
</section>"""

    items = []
    for i, (q, a) in enumerate(t["faq"], 1):
        items.append(f"""<div class="faq__item">
<h3 class="faq__q"><button class="faq__btn" type="button" data-faq aria-expanded="true" aria-controls="faq-{i}">{q}{ICON_PLUS}</button></h3>
<div class="faq__a" id="faq-{i}"><p>{todo(a)}</p></div>
</div>""")
    faq = f"""<section class="section section--raised" id="{ids["faq"]}" aria-labelledby="faq-title">
<div class="container grid">
<div class="faq-wrap" data-reveal>
<div class="sec-head"><span class="mono" aria-hidden="true">05 —</span><h2 class="h2" id="faq-title">{t["faq_h"]}</h2></div>
<div class="faq">
{chr(10).join(items)}
</div>
</div>
</div>
</section>"""

    contact = f"""<section class="section" id="{ids["contact"]}" aria-labelledby="contact-title">
<div class="container grid contact">
<div class="contact__text" data-reveal>
<div class="sec-head sec-head--tight"><span class="mono" aria-hidden="true">06 —</span><h2 class="h2" id="contact-title">{t["contact_h"]}</h2></div>
<p class="lead">{todo(t["contact_lead"])}</p>
<ul class="contact__links">
<li><a class="link-plain" href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a class="link-plain" href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></li>
<li><a class="link-plain" href="{GITHUB}" rel="me noopener" target="_blank">github.com/gabwowce</a></li>
</ul>
</div>
<form class="form d1" data-reveal data-contact action="{FORMSPREE}" method="POST" data-msg-sending="{esc(t["f_sending"])}" data-msg-ok="{esc(t["f_ok"])}" data-msg-fail="{esc(t["f_fail"])}" data-msg-invalid="{esc(t["f_invalid"])}">
<div class="form__row">
<label class="field">{t["f_name"]}<input type="text" name="name" autocomplete="name" required></label>
<label class="field">{t["f_email"]}<input type="email" name="email" autocomplete="email" required></label>
</div>
<label class="field">{t["f_msg"]}<textarea name="message" rows="6" required></textarea></label>
<div class="form__hp" aria-hidden="true"><label>{t["f_hp"]}<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="_subject" value="{esc(t["f_subject"])}">
<div><button class="btn" type="submit">{t["f_send"]}</button></div>
<p class="form__status" role="status" aria-live="polite"></p>
</form>
</div>
</section>"""

    footer = f"""<footer class="site-footer">
<div class="container site-footer__in">
<span>Gabrielė Tamaševičiūtė · © {YEAR}</span>
<div class="site-footer__links">
<a class="link-plain" href="{url("portfolio", lang)}">{t["footer_cv"]}</a>
<a class="muted-link" href="{t["guides_url"]}">{t["footer_guides"]}</a>
<a class="muted-link" href="mailto:{EMAIL}">{EMAIL}</a>
{lang_link(lang, "home")}
</div>
</div>
</footer>"""

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
            "priceRange": "$$",
            "address": {"@type": "PostalAddress", "addressLocality": "Vilnius", "addressCountry": "LT"},
            "areaServed": [{"@type": "Country", "name": "Lietuva" if lang == "lt" else "Lithuania"}],
            "availableLanguage": ["lt", "en"],
            "founder": {"@id": SITE + "/#person"},
            "sameAs": [GITHUB, TIKTOK, LINKEDIN],
        },
        person_ld(lang),
    ]

    page = head(lang, "home", t["home_title"], t["home_desc"], jsonld=jsonld)
    page += "<body>\n" + header + '\n<main id="main">\n' + "\n".join(
        [hero, works, services, steps, about, faq, contact]) + "\n</main>\n" + footer + "\n</body>\n</html>\n"
    write(ROUTES["home"][lang], page)


def person_ld(lang):
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": SITE + "/#person",
        "name": "Gabrielė Tamaševičiūtė",
        "jobTitle": "Frontend / full-stack programuotoja" if lang == "lt" else "Frontend / full-stack developer",
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
        "title": "Gabrielė Tamaševičiūtė – CV ir portfolio | Frontend / full-stack programuotoja",
        "desc": "Frontend / full-stack programuotoja Vilniuje (React, TypeScript): atrinkti darbai, patirtis, technologijos ir CV.",
        "back": "← codeart.lt",
        "role": "Frontend / full-stack programuotoja · React, TypeScript",
        "where": "Vilnius · [BŪSENA, pvz. Atvira pasiūlymams]",
        "contacts_label": "Kontaktai",
        "cv_pdf": "CV (PDF)",
        "cv_dl": "Atsisiųsti CV (PDF)",
        "facts_label": "Trumpai",
        "facts": [("Dabar", "Programuotoja (Mid), UVS"), ("Patirtis", "2+ m. profesionaliai"),
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
             ["React", "TypeScript", "RTK Query", "AG Grid", ".NET"],
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
            ("Frontend", ["React", "TypeScript", "Next.js", "Tailwind", "RTK Query", "AG Grid"]),
            ("Backend ir duomenys", ["REST API", "Supabase", "Autentifikacija", "Duomenų bazės"]),
            ("Kita", ["C#/.NET", "WPF", "Figma", "WordPress", "LLM integracijos", "AI agentai"]),
        ],
        "edu_l": "Išsilavinimas",
        "edu": "Vilniaus kolegija, Programų sistemos, 2023–2027 (studijuoju)",
        "more": "Daugiau darbų (Kidcan, Kibinai Vilnius, AutoRent ir kt.) ir išsamūs aprašymai: codeart.lt/portfolio",
        "sheet_title": "Gabrielė Tamaševičiūtė – CV",
        "sheet_foot": "Gabrielė Tamaševičiūtė · CV",
    },
    "en": {
        "title": "Gabrielė Tamaševičiūtė – CV and portfolio | Frontend / full-stack developer",
        "desc": "Frontend / full-stack developer in Vilnius (React, TypeScript): selected work, experience, technologies and CV.",
        "back": "← codeart.lt",
        "role": "Frontend / full-stack developer · React, TypeScript",
        "where": "Vilnius · [STATUS, e.g. Open to offers]",
        "contacts_label": "Contacts",
        "cv_pdf": "CV (PDF)",
        "cv_dl": "Download CV (PDF)",
        "facts_label": "In short",
        "facts": [("Now", "Developer (Mid), UVS"), ("Experience", "2+ years professionally"),
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
             ["React", "TypeScript", "RTK Query", "AG Grid", ".NET"],
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
            ("Frontend", ["React", "TypeScript", "Next.js", "Tailwind", "RTK Query", "AG Grid"]),
            ("Backend and data", ["REST API", "Supabase", "Authentication", "Databases"]),
            ("Other", ["C#/.NET", "WPF", "Figma", "WordPress", "LLM integrations", "AI agents"]),
        ],
        "edu_l": "Education",
        "edu": "Vilnius University of Applied Sciences (Vilniaus kolegija), Software Systems, 2023–2027 (in progress)",
        "more": "More work (Kidcan, Kibinai Vilnius, AutoRent and others) and full write-ups: codeart.lt/en/portfolio.html",
        "sheet_title": "Gabrielė Tamaševičiūtė – CV",
        "sheet_foot": "Gabrielė Tamaševičiūtė · CV",
    },
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
    for name, desc, stack, year, links in p["others"]:
        ls = "".join(f'<a class="link" href="{u}" target="_blank" rel="noopener" aria-label="{name}: {label}">{label} ↗</a>'
                     for label, u in links)
        others.append(f"""<li><span class="r-name">{name}</span><span class="r-desc">{desc}</span><span class="r-stack">{stack}</span><span class="r-year">{year}</span><span class="r-links">{ls}</span></li>""")

    exp = "\n".join(
        f'<li{" class=\"is-past\"" if past else ""}><span class="t-date">{d}</span><span class="t-role">{r}</span><span class="t-what">{w}</span></li>'
        for d, r, w, past in p["exp"])

    tech = "\n".join(
        f'<div><dt>{g}</dt><dd>{"".join(f"<span class=\"tag\">{x}</span>" for x in items)}</dd></div>'
        for g, items in p["tech"])

    body = f"""<body class="page-cv">
<header class="cv-head">
<div class="container">
<div class="cv-head__top"><a class="back" href="{url("home", lang)}">{p["back"]}</a>{lang_link(lang, "portfolio")}</div>
<div class="cv-head__row">
<div>
<h1>Gabrielė Tamaševičiūtė</h1>
<p class="cv-head__role">{p["role"]}</p>
<p class="cv-head__where">{todo(p["where"])}</p>
<nav class="cv-head__links" aria-label="{p["contacts_label"]}">
<a href="{pdf(lang)}">{p["cv_pdf"]}</a>
<a href="{GITHUB}" target="_blank" rel="me noopener">GitHub</a>
<a href="{LINKEDIN}" target="_blank" rel="me noopener">LinkedIn</a>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</nav>
</div>
<a class="btn btn--lg" href="{pdf(lang)}">{p["cv_dl"]}</a>
</div>
</div>
</header>
<main id="main" class="container">
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
</main>
<footer class="cv-foot">
<div class="container">
<p><strong>{p["edu_l"]}</strong> · {p["edu"]}</p>
<div class="cv-foot__actions">
<a class="link-plain" href="mailto:{EMAIL}">{EMAIL}</a>
<a class="btn btn--md" href="{pdf(lang)}">{p["cv_dl"]}</a>
</div>
</div>
</footer>
</body>
</html>
"""
    page = head(lang, "portfolio", p["title"], p["desc"], jsonld=[person_ld(lang)], og_type="profile")
    write(ROUTES["portfolio"][lang], page + body)


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
    tech = "\n".join(f"<div><dt>{g}</dt><dd>{' · '.join(items)}</dd></div>" for g, items in p["tech"])
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
            "title": "Kalbų mokymosi platforma", "meta": "web platforma · [KLIENTINIS PROJEKTAS / KLIENTO PAVADINIMAS] · 2026",
            "what": "Internetinė kalbų mokymosi sistema iš trijų dalių: vieša mokymų svetainė, mokinio mokymosi platforma ir turinio valdymo sistema. Kursus administratorius kuria pats, be programuotojo: sistema iš įvesto žodyno sudaro interaktyvias užduotis, valdo prieigą prie kursų per aktyvavimo kodus, seka mokinių progresą ir baigus lygį išduoda sertifikatą.",
            "status": "[BŪSENA]",
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
                ("a", "[Ekrano kopija: importo dialogo analizės žingsnis su santrauka, įspėjimais apie dublikatus ir laukiamais medijos failais]",
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
            "title": "Language learning platform", "meta": "web platform · [CLIENT PROJECT / CLIENT NAME] · 2026",
            "what": "An online language learning system in three parts: a public course website, a learner platform and a content management system. The admin builds courses on their own, without a developer: the system turns the entered vocabulary into interactive exercises, manages course access through activation codes, tracks learner progress and issues a certificate when a level is completed.",
            "status": "[STATUS]",
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
                ("a", "[Screenshot: the analysis step of the import dialog with a summary, duplicate warnings and expected media files]",
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
                ("c", "[Ekrano kopija: Visuals biblioteka su miniatiūromis ir peržiūra su saugios zonos perdanga]",
                 "Dizaino sistema, kuri neleidžia suklysti",
                 "Video ne piešiamas nuo nulio, o surenkamas iš patikrintų dalių. Tekstas neišlenda už kadro, scenos nenukerpamos per anksti, o stilius visada vienodas.",
                 ["7 scenų tipai, 25 vizualų tipai (terminalas, kodo pakeitimai, naršyklės ir telefono maketai, diagramos, statistika) ir 7 fonai.",
                  "Scenos trukmė apskaičiuojama automatiškai iš balso teksto ir ekrane rodomo teksto skaitymo laiko.",
                  "Išdėstymo šablonai vizualą pritaiko saugiai zonai, kurios neuždengia TikTok sąsaja.",
                  "Elementas gali sklandžiai „keliauti“ iš scenos į sceną.",
                  "Redaktorius įspėja apie per trumpą sceną, perpildytą kadrą ar per ilgas kodo eilutes."]),
                ("a", "[Ekrano kopija: peržiūra su subtitrais ir paryškintu žodžiu, garso klipas laiko juostoje, Render MP4 eigos būsenoje]",
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
                ("c", "[Screenshot: the Visuals library with thumbnails and a preview with the safe-zone overlay]",
                 "A design system that doesn't let you make mistakes",
                 "Videos aren't drawn from scratch but assembled from proven parts. Text never spills out of the frame, scenes aren't cut too early, and the style is always consistent.",
                 ["7 scene types, 25 visual types (terminal, code diffs, browser and phone mockups, diagrams, statistics) and 7 backgrounds.",
                  "Scene length is calculated automatically from the voice-over text and the reading time of on-screen text.",
                  "Layout templates fit each visual into the safe zone that TikTok's interface doesn't cover.",
                  "An element can travel smoothly from one scene to the next.",
                  "The editor warns about a scene that's too short, an overcrowded frame or code lines that are too long."]),
                ("a", "[Screenshot: the preview with subtitles and a highlighted word, an audio clip on the timeline, Render MP4 in progress]",
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
                            dark=(image_key == "tik"), crop=False)
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

    body = f"""<body class="page-project">
<a class="skip-link" href="#main">{t["skip"]}</a>
<header class="site-header site-header--compact">
<div class="container site-header__in">
<a class="brand" href="{url("home", lang)}">Gabrielė Tamaševičiūtė</a>
<a class="btn" href="{url("home", lang)}#{t["ids"]["contact"]}">{t["cta"]}</a>
</div>
</header>
<main id="main">
<section class="p-intro">
<div class="container">
<div class="p-intro__top"><a class="back" href="{url("portfolio", lang)}">{l["back"]}</a>{lang_link(lang, key)}</div>
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
</main>
<footer class="p-foot">
<div class="container">
<a class="next" href="{url(nxt, lang)}"><span class="mono">{l["next"]}</span><strong>{PROJECTS[nxt][lang]["title"]} →</strong></a>
<a class="btn btn--lg" href="{url("home", lang)}#{t["ids"]["contact"]}">{t["cta"]}</a>
</div>
</footer>
</body>
</html>
"""
    title = f'{d["title"]} – {l["suffix"]}'
    jsonld = [{
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": d["title"],
        "description": d["desc"],
        "url": SITE + url(key, lang),
        "inLanguage": lang,
        "creator": {"@id": SITE + "/#person"},
    }]
    page = head(lang, key, title, d["desc"], jsonld=jsonld, og_type="article")
    write(ROUTES[key][lang], page + body)


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
    keep = []
    old = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for loc in re.findall(r"<loc>([^<]+)</loc>", old):
        if "/resources" in loc or "/game.html" in loc:
            keep.append(loc)
    new = []
    for key in ("home", "portfolio", "p_lang", "p_tik", "p_loy"):
        for lang in ("lt", "en"):
            new.append(SITE + url(key, lang))
    urls = new + [u for u in keep if u not in new]
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
        for key in ("p_lang", "p_tik", "p_loy"):
            project(key, lang)

    redirect("lt/about.html", "/lt/#apie", "lt")
    redirect("lt/services.html", "/lt/#paslaugos", "lt")
    redirect("lt/contact.html", "/lt/#kontaktai", "lt")
    redirect("en/about.html", "/en/#about", "en")
    redirect("en/contact.html", "/en/#contact", "en")
    redirect("portfolio/index.html", "/lt/portfolio.html", "lt")
    sitemap()


if __name__ == "__main__":
    main()
