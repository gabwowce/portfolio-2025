#!/usr/bin/env python3
"""
Write the resources page body - tracks and their steps - in both locales.

A flat grid of resource cards reads as "here are three things I happened to
write". A track reads as "here is the path, and here is where you are on
it": someone landing on step 3 can see what comes before and after, and
someone landing on an empty step can see the shape of what is coming.

So the page is a small number of ordered tracks, each a numbered list of
steps. A step is either published (links out) or not yet (says so plainly).
Unpublished steps stay listed on purpose - the sequence is the point, and
hiding the gaps would make the track look shorter than it is.

Edit TRACKS below and run:  python3 tools/build-resources.py

Both files carry <!-- TRACKS:START --> / <!-- TRACKS:END --> markers; only
what is between them is rewritten.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

UI = {
    "lt": {
        "steps": "žingsnių",
        "ready": "paruošta",
        "read": "Skaityti",
        "soon": "Netrukus",
        "available": "Paruošta",
        "en_note": "anglų k.",
        "intro": "Resursai sudėlioti į nuoseklius takelius — eik iš eilės arba "
                 "šok į tą žingsnį, kurio tau trūksta. Tušti žingsniai palikti "
                 "matomi specialiai: taip matai visą kelią, ne tik tai, kas jau "
                 "parašyta.",
    },
    "en": {
        "steps": "steps",
        "ready": "ready",
        "read": "Read it",
        "soon": "Coming soon",
        "available": "Available",
        "en_note": "in English",
        "intro": "The resources are laid out as ordered tracks — follow one "
                 "through, or jump to the step you're missing. Empty steps are "
                 "listed on purpose: you see the whole path, not just the part "
                 "that's written.",
    },
}

# Each track: number, title, blurb, and its steps in order.
# A step's "href" being None means it is not published yet.
TRACKS = [
    {
        "id": "claude-code",
        "cat": "ai-dev",
        "tool": "Claude Code",
        "title": {"lt": "Claude Code nuo nulio",
                  "en": "Claude Code from scratch"},
        "blurb": {
            "lt": "Nuo pirmo paleidimo iki to, kad agentas dirbtų tavo "
                  "projekte saugiai ir su tavo taisyklėmis. Eik iš eilės — "
                  "kiekvienas žingsnis remiasi ankstesniu.",
            "en": "From the first launch to an agent working inside your "
                  "project safely and on your rules. Go in order — each step "
                  "builds on the one before it.",
        },
        "steps": [
            {
                "title": {"lt": "Kas yra Claude Code ir kaip jį paleisti",
                          "en": "What Claude Code is, and getting it running"},
                "desc": {"lt": "Kuo agentas terminale skiriasi nuo pokalbio "
                               "naršyklėje, ir ką jis gali pasiekti tavo kompiuteryje.",
                         "en": "How an agent in your terminal differs from a chat "
                               "in a browser, and what it can reach on your machine."},
                "href": None,
            },
            {
                "title": {"lt": "Projektas, kontekstas ir CLAUDE.md",
                          "en": "Project, context and CLAUDE.md"},
                "desc": {"lt": "Ką agentas turi žinoti apie tavo kodą, kad "
                               "nustotų spėlioti — ir kaip tai surašyti vieną kartą.",
                         "en": "What the agent needs to know about your codebase to "
                               "stop guessing — and how to write it down once."},
                "href": None,
            },
            {
                "title": {"lt": "Saugikliai: kad agentas nesugriautų projekto",
                          "en": "Guardrails: stopping the agent before it breaks things"},
                "desc": {"lt": "Paruoštas <code>.claude/settings.json</code> su penkiais "
                               "saugikliais ir <code>guard.sh</code> skriptu — su paaiškinimu, "
                               "ką kiekvienas realiai blokuoja.",
                         "en": "A ready <code>.claude/settings.json</code> with five safety "
                               "hooks plus a <code>guard.sh</code> script — with a plain-language "
                               "explanation of what each one actually blocks."},
                "href": "/en/resources/claude-code-guardrails.html",
                "href_lang": "en",
            },
            {
                "title": {"lt": "Hooks giliau: kada „ask“, kaip juos testuoti",
                          "en": "Hooks in depth: when to ask, how to test them"},
                "desc": {"lt": "Kai blokuoti per griežta, o praleisti per rizikinga — "
                               "trečias kelias ir kaip patikrinti, kad veikia.",
                         "en": "When blocking is too strict and allowing is too risky — "
                               "the third option, and how to prove it works."},
                "href": None,
            },
            {
                "title": {"lt": "Savos komandos ir skills",
                          "en": "Your own commands and skills"},
                "desc": {"lt": "Kaip pasidaryti, kad pasikartojantis darbas būtų "
                               "viena komanda, o ne tas pats promptas kas kartą.",
                         "en": "Turning repeated work into one command instead of "
                               "retyping the same prompt every time."},
                "href": None,
            },
            {
                "title": {"lt": "MCP: kaip prijungti savo įrankius",
                          "en": "MCP: wiring in your own tools"},
                "desc": {"lt": "Kad agentas pasiektų tavo duomenų bazę, API ar "
                               "vidinę sistemą — ir tik tiek, kiek leidi.",
                         "en": "Letting the agent reach your database, API or internal "
                               "system — and only as far as you allow."},
                "href": None,
            },
        ],
    },
    {
        "id": "start",
        "cat": "learning",
        "tool": {"lt": "Bet koks AI įrankis", "en": "Any AI tool"},
        "title": {"lt": "Kaip pradėti programuoti dabar",
                  "en": "How to start coding now"},
        "blurb": {
            "lt": "Kelias pradedančiajam tuo metu, kai AI rašo pusę kodo už tave. "
                  "Ne „išmok sintaksę“, o kaip išmokti taip, kad po metų dar "
                  "mokėtum pats.",
            "en": "A beginner's path at a time when AI writes half the code for "
                  "you. Not \"learn the syntax\", but how to learn so that you "
                  "still know it yourself a year from now.",
        },
        "steps": [
            {
                "title": {"lt": "Nuo ko pradėti — ir ko negalima praleisti",
                          "en": "Where to start — and what you can't skip"},
                "desc": {"lt": "Kas pasikeitė per pastaruosius dvejus metus, o kas "
                               "liko lygiai toks pat.",
                         "en": "What changed in the last two years, and what stayed "
                               "exactly the same."},
                "href": None,
            },
            {
                "title": {"lt": "Aplinka: redaktorius, terminalas, Git",
                          "en": "Your setup: editor, terminal, Git"},
                "desc": {"lt": "Minimalus rinkinys, kurio užtenka pirmam pusmečiui, "
                               "be papildomo triukšmo.",
                         "en": "The minimum kit that covers your first six months, "
                               "without the extra noise."},
                "href": None,
            },
            {
                "title": {"lt": "Pirmas projektas nuo nulio iki gyvo",
                          "en": "A first project, from empty folder to live"},
                "desc": {"lt": "Mažas, bet pilnas: nuo tuščio aplanko iki nuorodos, "
                               "kurią gali kam nors nusiųsti.",
                         "en": "Small but complete: from an empty folder to a link "
                               "you can send someone."},
                "href": None,
            },
            {
                "title": {"lt": "Vibe coding žemėlapis: kur AI padeda, kur kenkia",
                          "en": "The vibe coding map: where AI helps, where it hurts"},
                "desc": {"lt": "Kur programavimas su AI tikrai pagreitina darbą, o kur "
                               "tyliai susikuria netvarka, už kurią sumokėsi vėliau.",
                         "en": "Where AI-assisted coding genuinely speeds you up, and "
                               "where it quietly creates a mess you'll pay for later."},
                "href": None,
            },
            {
                "title": {"lt": "Portfolio, kuris ką nors reiškia",
                          "en": "A portfolio that means something"},
                "desc": {"lt": "Kodėl trys tutorial'ų klonai nieko nesako, ir ką rodyti "
                               "vietoj jų.",
                         "en": "Why three tutorial clones say nothing, and what to show "
                               "instead."},
                "href": None,
            },
        ],
    },
]


def pick(v, lang):
    return v[lang] if isinstance(v, dict) else v


def esc(s):
    return s.replace("&", "&amp;")


def render(lang):
    u = UI[lang]
    out = [f'      <p class="resources-intro u-reveal">{u["intro"]}</p>', ""]
    for n, tr in enumerate(TRACKS, 1):
        steps = tr["steps"]
        ready = sum(1 for s in steps if s["href"])
        out += [
            f'      <section class="track u-reveal" id="track-{tr["id"]}" data-cat="{tr["cat"]}">',
            f'        <header class="track__head">',
            f'          <span class="track__num" aria-hidden="true">{n:02d}</span>',
            f'          <div class="track__headtext">',
            f'            <h2 class="track__title">{esc(pick(tr["title"], lang))}</h2>',
            f'            <p class="track__blurb">{esc(pick(tr["blurb"], lang))}</p>',
            f'            <p class="track__meta">',
            f'              <span class="resource-card__tool{" tool--claude" if tr["tool"] == "Claude Code" else ""}">{esc(pick(tr["tool"], lang))}</span>',
            f'              <span>{len(steps)} {u["steps"]} · {ready} {u["ready"]}</span>',
            f'            </p>',
            f'          </div>',
            f'        </header>',
            f'        <ol class="track-steps">',
        ]
        for i, s in enumerate(steps, 1):
            done = " is-ready" if s["href"] else ""
            out += [
                f'          <li class="track-step{done}">',
                f'            <span class="track-step__n" aria-hidden="true">{i}</span>',
                f'            <div class="track-step__body">',
                f'              <h3 class="track-step__title">{esc(pick(s["title"], lang))}</h3>',
                f'              <p class="track-step__desc">{pick(s["desc"], lang)}</p>',
            ]
            if s["href"]:
                hl = s.get("href_lang")
                note = f' <span class="track-step__note">({u["en_note"]})</span>' if hl and hl != lang else ""
                attr = f' hreflang="{hl}"' if hl else ""
                out.append(
                    f'              <a class="link-ghost" href="{s["href"]}"{attr}>{u["read"]} →</a>{note}')
            else:
                out.append(
                    f'              <span class="track-step__soon">{u["soon"]}</span>')
            out += ['            </div>', '          </li>']
        out += ['        </ol>', '      </section>', '']
    return "\n".join(out)


def main():
    for lang in ("lt", "en"):
        path = ROOT / lang / "resources.html"
        s = path.read_text()
        block = f"<!-- TRACKS:START -->\n{render(lang)}      <!-- TRACKS:END -->"
        new, n = re.subn(r'<!-- TRACKS:START -->.*?<!-- TRACKS:END -->',
                         lambda _: block, s, flags=re.S)
        if not n:
            raise SystemExit(f"{lang}/resources.html: no TRACKS markers found")
        path.write_text(new)
        print(f"{lang}/resources.html: {len(TRACKS)} tracks, "
              f"{sum(len(t['steps']) for t in TRACKS)} steps")


if __name__ == "__main__":
    main()
