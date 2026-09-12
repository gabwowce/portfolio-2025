#!/usr/bin/env python3
"""
Turn raw project screenshots into web-sized WebP.

The masters the owner drops in img/<project>/ are 3-4k wide PNGs of 0.3-4.7 MB
each. A portfolio card never shows one larger than ~1100 CSS px, so every byte
past that is pure download cost on the one page a prospective client will
actually scroll.

Each source becomes a 1400w and a 700w WebP next to it, and the card uses a
srcset so a phone pulls the small one. Sources stay in git untouched - this
only ever writes new files.

Note: img/ac/* is deliberately NOT listed here. Those screenshots are of a real
client's production loyalty system and contain a cardholder's name, phone
numbers, card numbers and the client's branding. They must not be published.
"""
import os
from PIL import Image

SOURCES = [
    "img/keepmi/landing-hero.png",
    "img/keepmi/dashboard.png",
    "img/keepmi/select-design.png",
    "img/TikMaker/main.png",
]

WIDTHS = [1400, 700]

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for rel in SOURCES:
    src = os.path.join(root, rel)
    im = Image.open(src).convert("RGB")
    stem = os.path.splitext(src)[0]
    for w in WIDTHS:
        h = round(im.height * w / im.width)
        out = f"{stem}-{w}.webp"
        im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=82, method=6)
        print(f"{os.path.relpath(out, root):45s} {w}x{h}  {os.path.getsize(out)//1024} KB")
