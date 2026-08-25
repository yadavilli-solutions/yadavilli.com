#!/usr/bin/env python3
"""Generate favicons and the Open Graph card from the Yadavilli Solutions logo kit.

Source of truth: static/img/brand/default-monochrome-white.svg (path outlines, no
font dependency). Everything else in static/img is derived from it.

Run:  python3 scripts/generate-brand-assets.py
Deps: cairosvg, pillow
"""

import io
import re
from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOGOS = ROOT / "static" / "img" / "brand"
OUT = ROOT / "static" / "img"

CYAN = (0x08, 0xC7, 0xD6)
NAVY = (0x02, 0x02, 0x3E)

# The "Y" glyph inside the wordmark, in the SVG's own user units. Generous bounds:
# the render is trimmed to its alpha bbox afterwards, so over-shooting is free.
Y_VIEWBOX = "180 0 130 126"

SVG_NS = 'xmlns="http://www.w3.org/2000/svg"'


def read_logo() -> str:
    return (LOGOS / "default-monochrome-white.svg").read_text()


def wordmark_group(svg: str) -> str:
    """First <g> of the logo: the 'Yadavilli Solutions' wordmark path."""
    return re.search(r"<g\b.*?</g>", svg, re.S).group()


def render(svg: str, width: int, height: int) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=width, output_height=height)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def gradient(width: int, height: int) -> Image.Image:
    """Diagonal cyan -> navy wash, matching the logo lockup background."""
    img = Image.new("RGB", (width, height))
    px = img.load()
    span = (width - 1) + (height - 1)
    for y in range(height):
        for x in range(width):
            t = (x + y) / span
            px[x, y] = tuple(round(CYAN[i] + (NAVY[i] - CYAN[i]) * t) for i in range(3))
    return img.convert("RGBA")


def isolate_first_glyph(img: Image.Image, gap: int = 6) -> Image.Image:
    """Crop to the leftmost inked shape, dropping any neighbouring letter that
    leaked into the viewBox. Columns of the Y always carry ink somewhere (the
    stem runs down the middle), so the first blank column run is the letter gap."""
    alpha = img.getchannel("A").tobytes()
    w, h = img.width, img.height
    cols = [sum(alpha[y * w + x] for y in range(h)) for x in range(w)]
    left = next(x for x, v in enumerate(cols) if v)
    right = img.width
    blank = 0
    for x in range(left, img.width):
        blank = blank + 1 if cols[x] == 0 else 0
        if blank >= gap:
            right = x - gap + 1
            break
    return img.crop((left, 0, right, img.height)).crop(
        img.crop((left, 0, right, img.height)).getbbox()
    )


def mark(y_glyph: Image.Image, size: int, glyph_ratio: float = 0.52) -> Image.Image:
    """Square app icon: the Y centred on the brand gradient."""
    tile = gradient(size, size)
    target_h = max(1, round(size * glyph_ratio))
    target_w = max(1, round(y_glyph.width * target_h / y_glyph.height))
    glyph = y_glyph.resize((target_w, target_h), Image.LANCZOS)
    tile.alpha_composite(glyph, ((size - target_w) // 2, (size - target_h) // 2))
    return tile


def og_card(svg: str) -> Image.Image:
    card = gradient(1200, 630)
    logo_w = 860
    logo_h = max(1, round(logo_w * 193 / 1762.571162294872))
    logo = render(svg, logo_w, logo_h)
    card.alpha_composite(logo, ((1200 - logo_w) // 2, (630 - logo_h) // 2))
    return card


def main() -> None:
    svg = read_logo()
    y_svg = f'<svg {SVG_NS} viewBox="{Y_VIEWBOX}">{wordmark_group(svg)}</svg>'
    y_glyph = isolate_first_glyph(render(y_svg, 1024, 1094))

    for name, size in [
        ("favicon-16x16.png", 16),
        ("favicon-32x32.png", 32),
        ("apple-touch-icon.png", 180),
        ("android-chrome-192x192.png", 192),
        ("android-chrome-512x512.png", 512),
    ]:
        mark(y_glyph, size).save(OUT / name)
        print("wrote", name)

    mark(y_glyph, 256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote favicon.ico")

    og_card(svg).convert("RGB").save(OUT / "og-default.png", optimize=True)
    print("wrote og-default.png")


if __name__ == "__main__":
    main()
