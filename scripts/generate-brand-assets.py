#!/usr/bin/env python3
"""Generate the favicon set and the Open Graph card.

Source of truth: static/img/brand/logo-mark.svg (the Y) and the fonts in
static/fonts. Everything under static/img other than the brand folder is derived.

Rasterizing goes through headless Chrome, so there is no cairo dependency.

Run:  uv run --with pillow python scripts/generate-brand-assets.py
Env:  CHROME  path to a Chrome/Chromium binary (defaults to the macOS app)
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "static" / "img" / "brand"
OUT = ROOT / "static" / "img"
FONTS = ROOT / "static" / "fonts"

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

STONE = "#f6f5f2"
INK = "#16181b"
MUTED = "#55585e"
STREAK = "#c9a227"


def mark_path() -> str:
    return re.search(r'<path d="([^"]+)"', (BRAND / "logo-mark.svg").read_text()).group(1)


def icon_svg(rounded: bool = True) -> str:
    """Ink tile with the Y in stone. Reads the same on light and dark tabs."""
    radius = 28 if rounded else 0
    # The mark is 52 x 50; scale 1.3 fills the 128 tile with even margins.
    scale = 1.3
    tx = (128 - 52 * scale) / 2
    ty = (128 - 50 * scale) / 2
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">'
        f'<rect width="128" height="128" rx="{radius}" fill="{INK}"/>'
        f'<path transform="translate({tx:.2f} {ty:.2f}) scale({scale})" d="{mark_path()}" fill="{STONE}"/></svg>'
    )


def shoot(html: str, dest: Path, width: int, height: int, transparent: bool = False) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html)
        cmd = [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={width},{height}",
            f"--screenshot={dest}", f"file://{page}",
        ]
        if transparent:
            cmd.insert(2, "--default-background-color=00000000")
        subprocess.run(cmd, check=True, capture_output=True)


def icon_png(size: int, rounded: bool = True) -> Path:
    dest = OUT / f"icon-{size}.png"
    html = (
        "<style>html,body{margin:0;background:transparent}svg{display:block;"
        f"width:{size}px;height:{size}px}}</style>{icon_svg(rounded)}"
    )
    shoot(html, dest, size, size, transparent=True)
    return dest


def og_card() -> None:
    body = (FONTS / "ibm-plex-sans-latin-600-normal.woff2").as_uri()
    display = (FONTS / "newsreader-latin-500-normal.woff2").as_uri()
    html = f"""<style>
@font-face{{font-family:Plex;src:url({body});font-weight:600}}
@font-face{{font-family:Newsreader;src:url({display});font-weight:500}}
html,body{{margin:0;width:1200px;height:630px;background:{STONE};color:{INK}}}
body{{display:flex;flex-direction:column;justify-content:center;padding:0 112px;box-sizing:border-box;font-family:Plex,system-ui,sans-serif}}
.brand{{display:flex;align-items:center;gap:22px;font-size:34px;font-weight:600;letter-spacing:-0.01em}}
.brand svg{{width:40px;height:40px;display:block}}
h1{{margin:72px 0 0;font-family:Newsreader,Georgia,serif;font-weight:500;font-size:112px;line-height:1.05;letter-spacing:-0.01em}}
.s{{position:relative;display:inline-block}}
.s svg{{position:absolute;left:-0.04em;bottom:-0.1em;width:calc(100% + 0.08em);height:0.24em;color:{STREAK}}}
p{{margin:40px 0 0;font-size:30px;line-height:1.3;color:{MUTED};font-family:Plex,system-ui,sans-serif;font-weight:600}}
</style>
<div class="brand"><svg viewBox="0 0 52 50"><path d="{mark_path()}" fill="{INK}"/></svg>Yadavilli Solutions</div>
<h1>A <span class="s">holding<svg viewBox="0 0 200 12" preserveAspectRatio="none"><path d="M3 9C50 5 110 7 197 3" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg></span> company.</h1>
<p>hello@yadavilli.com</p>"""
    shoot(html, OUT / "og-default.png", 1200, 630)


def main() -> None:
    (OUT / "favicon.svg").write_text(icon_svg())

    sizes = {16: "favicon-16x16.png", 32: "favicon-32x32.png", 180: "apple-touch-icon.png",
             192: "android-chrome-192x192.png", 512: "android-chrome-512x512.png"}
    for size, name in sizes.items():
        tmp = icon_png(size, rounded=size not in (180,))
        tmp.replace(OUT / name)

    Image.open(OUT / "favicon-32x32.png").save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32)])
    og_card()
    print("favicon set and og-default.png written")


if __name__ == "__main__":
    main()
