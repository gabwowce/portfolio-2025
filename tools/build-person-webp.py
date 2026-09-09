#!/usr/bin/env python3
"""
Build the web-ready character images from the master PNGs in img/person/.

The masters are 1086x1448 RGBA exports (~1 MB each) with a lot of empty
alpha around the figure. Shipping those directly would cost ~13 MB on a
site whose whole point is that it stays fast, so this script:

  1. crops each master to its alpha bounding box, so the character fills
     the frame instead of floating in transparent padding;
  2. writes two WebP widths per pose - 900px for heroes, 450px for the
     smaller placements - both with the alpha channel kept;
  3. cuts one square headshot (avatar-profile) for the round author
     images in footers and bylines.

Run it after replacing or adding a master PNG:  python3 tools/build-person-webp.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "img" / "person"
WIDTHS = {"": 900, "-450": 450}
QUALITY = 82

# The round profile image has its own square master.
PROFILE_SRC = "profile"
PROFILE_SIZE = 320

def crop_to_alpha(im):
    return im.crop(im.getbbox())


def save_webp(im, path, width):
    h = round(im.height * width / im.width)
    out = im.resize((width, h), Image.LANCZOS)
    out.save(path, "WEBP", quality=QUALITY, method=6)
    return out.size


def main():
    for src in sorted(SRC.glob("*.png")):
        if src.stem == PROFILE_SRC:
            continue  # handled below, as a square portrait
        im = crop_to_alpha(Image.open(src).convert("RGBA"))
        for suffix, width in WIDTHS.items():
            dst = src.with_name(f"{src.stem}{suffix}.webp")
            size = save_webp(im, dst, width)
            print(f"{dst.relative_to(ROOT)}  {size[0]}x{size[1]}  {dst.stat().st_size // 1024} KB")

    # The round profile image: its own square master, so it only needs
    # resizing - no guessing at where the face sits in a full-body pose.
    im = Image.open(SRC / f"{PROFILE_SRC}.png").convert("RGBA")
    dst = SRC / "avatar-profile.webp"
    im.resize((PROFILE_SIZE, PROFILE_SIZE), Image.LANCZOS).save(
        dst, "WEBP", quality=88, method=6
    )
    print(f"{dst.relative_to(ROOT)}  {PROFILE_SIZE}x{PROFILE_SIZE}  {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
