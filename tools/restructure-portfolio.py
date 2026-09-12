#!/usr/bin/env python3
"""
One-off: restructure the portfolio grid in both locales.

Removes the two projects the owner pulled (carestudio, codeart), adds the
two she added (the loyalty backoffice and TikMaker), and reorders what is
left so the four systems she actually spent time on lead the page.

The two new cards are written here rather than by hand because they have to
exist twice, in two languages, with identical markup - and the share block
each card carries is ~60 lines of SVG that is not worth duplicating by eye.
It lifts that block from an existing card instead.

Idempotent: re-running replaces the generated cards and re-sorts.

Confidentiality note: the loyalty backoffice card carries NO screenshot and
NO client name, product name, internal service name or internal field name.
The screenshots in img/ac/ show a real cardholder's name, two phone numbers,
card numbers and the client's branding, and are never published.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

ORDER = [
    "loyalty-backoffice",
    "keepmi",
    "kidcan",
    "kibinai",
    "tikmaker",
    "ltsa",
    "autorent",
    "travel-app",
    "convertclimb",
]
DROP = ["carestudio", "codeart"]


# --------------------------------------------------------------------------
# The two new cards.
# --------------------------------------------------------------------------

SYS = {
    "lt": {
        "title": "Lojalumo valdymo sistema — B2B backoffice",
        "sub": "Web · klientinis projektas · ekranai nerodomi",
        "domains": ["Kortelės", "Klientai", "Lojalumas", "Transakcijos",
                    "Dashboard", "Konfigūracija", "Nustatymai", "Audito žurnalas"],
        "locked": "Klientinė sistema — ekranai nerodomi",
        "desc": """Kasdien naudojama vidinė sistema: lojalumo kortelės, kortelių
              turėtojai, organizacijos ir transakcijos. Naudotojai — įmonės
              darbuotojai, ne galutiniai klientai, todėl viskas sukasi apie
              teises, auditą ir duomenų tikslumą.""",
        "hard_label": "Sunkiausia dalis",
        "hard": """Ne sąsaja, o duomenų ir logikos nuoseklumas su gyvu,
              nuolat besikeičiančiu backend'u. API tipai generuojami iš backend'o
              schemos, tad kiekvienas jos pakeitimas turi būti persinchronizuotas
              prieš tai, kai jį pastebi naudotojas. Masiniai kortelių veiksmai turi
              du visiškai skirtingus kelius, kuriuos abu reikia palaikyti vienodai.
              Daugiapakopės formos su dinaminiais laukais atvedė prie „stale
              closure“ validacijos klaidų. O akcijų migracija iš senos sistemos su
              prioritetų logika reikalavo duomenų perkėlimo dar prieš perjungiant.""",
        "role_label": "Mano vaidmuo",
        "role": """Ne tik frontend'as. Formuluoju užduotis backend'o kolegai,
              derinu API kontraktus ir prižiūriu projektą kaip visumą — o patį
              pradžios etapą, kol prisijungė backend'o žmogus, dariau viena.""",
    },
    "en": {
        "title": "Loyalty management system — B2B backoffice",
        "sub": "Web · client project · screens not shown",
        "domains": ["Cards", "Clients", "Loyalty", "Transactions",
                    "Dashboard", "Configuration", "Settings", "Audit log"],
        "locked": "Client system — screens not shown",
        "desc": """An internal system in daily use: loyalty cards, cardholders,
              organisations and transactions. Its users are the company's own
              staff, not end customers, so everything turns on permissions,
              auditability and data accuracy.""",
        "hard_label": "The hard part",
        "hard": """Not the interface — keeping data and logic consistent with a
              live backend that keeps changing. API types are generated from the
              backend schema, so every schema change has to be re-synced before a
              user runs into it. Bulk card actions have two completely different
              paths that both need equal support. Multi-step forms with dynamic
              fields produced stale-closure validation bugs. And migrating
              promotions off the old system, with its priority rules, meant
              backfilling the data before anything could be switched over.""",
        "role_label": "My role",
        "role": """Not just the frontend. I scope and hand off work to the backend
              developer, agree the API contracts and steer the project as a whole —
              and I built the early stage alone, before a backend developer
              joined.""",
    },
}

SYS_FACTS = {
    "lt": [("~27", "maršrutų"), ("8", "sričių"), ("2 × ~2200", "vertimo raktų"),
           ("Rolės", "ir teisės"), ("Audito", "žurnalas")],
    "en": [("~27", "routes"), ("8", "domains"), ("2 × ~2200", "translation keys"),
           ("Roles", "and permissions"), ("Audit", "log")],
}

