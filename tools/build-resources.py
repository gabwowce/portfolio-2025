#!/usr/bin/env python3
"""
Build the resources section: an index of courses, and a page per course.

A long numbered list on one page stops working as soon as a track has more
than a handful of steps - and these tracks will. So the shape is the one
every course site converged on for good reason: the index is a shelf of
course cards, and opening one gives you the curriculum on the left and the
selected lesson on the right, with its resources attached to it.

That split matters. The curriculum answers "what is this course and how far
does it go" at a glance, without scrolling through prose. The right pane
answers "what is in this particular lesson" only when asked. A step that
isn't written yet still appears in the curriculum - the sequence is the
product, and hiding the gaps would make each course look shorter than it is.

Run:  python3 tools/build-resources.py

Writes, for each locale:
  <lang>/resources.html                  - the shelf (between TRACKS markers)
  <lang>/resources/<track-id>.html       - one course page per track

Course pages are built from that locale's resources.html as a shell, so the
header, footer and theme script stay in sync with the rest of the site
automatically - there is no second copy of the chrome to keep updated.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent

UI = {
    "lt": {
        "steps": "žingsniai",
        "ready": "paruošta",
        "read": "Atidaryti resursą",
        "soon": "Netrukus",
        "open": "Peržiūrėti kursą",
        "curriculum": "Turinys",
        "back": "Visi kursai",
        "lesson": "Žingsnis",
        "en_note": "anglų k.",
        "no_res": "Šiam žingsniui resurso dar nėra. Kai parašysiu, jis atsiras "
                  "čia — o žingsnis lieka sąraše, kad matytum visą kelią.",
        "res_head": "Resursai",
        "intro": "Ne atsitiktinės kortelės, o kursai. Kiekvienas eina iš eilės "
                 "nuo pradžios iki galo — atsidaryk ir pamatysi visą turinį, "
                 "net tas dalis, kurių dar neparašiau.",
        "title": "Resursai",
    },
    "en": {
        "steps": "steps",
        "ready": "ready",
        "read": "Open the resource",
        "soon": "Coming soon",
        "open": "View the course",
        "curriculum": "Curriculum",
        "back": "All courses",
        "lesson": "Step",
        "en_note": "in English",
        "no_res": "There is no resource for this step yet. When I write it, it "
                  "appears here — the step stays listed so you can see the "
                  "whole path.",
        "res_head": "Resources",
        "intro": "Not a pile of cards — courses. Each one runs in order from "
                 "start to finish. Open one and you see the whole curriculum, "
                 "including the parts I haven't written yet.",
        "title": "Resources",
    },
}

TRACKS = [
    {
        "id": "claude-code",
        "tool": "Claude Code",
        "title": {"lt": "Claude Code nuo nulio",
                  "en": "Claude Code from scratch"},
        "blurb": {
            "lt": "Nuo pirmo paleidimo iki to, kad agentas dirbtų tavo "
                  "projekte saugiai ir su tavo taisyklėmis. Kiekvienas "
                  "žingsnis remiasi ankstesniu.",
            "en": "From the first launch to an agent working inside your "
                  "project safely and on your rules. Each step builds on the "
                  "one before it.",
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
                "res": {"lt": "Claude Code Guardrails", "en": "Claude Code Guardrails"},
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
        "id": "start-coding",
        "tool": {"lt": "Bet koks AI įrankis", "en": "Any AI tool"},
        "title": {"lt": "Kaip pradėti programuoti dabar",
                  "en": "How to start coding now"},
        "blurb": {
            "lt": "Kelias pradedančiajam tuo metu, kai AI rašo pusę kodo už "
                  "tave. Ne „išmok sintaksę“, o kaip mokytis taip, kad po metų "
                  "dar mokėtum pats.",
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


def e(s):
    return html.escape(s, quote=False)


def ready_count(tr):
    return sum(1 for s in tr["steps"] if s["href"])


# --------------------------------------------------------------------------
# The shelf: one card per course, on <lang>/resources.html
# --------------------------------------------------------------------------

def shelf(lang):
    u = UI[lang]
    out = [f'      <p class="resources-intro u-reveal">{u["intro"]}</p>', "",
           '      <div class="course-grid u-stagger">']
    for n, tr in enumerate(TRACKS, 1):
        total, ready = len(tr["steps"]), ready_count(tr)
        pct = round(ready / total * 100)
        tool = pick(tr["tool"], lang)
        tool_cls = " tool--claude" if tr["tool"] == "Claude Code" else ""
        href = f'/{lang}/resources/{tr["id"]}.html'
        out += [
            f'        <a class="course-card u-reveal" href="{href}">',
            f'          <span class="course-card__num" aria-hidden="true">{n:02d}</span>',
            f'          <h2 class="course-card__title">{e(pick(tr["title"], lang))}</h2>',
            f'          <p class="course-card__blurb">{e(pick(tr["blurb"], lang))}</p>',
            f'          <span class="resource-card__tool{tool_cls}">{e(tool)}</span>',
            f'          <div class="course-card__foot">',
            f'            <div class="course-bar" role="img"'
            f' aria-label="{ready}/{total} {u["ready"]}">',
            f'              <span style="width:{pct}%"></span>',
            f'            </div>',
            f'            <span class="course-card__meta">{total} {u["steps"]}'
            f' · {ready} {u["ready"]}</span>',
            f'          </div>',
            f'          <span class="course-card__cta">{u["open"]} →</span>',
            f'        </a>',
        ]
    out += ['      </div>']
    return "\n".join(out)


# --------------------------------------------------------------------------
# A course page: curriculum on the left, the selected step on the right
# --------------------------------------------------------------------------

def course_main(tr, n, lang):
    u = UI[lang]
    steps = tr["steps"]
    total, ready = len(steps), ready_count(steps and tr)
    tool = pick(tr["tool"], lang)
    tool_cls = " tool--claude" if tr["tool"] == "Claude Code" else ""

    nav = []
    panels = []
    for i, s in enumerate(steps, 1):
        sel = "true" if i == 1 else "false"
        done = " is-ready" if s["href"] else ""
        nav += [
            f'            <li>',
            f'              <button class="lesson-link{done}" role="tab"'
            f' id="tab-{i}" aria-controls="panel-{i}" aria-selected="{sel}"'
            f' data-step="{i}">',
            f'                <span class="lesson-link__n" aria-hidden="true">{i}</span>',
            f'                <span class="lesson-link__t">{e(pick(s["title"], lang))}</span>',
            f'              </button>',
            f'            </li>',
        ]
        # Resources attached to this step - the right-hand side of the pane.
        if s["href"]:
            hl = s.get("href_lang")
            note = (f' <span class="lesson-res__note">({u["en_note"]})</span>'
                    if hl and hl != lang else "")
            attr = f' hreflang="{hl}"' if hl else ""
            res = [
                f'                <h3 class="lesson-panel__reshead">{u["res_head"]}</h3>',
                f'                <a class="lesson-res" href="{s["href"]}"{attr}>',
                f'                  <span class="lesson-res__name">'
                f'{e(pick(s.get("res", s["title"]), lang))}</span>{note}',
                f'                  <span class="lesson-res__cta">{u["read"]} →</span>',
                f'                </a>',
            ]
        else:
            res = [
                f'                <p class="lesson-panel__empty">'
                f'<span class="track-step__soon">{u["soon"]}</span></p>',
                f'                <p class="lesson-panel__emptynote">{u["no_res"]}</p>',
            ]
        panels += [
            f'          <article class="lesson-panel" role="tabpanel" id="panel-{i}"'
            f' aria-labelledby="tab-{i}"{"" if i == 1 else " hidden"}>',
            f'            <p class="lesson-panel__kicker">{u["lesson"]} {i} / {total}</p>',
            f'            <h2 class="lesson-panel__title">{e(pick(s["title"], lang))}</h2>',
            f'            <p class="lesson-panel__desc">{pick(s["desc"], lang)}</p>',
            f'            <div class="lesson-panel__res">',
            *res,
            f'            </div>',
            f'          </article>',
        ]

    return "\n".join([
        '    <main class="content content--single content--course container">',
        f'      <a class="course-back" href="/{lang}/resources.html">← {u["back"]}</a>',
        '',
        '      <header class="course-head u-reveal">',
        f'        <span class="course-head__num" aria-hidden="true">{n:02d}</span>',
        '        <div>',
        f'          <h1 class="course-head__title">{e(pick(tr["title"], lang))}</h1>',
        f'          <p class="course-head__blurb">{e(pick(tr["blurb"], lang))}</p>',
        '          <p class="track__meta">',
        f'            <span class="resource-card__tool{tool_cls}">{e(tool)}</span>',
        f'            <span>{total} {u["steps"]} · {ready} {u["ready"]}</span>',
        '          </p>',
        '        </div>',
        '      </header>',
        '',
        '      <div class="course-layout u-reveal" data-course>',
        '        <nav class="course-curriculum" aria-label="'
        + u["curriculum"] + '">',
        f'          <h2 class="course-curriculum__head">{u["curriculum"]}</h2>',
        '          <ol class="lesson-list" role="tablist"'
        f' aria-label="{u["curriculum"]}">',
        *nav,
        '          </ol>',
        '        </nav>',
        '',
        '        <div class="course-detail">',
        *panels,
        '        </div>',
        '      </div>',
        '    </main>',
    ])


COURSE_JS = """
    <script>
      /*
        Curriculum -> detail. Progressive enhancement: without JS every panel
        is visible and the page is still a readable curriculum, so the script
        only ever hides things once it is running.
      */
      (function () {
        var root = document.querySelector("[data-course]");
        if (!root) return;
        root.classList.add("is-enhanced");
        var tabs = root.querySelectorAll(".lesson-link");
        var panels = root.querySelectorAll(".lesson-panel");
        function show(n) {
          tabs.forEach(function (t) {
            t.setAttribute("aria-selected", t.dataset.step === n);
          });
          panels.forEach(function (p) {
            p.hidden = p.id !== "panel-" + n;
          });
        }
        tabs.forEach(function (t) {
          t.addEventListener("click", function () { show(t.dataset.step); });
          t.addEventListener("keydown", function (ev) {
            var d = ev.key === "ArrowDown" ? 1 : ev.key === "ArrowUp" ? -1 : 0;
            if (!d) return;
            ev.preventDefault();
            var list = Array.prototype.slice.call(tabs);
            var next = list[(list.indexOf(t) + d + list.length) % list.length];
            next.focus();
            show(next.dataset.step);
          });
        });
      })();
    </script>
