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
        "open": "Skaityti gidą",
        "curriculum": "Turinys",
        "back": "Visi gidai",
        "lesson": "Žingsnis",
        "en_note": "anglų k.",
        "no_res": "Šiam žingsniui resurso dar nėra. Kai parašysiu, jis atsiras "
                  "čia — o žingsnis lieka sąraše, kad matytum visą kelią.",
        "res_head": "Resursai",
        "intro": "Kiekvienas gidas eina iš eilės nuo pradžios iki galo. "
                 "Atsidaryk ir pamatysi visą turinį, net tas dalis, kurių dar "
                 "neparašiau.",
        "title": "Gidai",
    },
    "en": {
        "steps": "steps",
        "ready": "ready",
        "read": "Open the resource",
        "soon": "Coming soon",
        "open": "Read the guide",
        "curriculum": "Curriculum",
        "back": "All guides",
        "lesson": "Step",
        "en_note": "in English",
        "no_res": "There is no resource for this step yet. When I write it, it "
                  "appears here — the step stays listed so you can see the "
                  "whole path.",
        "res_head": "Resources",
        "intro": "Each guide runs in order from start to finish. Open one and "
                 "you see the whole thing, including the parts I haven't "
                 "written yet.",
        "title": "Guides",
    },
}

TRACKS = [
    {
        "id": "claude-code",
        "tool": "Claude Code",
        "tag": {"lt": "Claude Code • AI programavimas",
                "en": "Claude Code • AI coding"},
        "title": {"lt": "Claude Code gidas pradedantiesiems",
                  "en": "Claude Code: a beginner's guide"},
        "blurb": {
            "lt": "Išmok naudoti Claude Code nuo nulio: diegimas, projekto "
                  "paruošimas, CLAUDE.md, permissions, hooks ir saugus AI "
                  "darbas su realiu kodu.",
            "en": "Learn Claude Code from zero: install, setting up a project, "
                  "CLAUDE.md, permissions, hooks, and working safely with AI "
                  "on real code.",
        },
        "steps": [
            {
                "title": {"lt": "Kas yra Claude Code ir kaip jį paleisti",
                          "en": "What Claude Code is, and getting it running"},
                "desc": {"lt": "Ne pokalbis naršyklėje, o agentas tavo terminale: "
                               "jis pats mato failus, paleidžia komandas ir keičia kodą. "
                               "Nuo įdiegimo iki pirmos užduoties, ir ką jis realiai "
                               "pasiekia tavo kompiuteryje.",
                         "en": "Not a chat in a browser but an agent in your terminal: "
                               "it reads your files, runs commands and edits code itself. "
                               "From install to the first real task, and what it can "
                               "actually reach on your machine."},
                "href": None,
            },
            {
                "title": {"lt": "Projektas, kontekstas ir CLAUDE.md",
                          "en": "Project, context and CLAUDE.md"},
                "desc": {"lt": "Agentas spėlioja tol, kol jam nepasakai. CLAUDE.md "
                               "yra ta vieta, kur vieną kartą surašai savo struktūrą, "
                               "taisykles ir įpročius, ir nustoji kartoti tą patį "
                               "kiekviename prompte.",
                         "en": "The agent guesses until you tell it otherwise. "
                               "CLAUDE.md is where you write your structure, your rules "
                               "and your habits down once, and stop repeating yourself "
                               "in every prompt."},
                "href": None,
            },
            {
                "title": {"lt": "Saugikliai: kad agentas nesugriautų projekto",
                          "en": "Guardrails: stopping the agent before it breaks things"},
                "desc": {"lt": "Agentas, galintis paleisti bet kokią komandą, anksčiau "
                               "ar vėliau paleis tą, kurios nenorėjai. Paruoštas "
                               "<code>.claude/settings.json</code> su penkiais saugikliais ir "
                               "<code>guard.sh</code> skriptu, su paaiškinimu, ką kiekvienas "
                               "realiai blokuoja.",
                         "en": "An agent that can run any command will, sooner or later, run "
                               "the one you did not want. A ready <code>.claude/settings.json</code> "
                               "with five safeguards and a <code>guard.sh</code> script, with a "
                               "plain explanation of what each one actually blocks."},
                "content_from": "en/resources/claude-code-guardrails.html",
                "content_lang": "en",
            },
            {
                "title": {"lt": "Hooks giliau: gyvenimo ciklas ir anatomija",
                          "en": "Hooks in depth: the lifecycle and the anatomy"},
                "desc": {"lt": "Instrukcijos sako, ką agentas turėtų daryti. Hooks "
                               "leidžia tavo sistemai reaguoti į tai, ką jis iš tikrųjų daro. "
                               "Kur jie įsiterpia, iš ko sudarytas vienas hook ir kaip atrodo "
                               "tas, kuris pasako „ne“, su interaktyviu pavyzdžiu.",
                         "en": "Instructions tell the agent what it should do. Hooks let "
                               "your system react to what it actually does. Where they sit in "
                               "the loop, what one hook is made of, and what the one that says "
                               "no looks like, with a live example."},
                "content_from": "en/resources/claude-code-hooks.html",
                "content_lang": "en",
            },
            {
                "title": {"lt": "Savos komandos ir skills",
                          "en": "Your own commands and skills"},
                "desc": {"lt": "Jei tą patį promptą rašai trečią kartą, tai jau ne "
                               "promptas, o komanda. Kaip pasikartojantį darbą paversti "
                               "vienu trumpiniu, kurį vienodai supranta ir agentas, ir "
                               "tavo komanda.",
                         "en": "If you are typing the same prompt a third time, it is not "
                               "a prompt any more, it is a command. How to turn repeated "
                               "work into one shortcut that the agent and your teammates "
                               "read the same way."},
                "href": None,
            },
            {
                "title": {"lt": "MCP: kaip prijungti savo įrankius",
                          "en": "MCP: wiring in your own tools"},
                "desc": {"lt": "Pagal nutylėjimą agentas mato tik failus. MCP yra "
                               "būdas duoti jam tavo duomenų bazę, API ar vidinę sistemą, "
                               "ir tiksliai tiek, kiek leidi, ne daugiau.",
                         "en": "By default the agent only sees files. MCP is how you hand "
                               "it your database, your API or an internal system, and "
                               "exactly as far as you allow, no further."},
                "href": None,
            },
        ],
    },
    {
        "id": "start-coding",
        "tool": {"lt": "Bet koks AI įrankis", "en": "Any AI tool"},
        "tag": {"lt": "Programavimas su AI • Pradedantiesiems",
                "en": "Coding with AI • Beginners"},
        "title": {"lt": "Kaip išmokti programuoti AI eroje",
                  "en": "How to learn to code in the AI era"},
        # The card title is written to catch a person, the <title> to catch
        # the search. Deliberately not the same sentence.
        "seo_title": {"lt": "Kaip pradėti programuoti su AI 2026 – gidas pradedantiesiems",
                      "en": "How to start coding with AI in 2026 – a beginner's guide"},
        "blurb": {
            "lt": "AI gali parašyti kodą už tave. Šis gidas parodys, ką vis "
                  "tiek turi išmokti pats, kaip naudoti AI kaip mokytoją ir "
                  "kaip tapti savarankišku programuotoju.",
            "en": "AI can write the code for you. This guide shows what you "
                  "still have to learn yourself, how to use AI as a teacher, "
                  "and how to become a developer who can work on their own.",
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
    return sum(1 for s in tr["steps"] if s.get("content_from"))


# --------------------------------------------------------------------------
# The shelf: one card per course, on <lang>/resources.html
# --------------------------------------------------------------------------

def shelf(lang):
    u = UI[lang]
    out = [f'      <p class="resources-intro u-reveal">{u["intro"]}</p>', "",
           '      <div class="course-grid u-stagger">']
    for n, tr in enumerate(TRACKS, 1):
        tool = pick(tr.get("tag", tr["tool"]), lang)
        tool_cls = " tool--claude" if tr["id"] == "claude-code" else ""
        href = f'/{lang}/resources/{tr["id"]}.html'
        out += [
            f'        <a class="course-card u-reveal" href="{href}">',
            f'          <span class="course-card__num" aria-hidden="true">{n:02d}</span>',
            f'          <h2 class="course-card__title">{e(pick(tr["title"], lang))}</h2>',
            f'          <p class="course-card__blurb">{e(pick(tr["blurb"], lang))}</p>',
            f'          <span class="resource-card__tool{tool_cls}">{e(tool)}</span>',
            f'          <div class="course-card__foot">',
            f'            <span class="course-card__cta">{u["open"]} →</span>',
            f'          </div>',
            f'        </a>',
        ]
    out += ['      </div>']
    return "\n".join(out)


# --------------------------------------------------------------------------
# A course page: curriculum on the left, the selected step on the right
# --------------------------------------------------------------------------

def inline_resource(path):
    """
    Lift the body of an existing resource page into a lesson panel.

    The resource pages are real, standalone, indexable pages and stay that
    way - this reads the finished article out of one rather than keeping a
    second copy of it here. Asset paths are re-rooted because the article
    was written two directories deep, and the page's own hero is dropped:
    the panel already carries the title.
    """
    import re as _re
    src = (ROOT / path).read_text()
    i = src.index("<main")
    body = src[src.index(">", i) + 1:src.index("</main>")]
    body = body.replace('="../../', '="/')
    # The article's closing sections are page furniture ("Who made this",
    # "What's next") that make no sense inside one step of a course.
    body = _re.sub(r'<section class="resource-section[^"]*"[^>]*>\s*<h2>'
                   r'(?:Who made this|What\'s next)</h2>.*?</section>', "",
                   body, flags=_re.S)
    return "\n".join("            " + ln.strip()
                      for ln in body.strip().splitlines() if ln.strip())


def course_main(tr, n, lang):
    u = UI[lang]
    steps = tr["steps"]
    total, ready = len(steps), ready_count(steps and tr)
    tool = pick(tr.get("tag", tr["tool"]), lang)
    tool_cls = " tool--claude" if tr["id"] == "claude-code" else ""

    nav = []
    panels = []
    for i, s in enumerate(steps, 1):
        sel = "true" if i == 1 else "false"
        done = " is-ready" if s.get("content_from") else ""
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
        # The resource itself goes in the panel. A link out to it would make
        # the reader leave the curriculum to read one step, then come back -
        # the whole point of the two-pane layout is that they don't have to.
        if s.get("content_from"):
            hl = s.get("content_lang")
            note = ([f'            <p class="lesson-panel__lang">'
                     f'({u["en_note"]})</p>']
                    if hl and hl != lang else [])
            body = [*note, inline_resource(s["content_from"])]
        else:
            body = [
                f'            <p class="lesson-panel__empty">'
                f'<span class="track-step__soon">{u["soon"]}</span></p>',
                f'            <p class="lesson-panel__emptynote">{u["no_res"]}</p>',
            ]
        panels += [
            f'          <article class="lesson-panel" role="tabpanel" id="panel-{i}"'
            f' aria-labelledby="tab-{i}"{"" if i == 1 else " hidden"}>',
            f'            <p class="lesson-panel__kicker">{u["lesson"]} {i} / {total}</p>',
            f'            <h2 class="lesson-panel__title">{e(pick(s["title"], lang))}</h2>',
            f'            <p class="lesson-panel__desc">{pick(s["desc"], lang)}</p>',
            *body,
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
    #
    # Every ../ inside an attribute, not just the one after the opening
    # quote: a srcset holds several URLs, and rewriting only the first left
    # the wide-viewport candidate pointing at /lt/img/... - which 404s, so
    # the image broke on exactly the screens it was meant for.
    s = re.sub(r'(src|srcset|href)="([^"]*)"',
               lambda m: '%s="%s"' % (m.group(1), m.group(2).replace('../', '/')),
               s)
    s = re.sub(r'href="(?!https?:|/|#|mailto:)([\w-]+\.html)"',
               rf'href="/{lang}/\1"', s)

    seo = pick(tr.get("seo_title", tr["title"]), lang)
    s = re.sub(r'<title>.*?</title>',
               f'<title>{e(seo)} | {u["title"]} — Gabrielė</title>', s,
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
    if any(st.get("content_from") for st in tr["steps"]):
        s = s.replace('<script src="/js/script.js" defer></script>',
                      '<script src="/js/script.js" defer></script>\n'
                      '    <script src="/js/resource-page.js" defer></script>')
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