TIK = {
    "lt": {
        "title": "TikMaker — vaizdo redaktorius su AI įgarsinimu",
        "sub": "Web · vidinis įrankis · 2026",
        "alt": "TikMaker — scenų timeline, inspektorius ir peržiūra",
        "desc": """Įrankis, kurį pasidariau savo TikTok / Reels / Shorts turiniui:
              scenų storyboard, timeline su atskirais teksto, vizualų ir garso
              takeliais, ir tikras renderis į MP4 — ne mockup'as, projektai
              eksportuojami realiais failais.""",
        "hard_label": "Kur čia AI",
        "hard": """ElevenLabs text-to-speech (multilingual modelis, veikia ir
              lietuviškai) pajungtas per savo serverio pusės endpoint'ą, kad API
              raktas liktų serveryje ir niekada nepasiektų naršyklės. Svarbiausias
              sprendimas — sugeneruotas balso takelis įrašomas į tą patį garsų
              manifestą kaip ir visi kiti efektai. Todėl jis automatiškai gauna
              timeline eilutę, bangos formą, trim/split ir garsumo valdymą; jokio
              atskiro „balso“ pipeline'o palaikyti nereikia.""",
        "role_label": "Sąžiningai",
        "role": """Tai vidinis darbo įrankis, kurį naudoju pati — ne parduodamas
              produktas. Rodau jį todėl, kad jame matosi, kaip AI paslauga
              pajungiama prie realaus produkto: raktas serveryje, rezultatas
              integruotas į esamą duomenų modelį, o ne prilipdytas iš šono.""",
    },
    "en": {
        "title": "TikMaker — video editor with AI voiceover",
        "sub": "Web · internal tool · 2026",
        "alt": "TikMaker — scene timeline, inspector and preview",
        "desc": """A tool I built for my own TikTok / Reels / Shorts content:
              a scene storyboard, a timeline with separate text, visual and audio
              tracks, and a real render to MP4 — not a mockup, projects export as
              actual files.""",
        "hard_label": "Where the AI is",
        "hard": """ElevenLabs text-to-speech (the multilingual model, which handles
              Lithuanian) is wired in through a server-side endpoint of my own, so
              the API key stays on the server and never reaches the browser. The
              decision that mattered: the generated voice track is written into the
              same audio manifest as every other sound effect. So it automatically
              gets a timeline row, a waveform, trim/split and volume — there is no
              separate "voice" pipeline to maintain.""",
        "role_label": "Honestly",
        "role": """This is an internal tool I use myself, not a product for sale.
              I show it because it demonstrates how an AI service gets wired into a
              real product: key on the server, output folded into the existing data
              model rather than bolted on the side.""",
    },
}


def para(pid, block, share, lang, body):
    """Card body shared by both new projects."""
    d = body
    extra = f'''
              <p class="desc u-reveal">
                <strong class="proj-aspect">{d["hard_label"]}.</strong>
                {" ".join(d["hard"].split())}
              </p>
              <p class="desc u-reveal">
                <strong class="proj-aspect">{d["role_label"]}.</strong>
                {" ".join(d["role"].split())}
              </p>'''
    return extra


def sys_card(lang, share):
    d = SYS[lang]
    tiles = "\n".join(
        f'                  <li>{t}</li>' for t in d["domains"])
    facts = "\n".join(
        f'                <li><strong>{v}</strong> {l}</li>'
        for v, l in SYS_FACTS[lang])
    return f'''<article
            class="project project-xl project--sys u-stagger"
            id="loyalty-backoffice"
            data-cat="web"
          >
            <div class="sysmap u-reveal" role="img" aria-label="{d["locked"]}">
              <div class="sysmap__inner">
                <ul class="sysmap__domains">
{tiles}
                </ul>
                <p class="sysmap__note">{d["locked"]}</p>
              </div>
            </div>

            <div class="meta u-reveal u-stagger">
              <h3 class="u-reveal">{d["title"]}</h3>
              <p class="sub u-reveal">{d["sub"]}</p>
{share}
              <p class="desc u-reveal">{" ".join(d["desc"].split())}</p>
{para("loyalty-backoffice", None, share, lang, d)}
              <ul class="stack-facts u-reveal">
{facts}
              </ul>
            </div>
          </article>
'''


def tik_card(lang, share):
    d = TIK[lang]
    badge = "AI viduje" if lang == "lt" else "AI inside"
    return f'''<article
            class="project project-xl u-stagger"
            id="tikmaker"
            data-cat="web"
          >
            <div class="thumb u-reveal">
              <img
                src="../img/TikMaker/main-1400.webp"
                srcset="../img/TikMaker/main-700.webp 700w, ../img/TikMaker/main-1400.webp 1400w"
                sizes="(max-width: 768px) 100vw, 1100px"
                alt="{d["alt"]}"
                width="1400"
                height="812"
                loading="lazy"
                decoding="async"
                fetchpriority="low"
              />
            </div>

            <div class="meta u-reveal u-stagger">
              <h3 class="u-reveal">{d["title"]}</h3>
              <p class="sub u-reveal">
                {d["sub"]} · <span class="stack-badge">{badge}</span>
              </p>
{share}
              <p class="desc u-reveal">{" ".join(d["desc"].split())}</p>
{para("tikmaker", None, share, lang, d)}
            </div>
          </article>
'''


# --------------------------------------------------------------------------

ART = re.compile(r'[ \t]*<article[^>]*\bid="([-\w]+)"[^>]*>.*?</article>\n',
                 re.S)


def grid_span(s):
    """Return (start, end) of the content between the grid div and its close."""
    m = re.search(r'<div class="featured-grid[^"]*">\n', s)
    start = m.end()
    end = s.rindex("</article>\n") + len("</article>\n")
    return start, end


def main():
    for lang in ("lt", "en"):
        path = ROOT / lang / "portfolio.html"
        s = path.read_text()
        start, end = grid_span(s)
        body = s[start:end]

        cards = {m.group(1): m.group(0) for m in ART.finditer(body)}
        missing = [i for i in ORDER if i not in cards
                   and i not in ("loyalty-backoffice", "tikmaker")]
        if missing:
            raise SystemExit(f"{lang}: expected projects not found: {missing}")

        # Lift the share block from an existing card so the new ones match.
        share = re.search(r'[ \t]*<div class="share share--overlay[^"]*"[^>]*>.*?</div>\n',
                          cards["keepmi"], re.S).group(0).rstrip("\n")

        cards["loyalty-backoffice"] = sys_card(lang, share)
        cards["tikmaker"] = tik_card(lang, share)

        out = "\n".join(cards[i].rstrip("\n") for i in ORDER) + "\n"
        s = s[:start] + out + s[end:]
        path.write_text(s)
        dropped = [d for d in DROP if d in cards]
        print(f"{lang}/portfolio.html: {len(ORDER)} cards, dropped {dropped}")


if __name__ == "__main__":
    main()
