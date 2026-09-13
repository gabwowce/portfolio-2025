#!/usr/bin/env python3
"""
Redact the client-system screenshots so they can be published.

The masters in img/ac/ are of a real production loyalty backoffice. They
show a cardholder's full name, two phone numbers, card numbers, account
balances, the client's own branding and tenant name, and their live
promotion and product catalogue. None of that can go on a public site.

What survives redaction is the part that is actually worth showing: the
shape of the system. Two-pane master/detail, a dense virtualised list, a
tabbed record, a right-hand rail of related entities. A prospective client
looking at this learns "she has built a real backoffice", which is the
claim, and learns nothing about whose it is.

Method: every text-bearing region is downsampled to a fraction of its size
and scaled back up. That destroys the information rather than smearing it
- a Gaussian blur alone can be partially inverted, a resample cannot,
because the pixels simply no longer exist. Structural chrome (nav rail,
tab bar, panel edges) is left crisp so the layout still reads.

Regions are normalised (x0, y0, x1, y1) fractions so they survive the
masters being re-exported at a different size.

Run:  python3 tools/redact-client-shots.py

The masters stay gitignored. Only the redacted output is committed.
"""
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

# How hard to destroy a region: the shrink factor before scaling back.
# 22 means a 220px-wide block of text becomes 10px wide, then back to 220.
HARD = 26   # names, phone numbers, branding, tenant - unrecoverable
DATA = 16   # list rows, balances, catalogue text

SHOTS = {
    "img/ac/cards.png": {
        "out": "img/ac-cards-redacted",
        "regions": [
            # (x0, y0, x1, y1, strength)
            (0.000, 0.000, 0.095, 0.040, HARD),   # product wordmark
            (0.870, 0.000, 1.000, 0.050, HARD),   # operator name + tenant
            (0.100, 0.245, 0.375, 1.000, DATA),   # card list: numbers, codes
            (0.370, 0.095, 0.720, 0.185, HARD),   # record header: card no, owner
            (0.375, 0.225, 0.825, 0.580, DATA),   # accounts, balances, limits
            (0.820, 0.215, 1.000, 0.375, HARD),   # cardholder name + 2 phones
            (0.820, 0.375, 1.000, 0.580, DATA),   # validity, segments
            (0.820, 0.595, 1.000, 0.880, DATA),   # promotions (client brands)
        ],
    },
    "img/ac/loyalty-promotions.png": {
        "out": "img/ac-loyalty-redacted",
        "regions": [
            (0.000, 0.000, 0.095, 0.040, HARD),   # product wordmark
            (0.870, 0.000, 1.000, 0.050, HARD),   # operator name + tenant
            (0.100, 0.085, 0.375, 1.000, DATA),   # promotion list (client brands)
            (0.380, 0.095, 0.915, 0.160, HARD),   # promotion title + status
            (0.380, 0.160, 0.700, 0.210, DATA),   # tab strip values
            (0.380, 0.215, 0.725, 0.465, DATA),   # basket: real product catalogue
            (0.380, 0.635, 0.725, 0.720, DATA),   # card category value
            (0.720, 0.225, 1.000, 0.650, HARD),   # receipt: products + tenant name
        ],
    },
}

WIDTHS = [1400, 700]


def destroy(im, box, factor):
    """Resample a region down and back up, so the text is gone for good."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if w < 2 or h < 2:
        return
    region = im.crop(box)
    small = region.resize((max(1, w // factor), max(1, h // factor)),
                          Image.BILINEAR)
    im.paste(small.resize((w, h), Image.NEAREST).filter(
        ImageFilter.GaussianBlur(max(1, w // 300))), box)


def main():
    for src, spec in SHOTS.items():
        path = ROOT / src
        if not path.exists():
            print(f"  skip (master not present): {src}")
            continue
        im = Image.open(path).convert("RGB")
        W, H = im.size
        for x0, y0, x1, y1, factor in spec["regions"]:
            destroy(im, (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)),
                    factor)
        for w in WIDTHS:
            h = round(im.height * w / im.width)
            out = ROOT / f"{spec['out']}-{w}.webp"
            im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=80,
                                                  method=6)
            print(f"{out.relative_to(ROOT)}  {w}x{h}  "
                  f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
