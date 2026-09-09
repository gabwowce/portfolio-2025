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

# Head crop for the round profile image, as fractions of the alpha bbox.
PROFILE_POSE = "standing-still"
PROFILE_BOX = (0.395, 0.005, 0.700, 0.215)  # left, top, right, bottom


def crop_to_alpha(im):
    return im.crop(im.getbbox())


def save_webp(im, path, width):
    h = round(im.height * width / im.width)
    out = im.resize((width, h), Image.LANCZOS)
    out.save(path, "WEBP", quality=QUALITY, method=6)
    return out.size


def main():
    for src in sorted(SRC.glob("*.png")):
        im = crop_to_alpha(Image.open(src).convert("RGBA"))
        for suffix, width in WIDTHS.items():
            dst = src.with_name(f"{src.stem}{suffix}.webp")
            size = save_webp(im, dst, width)
            print(f"{dst.relative_to(ROOT)}  {size[0]}x{size[1]}  {dst.stat().st_size // 1024} KB")

    # Square headshot, from the same master so the face matches every pose.
    im = crop_to_alpha(Image.open(SRC / f"{PROFILE_POSE}.png").convert("RGBA"))
    l, t, r, b = PROFILE_BOX
    head = im.crop((int(l * im.width), int(t * im.height),
                    int(r * im.width), int(b * im.height)))
    side = max(head.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(head, ((side - head.width) // 2, (side - head.height) // 2), head)
    dst = SRC / "avatar-profile.webp"
    square.resize((320, 320), Image.LANCZOS).save(dst, "WEBP", quality=88, method=6)
    print(f"{dst.relative_to(ROOT)}  320x320  {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