"""


def build_course_page(tr, n, lang, shell):
    """Reuse the locale's resources.html for header, footer and head."""
    u = UI[lang]
    title = pick(tr["title"], lang)
    url = f"https://codeart.lt/{lang}/resources/{tr['id']}.html"
    s = shell

    # This page lives one directory deeper, so every ../ asset path and every
    # bare relative nav link has to be re-rooted. Absolute paths are used
    # rather than ../../ so the depth stops mattering.
    s = s.replace('="../', '="/')
    s = re.sub(r'href="(?!https?:|/|#|mailto:)([\w-]+\.html)"',
               rf'href="/{lang}/\1"', s)

    s = re.sub(r'<title>.*?</title>',
               f'<title>{e(title)} | {u["title"]} — Gabrielė</title>', s,
               flags=re.S)
    s = re.sub(r'<link rel="canonical" href="[^"]*"',
               f'<link rel="canonical" href="{url}"', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*"',
               f'<meta property="og:url" content="{url}"', s)
    s = re.sub(r'(<meta name="description"\s+content=")[^"]*',
               rf'\1{e(pick(tr["blurb"], lang))}', s, flags=re.S)
    # hreflang pairs point at this course, not at the index
    s = re.sub(r'<link rel="alternate" hreflang="(lt|en|x-default)" href="[^"]*" />',
               lambda m: '<link rel="alternate" hreflang="%s" href="https://codeart.lt/%s/resources/%s.html" />'
               % (m.group(1),
                  "en" if m.group(1) in ("en", "x-default") else "lt",
                  tr["id"]), s)
    s = re.sub(r'(<a\s+id="langSwitch"[^>]*href=")[^"]*',
               rf'\1/{"en" if lang == "lt" else "lt"}/resources/{tr["id"]}.html', s)

    # swap hero + main for the course body
    hero_start = s.index('<!-- HERO -->')
    main_end = s.index('</main>') + len('</main>')
    s = s[:hero_start] + course_main(tr, n, lang) + s[main_end:]
    s = s.replace('</body>', COURSE_JS + '  </body>')
    return s


def main():
    for lang in ("lt", "en"):
        index = ROOT / lang / "resources.html"
        s = index.read_text()
        block = f"<!-- TRACKS:START -->\n{shelf(lang)}\n      <!-- TRACKS:END -->"
        s, n = re.subn(r'<!-- TRACKS:START -->.*?<!-- TRACKS:END -->',
                       lambda _: block, s, flags=re.S)
        if not n:
            raise SystemExit(f"{lang}/resources.html: no TRACKS markers")
        index.write_text(s)

        outdir = ROOT / lang / "resources"
        outdir.mkdir(exist_ok=True)
        for i, tr in enumerate(TRACKS, 1):
            page = build_course_page(tr, i, lang, s)
            (outdir / f"{tr['id']}.html").write_text(page)
        print(f"{lang}: shelf + {len(TRACKS)} course pages "
              f"({', '.join(t['id'] for t in TRACKS)})")


if __name__ == "__main__":
    main()
