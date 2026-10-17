#!/usr/bin/env python3
"""
Turn article cover pictures into web files.

Drop a PNG or JPG named after the article (the file name in
_content/straipsniai/, e.g. ai-verslui.png) into img/site/straipsniai/ and
run this. For each picture it writes, next to the source:

  <slug>.webp       1672x941, the article header (16:9, cropped to fill)
  <slug>-800.webp   800w, for cards and phones
  <slug>-og.jpg     1200x630, the picture shown when the link is shared

tools/build-site.py picks the picture up by the article's name, so run the
site build afterwards. Needs Pillow (py -3.11 has it here).

Run:  py -3.11 tools/build-article-images.py
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "img" / "site" / "straipsniai"
ARTICLES = ROOT / "_content" / "straipsniai"
SIZE = (1672, 941)

for src in sorted([*DIR.glob("*.png"), *DIR.glob("*.jpg"), *DIR.glob("*.jpeg")]):
    slug = src.stem
    if slug.endswith("-og"):
        continue
    if not (ARTICLES / f"{slug}.html").exists():
        print(f"skip {src.name}: no article named {slug}")
        continue
    im = ImageOps.fit(Image.open(src).convert("RGB"), SIZE, Image.LANCZOS)
    im.save(DIR / f"{slug}.webp", "WEBP", quality=82, method=6)
    im.resize((800, round(SIZE[1] * 800 / SIZE[0])), Image.LANCZOS).save(
        DIR / f"{slug}-800.webp", "WEBP", quality=82, method=6)
    ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(
        DIR / f"{slug}-og.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    print("wrote", slug)
