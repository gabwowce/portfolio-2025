#!/usr/bin/env python3
"""
Wrap each project's visual in a device frame and split the card in two.

Three things happen here, in both locales:

1. The screenshot moves inside a .mock frame - browser chrome, or a
   laptop base - so a product screen reads as a screen rather than as a
   loose image someone dropped on the card.
2. Projects with more than one screenshot get the extra ones as a small
   gallery under the frame, captioned. Shipping only the hero shot threw
   away screens that answer "what is actually in this thing".
3. The card gets .project--split, which puts the visual and the writing
   side by side on wide viewports and alternates which side the visual
   is on.

Run:  python3 tools/build-project-visuals.py

Idempotent: the visual column is rebuilt from VISUALS each time, so
editing the table and re-running is the way to change a card.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# shot: (basename, width, height, alt_lt|alt_en, caption_lt|caption_en)
VISUALS = {
    "keepmi": {
        "frame": "browser",
        "hero": ("img/keepmi/landing-hero", 1400, 840,
                 "keepmi — pradinis puslapis|keepmi — landing page", None),
        "shots": [
            ("img/keepmi/dashboard", 1400, 845,
             "keepmi — organizatoriaus skydelis|keepmi — organiser dashboard",
             "Organizatoriaus skydelis|Organiser dashboard"),
            ("img/keepmi/select-design", 1400, 838,
             "keepmi — kvietimo dizaino parinkimas|keepmi — invitation design picker",
             "Kvietimo dizainas|Invitation design"),
        ],
    },
    "tikmaker": {
        "frame": "laptop",
        "hero": ("img/TikMaker/main", 1400, 812,
                 "TikMaker — scenų timeline, inspektorius ir peržiūra"
                 "|TikMaker — scene timeline, inspector and preview", None),
        "shots": [],
    },
}


def pick(v, lang):
    if v is None:
        return None
    return v.split("|")[0 if lang == "lt" else -1] if "|" in v else v


def img(base, w, h, alt, lang, sizes, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c}\n'
            f'                  src="../{base}-1400.webp"\n'
            f'                  srcset="../{base}-700.webp 700w, ../{base}-1400.webp 1400w"\n'
            f'                  sizes="{sizes}"\n'
            f'                  alt="{pick(alt, lang)}"\n'
            f'                  width="{w}"\n'
            f'                  height="{h}"\n'
            f'                  loading="lazy"\n'
            f'                  decoding="async"\n'
            f'                  fetchpriority="low"\n'
            f'                />')


def visual_html(spec, lang):
    base, w, h, alt, _ = spec["hero"]
    laptop = " mock--laptop" if spec["frame"] == "laptop" else ""
    out = [
        '<div class="proj-visual u-reveal">',
        f'              <div class="mock{laptop}">',
        '                <div class="mock__bar" aria-hidden="true">',
        '                  <span class="mock__dot"></span>',
        '                  <span class="mock__dot"></span>',
        '                  <span class="mock__dot"></span>',
        '                  <span class="mock__addr"></span>',
        '                </div>',
        '                ' + img(base, w, h, alt, lang,
                                 "(max-width: 899px) 100vw, 560px"),
        '              </div>',
    ]
    if spec["shots"]:
        out.append('              <ul class="proj-shots">')
        for base, w, h, alt, cap in spec["shots"]:
            out += [
                '                <li>',
                '                  <figure>',
                '                    ' + img(base, w, h, alt, lang,
                                             "(max-width: 899px) 50vw, 280px"),
                f'                    <figcaption>{pick(cap, lang)}</figcaption>',
                '                  </figure>',
                '                </li>',
            ]
        out.append('              </ul>')
    out.append('            </div>')
    return "\n".join(out)


def main():
    for lang in ("lt", "en"):
        path = ROOT / lang / "portfolio.html"
        s = path.read_text()
        done = 0

        for pid, spec in VISUALS.items():
            i = s.index(f'id="{pid}"')
            start = s.rindex("<article", 0, i)
            end = s.index("</article>", i) + len("</article>")
            card = s[start:end]

            # replace whatever visual the card currently has
            card = re.sub(r'<div class="(?:thumb[^"]*|proj-visual[^"]*)">.*?</div>\n(?:\s*<ul class="proj-shots">.*?</ul>\n)?',
                          visual_html(spec, lang) + "\n", card, count=1, flags=re.S)
            s = s[:start] + card + s[end:]
            done += 1

        # every card with a visual gets the split layout
        s = re.sub(r'(<article\s+class="project )((?!.*project--split)[^"]*?)(")',
                   r'\1\2 project--split\3', s)
        s = s.replace("  project--split", " project--split")

        path.write_text(s)
        print(f"{lang}/portfolio.html: {done} visuals framed")


if __name__ == "__main__":
    main()
