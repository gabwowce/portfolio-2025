#!/usr/bin/env python3
"""
Rebuild the portfolio into one featured project plus a uniform grid.

The page had grown two different card shapes at once: four "system" cards
with three paragraphs of prose and a split layout, and five plain cards
with one paragraph and a thumbnail. Scanned quickly, that reads as clutter
- every card fighting the next one for a different amount of attention.

The fix a portfolio page actually wants: ONE project leads (the strongest
system, full width, with the depth it deserves), and everything else sits
in a grid where every card is the same shape - same thumbnail box, one
short paragraph, a handful of chips, the links. Consistency there is the
point: a recruiter scanning eight identical-height cards can compare them
in five seconds; eight different heights and they read as noise.

The featured project keeps the "hard part / my role" depth that a system
project earns. Grid cards get one paragraph - enough to say what it is and
why it is not a toy, not a case study.

Run:  python3 tools/build-portfolio-grid.py

Rewrites the whole <div class="featured-grid">...</div> block in both
locales. Re-running is safe; it looks for the same wrapper each time.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

FEATURED_ID = "loyalty-backoffice"

# --------------------------------------------------------------------------
# The featured project - full data, both locales.
# --------------------------------------------------------------------------

FEATURED = {
    "lt": {
        "eyebrow": "Iškirtinis projektas",
        "title": "Lojalumo valdymo sistema — B2B backoffice",
        "sub": "Web · klientinis projektas · ekranai su uždengtais duomenimis",
        "desc": "Kasdien naudojama vidinė sistema: lojalumo kortelės, kortelių "
                "turėtojai, organizacijos ir transakcijos. Naudotojai — įmonės "
                "darbuotojai, ne galutiniai klientai, todėl viskas sukasi apie "
                "teises, auditą ir duomenų tikslumą.",
        "hard_label": "Sunkiausia dalis",
        "hard": "Ne sąsaja, o duomenų ir logikos nuoseklumas su gyvu, "
                "nuolat besikeičiančiu backend'u. API tipai generuojami iš "
                "backend'o schemos, tad kiekvienas jos pakeitimas turi būti "
                "persinchronizuotas prieš tai, kai jį pastebi naudotojas. "
                "Masiniai kortelių veiksmai turi du visiškai skirtingus "
                "kelius, kuriuos abu reikia palaikyti vienodai.",
        "role_label": "Mano vaidmuo",
        "role": "Ne tik frontend'as. Formuluoju užduotis backend'o kolegai, "
                "derinu API kontraktus ir prižiūriu projektą kaip visumą — o "
                "patį pradžios etapą, kol prisijungė backend'o žmogus, "
                "dariau viena.",
        "cta": "Peržiūrėti projekto detales",
        "facts": [("~27", "maršrutų"), ("8", "sričių"),
                  ("2 × ~2200", "vertimo raktų"), ("Rolės", "ir auditas")],
    },
    "en": {
        "eyebrow": "Featured project",
        "title": "Loyalty management system — B2B backoffice",
        "sub": "Web · client project · screens with data redacted",
        "desc": "An internal system in daily use: loyalty cards, "
                "cardholders, organisations and transactions. Its users are "
                "the company's own staff, not end customers, so everything "
                "turns on permissions, auditability and data accuracy.",
        "hard_label": "The hard part",
        "hard": "Not the interface — keeping data and logic consistent with "
                "a live backend that keeps changing. API types are "
                "generated from the backend schema, so every schema change "
                "has to be re-synced before a user runs into it. Bulk card "
                "actions have two completely different paths that both "
                "need equal support.",
        "role_label": "My role",
        "role": "Not just the frontend. I scope and hand off work to the "
                "backend developer, agree the API contracts and steer the "
                "project as a whole — and I built the early stage alone, "
                "before a backend developer joined.",
        "cta": "View project details",
        "facts": [("~27", "routes"), ("8", "domains"),
                  ("2 × ~2200", "translation keys"), ("Roles", "and audit")],
    },
}

FEATURED_NODES = [
    ("React + TS", "backoffice UI", ""),
    ("RTK Query", "tipai iš schemos|types from schema", ""),
    ("AG Grid", "didelės lentelės|large tables", ""),
    ("REST API", "gyvas backend'as|live backend", ""),
]

FEATURED_IMG = ("img/ac-cards-redacted", 1400, 773,
                "Lojalumo backoffice — kortelių sąrašas ir kortelės įrašas, "
                "duomenys uždengti"
                "|Loyalty backoffice — card list and card record, data redacted")

# Second shot for the featured project's gallery - shown when the thumb is
# clicked, not on the card itself.
FEATURED_GALLERY_EXTRA = ("img/ac-loyalty-redacted", 1400,
                          "Akcijų testavimas su virtualiu krepšeliu, "
                          "duomenys uždengti"
                          "|Promotion testing with a virtual basket, "
                          "data redacted")


# --------------------------------------------------------------------------
# The grid - one short paragraph each, same shape.
# --------------------------------------------------------------------------
# link: (label, url) or None. A project can carry more than one.

GRID = [
    {
        "id": "tikmaker", "cat": "web", "tier": "lg",
        "img": "img/TikMaker/main-1400.webp",
        "title": "TikMaker — vaizdo redaktorius su AI įgarsinimu"
                  "|TikMaker — video editor with AI voiceover",
        "year": "2026", "badge": "AI viduje|AI inside",
        "desc": "Vaizdo redaktorius savo TikTok / Reels turiniui: "
                "ElevenLabs balso takelis integruotas tiesiai į timeline "
                "kaip bet kuris kitas efektas. Vidinis darbo įrankis, ne "
                "parduodamas produktas."
                "|A video editor for my own TikTok / Reels content: an "
                "ElevenLabs voice track wired directly into the timeline "
                "like any other effect. An internal tool I use myself, not "
                "a product for sale.",
        "chips": ["React + TS", "ElevenLabs", "Remotion"],
        "links": [],
    },
    {
        "id": "keepmi", "cat": "web", "tier": "lg",
        "img": "img/keepmi/landing-hero-1400.webp",
        "gallery": [
            ("img/keepmi/landing-hero",
             "keepmi — pradinis puslapis|keepmi — landing page"),
            ("img/keepmi/dashboard",
             "keepmi — organizatoriaus skydelis|keepmi — organiser dashboard"),
            ("img/keepmi/select-design",
             "keepmi — kvietimo dizaino parinkimas|keepmi — invitation design picker"),
        ],
        "title": "keepmi — skaitmeniniai kvietimai ir švenčių svečių hub'as"
                  "|keepmi — digital invitations and a guest hub",
        "year": "2026",
        "desc": "Skaitmeniniai kvietimai su svečių palinkėjimų rinkimu iki "
                "šventės, o pačią dieną — visas svečių hub'as vienoje "
                "vietoje: albumas, programa, viktorinos. Trys kalbos, "
                "Stripe apmokėjimai. Veikiantis MVP — realių naudotojų kol "
                "kas nėra."
                "|Digital invitations that collect video wishes before the "
                "event, then become a full guest hub on the day: photo "
                "album, program, quizzes. Three languages, Stripe billing. "
                "A working MVP — no real users yet.",
        "chips": ["Next.js", "next-intl", "Supabase", "Stripe"],
        "links": [("Live demo", "https://keepmi.app/")],
    },
    {
        "id": "kidcan", "cat": "mobile", "img": "img/kidcan.png",
        "title": "Kidcan — Parent & Kids mobile apps",
        "year": "2025",
        "desc": "Šeimų saugumo sprendimas: tėvai realiu laiku mato vaiko "
                "buvimo vietą per atskirą tėvų ir vaikų aplikacijų porą. "
                "Sukurta nuo nulio — dizainas, dvi mobilios aplikacijos ir "
                "bendras serveris."
                "|A family-safety solution: parents see their child's "
                "location in real time through a matched pair of parent "
                "and child apps. Built from scratch — design, two mobile "
                "apps, a shared backend.",
        "chips": ["React Native", "Expo", "Kotlin", "Supabase"],
        "links": [("Parents App", "https://github.com/gabwowce/KidcanParentsExpo"),
                  ("Kids App", "https://github.com/gabwowce/KidcanKids")],
    },
    {
        "id": "kibinai", "cat": "web", "img": "img/kibinai-group.png",
        "title": "Kibinai Vilnius — Headless React + WordPress",
        "year": "2025",
        "desc": "Restorano svetainė realiam verslui: meniu, turinys ir "
                "naujienos redaguojami be programuotojo pagalbos, o "
                "lankytojai mato greitai kraunamą, SEO-optimizuotą svetainę."
                "|A restaurant website for a real business: menu, content "
                "and news are all editable without a developer, while "
                "visitors get a fast-loading, SEO-optimised site.",
        "chips": ["React", "WordPress"],
        "links": [("Live demo", "https://kibinaivilnius.lt/"),
                  ("GitHub", "https://github.com/gabwowce/Kibinukai")],
    },
    {
        "id": "ltsa", "cat": "web", "img": "img/LTSA.png",
        "title": "LTSA — (HTML + CSS + JS)",
        "year": "2026",
        "desc": "Interaktyvi viktorina su el. pašto rinkimu — atsakymai "
                "automatiškai suvedami į Google Sheets, be jokio rankinio "
                "duomenų tvarkymo."
                "|An interactive quiz that collects emails automatically — "
                "every response lands in Google Sheets with zero manual "
                "data entry.",
        "chips": ["HTML", "CSS", "JS"],
        "links": [("Live demo", "https://ltsa.vercel.app/")],
    },
    {
        "id": "autorent", "cat": "web", "img": "img/Group 200.webp",
        "title": "AutoRent — automobilių nuoma"
                  "|AutoRent — car rental",
        "year": "2025",
        "desc": "Automobilių nuomos platforma su pilnu rezervacijos "
                "srautu: katalogas, paieška, filtrai, datų pasirinkimas ir "
                "užsakymo patvirtinimas."
                "|A car-rental platform with a complete booking flow: "
                "catalog, search, filters, date selection, order "
                "confirmation.",
        "chips": ["React", "FastAPI", "PostgreSQL"],
        "links": [("Live demo", "https://car-rental-frontend-v2.vercel.app/"),
                  ("GitHub", "https://github.com/gabwowce/car-rental-frontend")],
    },
    {
        "id": "travel-app", "cat": "mobile", "img": "img/123.webp",
        "title": "Travel App — React Native (Expo)",
        "year": "2025",
        "desc": "Kelionių planavimo aplikacijos pagrindas — veikia tiek "
                "Android, tiek iOS iš vieno kodo. Paruošta struktūra "
                "registracijai, žemėlapiams ir maršrutams."
                "|A foundation for a travel-planning app, running on both "
                "Android and iOS from one codebase. Ready-made structure "
                "for sign-up, maps and routes.",
        "chips": ["React Native", "Expo"],
        "links": [("GitHub", "https://github.com/gabwowce/travel-app-front")],
    },
    {
        "id": "convertclimb", "cat": "mobile", "img": "img/124.webp",
        "title": "ConvertClimb — React Native (Expo)",
        "year": "2025",
        "desc": "Nišinis įrankis laipiotojams: akimirksniu konvertuoja "
                "sudėtingumo laipsnius tarp skirtingų šalių sistemų. Veikia "
                "be interneto ryšio."
                "|A niche tool for climbers: instantly converts grades "
                "between different national systems. Works fully offline.",
        "chips": ["React Native", "Expo"],
        "links": [("GitHub", "https://github.com/gabwowce/ConvertClimb")],
    },
]


def pick(v, lang):
    if v is None:
        return None
    return v.split("|")[0 if lang == "lt" else -1] if "|" in v else v


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


SHARE = '''              <div class="share share--overlay u-reveal" data-share>
                <a class="share-btn" data-network="facebook" target="_blank" rel="noopener" aria-label="Share on Facebook" title="Facebook">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 22v-8h3l1-4h-4V7.5c0-1 .3-1.5 1.7-1.5H17V2.2c-.4-.1-1.7-.2-3.2-.2C10.9 2 9 3.7 9 7v3H6v4h3v8h4z"/></svg>
                </a>
                <a class="share-btn" data-network="x" target="_blank" rel="noopener" aria-label="Share on X" title="X">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.8l-5.3-6.5L5.3 22H2l7.3-8.4L1 2h6.9l4.8 5.8L18.9 2zm-1.2 18h1.7L6.2 3.9H4.4L17.7 20z"/></svg>
                </a>
                <a class="share-btn" data-network="linkedin" target="_blank" rel="noopener" aria-label="Share on LinkedIn" title="LinkedIn">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1 4.98 2.12 4.98 3.5zM0 22h5V7H0v15zM8 7h4.8v2.1h.1C13.6 7.8 15 6.7 17.4 6.7 22.4 6.7 23 10 23 14.3V22h-5v-6.7c0-1.6 0-3.6-2.2-3.6s-2.6 1.7-2.6 3.5V22H8V7z"/></svg>
                </a>
              </div>
'''


def gallery_json(shots, lang):
    """shots: list of (base_path_no_ext, alt) -> JSON for data-gallery."""
    import json
    return json.dumps([
        {"src": f"../{base}-1400.webp", "alt": pick(alt, lang)}
        for base, alt in shots
    ])


def featured_html(lang):
    d = FEATURED[lang]
    base, w, h, alt = FEATURED_IMG
    shots = [(base, alt), (FEATURED_GALLERY_EXTRA[0], FEATURED_GALLERY_EXTRA[2])]
    gallery_attr = esc(gallery_json(shots, lang)).replace("'", "&#39;")
    nodes = "\n".join(
        f'                    <li class="stack-node{" stack-node--ai" if k=="ai" else ""}">'
        f'{esc(label)}{f"<small>{esc(pick(sub, lang))}</small>" if sub else ""}</li>'
        for label, sub, k in FEATURED_NODES)
    facts = "\n".join(f'                <li><strong>{esc(v)}</strong> {esc(l)}</li>'
                      for v, l in d["facts"])
    return f'''<article class="project project-xl project--sys project--split project--featured u-stagger" id="{FEATURED_ID}" data-cat="web">
            <div class="proj-visual u-reveal">
              <div class="mock" data-gallery='{gallery_attr}'>
                <div class="mock__bar" aria-hidden="true">
                  <span class="mock__dot"></span><span class="mock__dot"></span><span class="mock__dot"></span>
                  <span class="mock__addr"></span>
                </div>
                <img
                  src="../{base}-1400.webp"
                  srcset="../{base}-700.webp 700w, ../{base}-1400.webp 1400w"
                  sizes="(max-width: 899px) 100vw, 560px"
                  alt="{esc(pick(alt, lang))}"
                  width="{w}" height="{h}" loading="eager" decoding="async" fetchpriority="high"
                />
                <span class="thumb-count">1 / {len(shots)}</span>
              </div>
            </div>
            <div class="meta u-reveal u-stagger">
              <span class="project-eyebrow">{d["eyebrow"]}</span>
              <h3 class="u-reveal">{d["title"]}</h3>
              <p class="sub u-reveal">{d["sub"]}</p>
{SHARE}              <p class="desc u-reveal"><strong class="proj-aspect">{d["hard_label"]}.</strong> {d["hard"]}</p>
              <p class="desc u-reveal"><strong class="proj-aspect">{d["role_label"]}.</strong> {d["role"]}</p>
              <ul class="stack-flow u-reveal">
{nodes}
              </ul>
              <ul class="stack-facts u-reveal">
{facts}
              </ul>
              <a class="btn-pill project-cta u-reveal" href="#{FEATURED_ID}">{d["cta"]} →</a>
            </div>
          </article>
'''


def grid_card_html(item, lang):
    title = pick(item["title"], lang)
    desc = pick(item["desc"], lang)
    badge = item.get("badge")
    links = item.get("links") or []
    link_html = "\n".join(
        f'                <a class="grid-card__link" href="{url}" target="_blank" rel="noopener">{pick(label, lang)} ↗</a>'
        for label, url in links)
    chips = "".join(f'<li>{esc(c)}</li>' for c in item["chips"])

    gallery = item.get("gallery")
    if gallery:
        gallery_attr = esc(gallery_json(gallery, lang)).replace("'", "&#39;")
        thumb_attrs = f" data-gallery='{gallery_attr}'"
        count_html = (f'\n              <span class="thumb-count">1 / {len(gallery)}</span>'
                     if len(gallery) > 1 else '')
    else:
        thumb_attrs = ""
        count_html = ""

    return f'''<article class="project project--grid u-stagger" id="{item["id"]}" data-cat="{item["cat"]}">
            <div class="grid-card__thumb u-reveal"{thumb_attrs}>
              <img src="../{item["img"]}" alt="{esc(title)}" loading="lazy" decoding="async" />{count_html}
            </div>
            <div class="grid-card__body u-reveal">
              <div class="grid-card__top">
                <h3 class="grid-card__title">{title}</h3>
                <span class="grid-card__year">{item["year"]}</span>
              </div>
              {f'<span class="stack-badge">{pick(badge, lang)}</span>' if badge else ''}
              <p class="grid-card__desc">{desc}</p>
              <ul class="tags grid-card__tags">{chips}</ul>
              <div class="grid-card__links">
{link_html}
              </div>
            </div>
          </article>
'''


def main():
    for lang in ("lt", "en"):
        path = ROOT / lang / "portfolio.html"
        s = path.read_text()
        start = s.index('<div class="featured-grid')
        start = s.index(">", start) + 1
        end = s.rindex("</div>", 0, s.index("</section>", start))
        # walk back to find the matching close of featured-grid (last </div>
        # before </section>, since it is the outermost one in that range)
        lg_items = [it for it in GRID if it.get("tier") == "lg"]
        small_items = [it for it in GRID if it.get("tier") != "lg"]

        body = featured_html(lang)
        body += '\n          <div class="portfolio-grid--lg">\n'
        for item in lg_items:
            body += grid_card_html(item, lang)
        body += '          </div>\n'
        body += '          <div class="portfolio-grid">\n'
        for item in small_items:
            body += grid_card_html(item, lang)
        body += '          </div>\n'

        s = s[:start] + "\n" + body + "        " + s[end:]
        path.write_text(s)
        print(f"{lang}/portfolio.html: 1 featured + {len(lg_items)} large "
              f"+ {len(small_items)} grid cards")


if __name__ == "__main__":
    main()
