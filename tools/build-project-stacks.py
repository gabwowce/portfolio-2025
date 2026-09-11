#!/usr/bin/env python3
"""
Write the architecture strip into each project card, in both locales.

The strip is plain HTML in the page rather than something rendered at
runtime, because the words in it - FastAPI, React Native, ElevenLabs -
are exactly what someone searches for, and a JS-rendered strip is
invisible to that. So it is generated here and written into the files.

Edit STACKS below and run:  python3 tools/build-project-stacks.py

A project with no entry, or an entry with no nodes, gets no strip at
all. That is deliberate: an empty or guessed architecture is worse
than none, because the first client who asks about it will find out.

Each node is (label, sublabel, kind) where kind is "" for an ordinary
piece and "ai" for anything model-shaped, which gets the accent.
Facts are (value, label) pairs - the numbers that show the thing is
not a demo.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

LABEL = {"lt": "Sistemos sandara", "en": "How it's built"}
AI_BADGE = {"lt": "AI viduje", "en": "AI inside"}

STACKS = {
    # Verified from the project's own title on the page.
    "autorent": {
        "nodes": [
            ("React", "klientas|client", ""),
            ("FastAPI", "Python API|Python API", ""),
            ("PostgreSQL", "duomenys|data", ""),
        ],
        "facts": [],
    },
    "kibinai": {
        "nodes": [
            ("React", "headless klientas|headless client", ""),
            ("WordPress", "turinio API|content API", ""),
        ],
        "facts": [],
    },
    # --- Fill these in, then re-run. Left empty on purpose. ---
    # "keepmi":      {"nodes": [], "facts": []},
    # "kidcan":      {"nodes": [], "facts": []},
    # "tikmaker":    {"nodes": [("ElevenLabs", "tekstas -> balsas|text -> speech", "ai")],
    #                 "facts": []},
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pick(text, lang):
    """Fields carry 'lt|en'; a field without a bar is used for both."""
    return text.split("|")[0 if lang == "lt" else -1] if "|" in text else text


def strip_html(pid, spec, lang, indent):
    nodes = spec.get("nodes") or []
    if not nodes:
        return None
    i = indent
    out = [f'{i}<div class="stack">',
           f'{i}  <span class="stack__label">{LABEL[lang]}</span>',
           f'{i}  <ul class="stack-flow">']
    for label, sub, kind in nodes:
        cls = "stack-node stack-node--ai" if kind == "ai" else "stack-node"
        sub_html = f'<small>{esc(pick(sub, lang))}</small>' if sub else ""
        out.append(f'{i}    <li class="{cls}">{esc(label)}{sub_html}</li>')
    out.append(f'{i}  </ul>')
    facts = spec.get("facts") or []
    if facts:
        out.append(f'{i}  <ul class="stack-facts">')
        for value, label in facts:
            out.append(f'{i}    <li><strong>{esc(pick(value, lang))}</strong>'
                       f'{esc(pick(label, lang))}</li>')
        out.append(f'{i}  </ul>')
    out.append(f'{i}</div>')
    return "\n".join(out) + "\n"


def has_ai(spec):
    return any(k == "ai" for _, _, k in spec.get("nodes") or [])


def main():
    for lang in ("lt", "en"):
        path = ROOT / lang / "portfolio.html"
        s = path.read_text()
        # remove previously generated strips before writing new ones
        s = re.sub(r'[ \t]*<div class="stack">.*?</div>\n', "", s, flags=re.S)
        written = 0
        for pid, spec in STACKS.items():
            m = re.search(rf'id="{pid}"', s)
            if not m:
                continue
            # place it after the project's description paragraph
            d = re.search(r'([ \t]*)<p class="desc[^"]*"[^>]*>.*?</p>\n', s[m.end():], re.S)
            if not d:
                print(f"  no description found for {pid} in {lang}")
                continue
            block = strip_html(pid, spec, lang, d.group(1))
            if not block:
                continue
            at = m.end() + d.end()
            s = s[:at] + block + s[at:]
            written += 1
        path.write_text(s)
        print(f"{lang}/portfolio.html: {written} strips written")


if __name__ == "__main__":
    main()
