#!/usr/bin/env python3
"""
Derive the usable logo variants from the supplied master artwork.

  python3 assets/make-logo-variants.py

Input : assets/prospur-logo.svg          — the supplied artwork, as-is
Output: assets/prospur-logo-light.svg    — for dark backgrounds

WHY A LIGHT VARIANT
The master sets PROSPUR in near-black (#020202-#050505) with the R in a
green-to-lime gradient. Every Prospur reel surface is dark — the brand band,
the seam plate, the cover — so the ink has to be knocked out to white.

This CANNOT be done with a CSS filter. `brightness(0) invert(1)` turns the
whole mark white, taking the green R with it; `invert(1)` alone would push
the greens to magenta. The only correct treatment is recolouring the dark
fills and leaving every green fill untouched, which is what this does.

WHY THE VIEWBOX CHANGES
The master is a 1024x1024 canvas with the wordmark occupying a band roughly
x=158-873, y=453-566 — about 8% of the area. Rendered at any sane width the
mark would be a sliver in a mostly empty box. The output crops the viewBox to
the artwork with a little padding, so `width: 300px` means 300px of wordmark.

The mask that punches the letter counters is preserved untouched — that is
what makes the interiors truly transparent rather than filled with the
background colour, and it is the whole point of the supplied file.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "prospur-logo.svg")
OUT_LIGHT = os.path.join(HERE, "prospur-logo-light.svg")

# The dark ink of the wordmark. Every other fill in the file is a green or
# lime accent and must survive untouched.
INK = {"#030303", "#020202", "#050505", "#040404"}

# Artwork bounds within the 1024x1024 master, plus a little breathing room.
VIEWBOX = "152 448 728 126"


def main():
    with open(SRC) as f:
        svg = f.read()

    # Recolour only the ink fills. Case-insensitive, and only inside fill="".
    def swap(m):
        return f'fill="#FFFFFF"' if m.group(1).upper() in INK else m.group(0)

    light = re.sub(r'fill="(#[0-9A-Fa-f]{6})"', lambda m: swap(m), svg)

    swapped = len(re.findall(r'fill="#FFFFFF"', light)) - len(re.findall(r'fill="#FFFFFF"', svg))
    if swapped < 6:
        raise SystemExit(f"expected to recolour the 7 wordmark glyphs, only did {swapped}")

    # The mask's backing rect is width="100%" height="100%", which resolves
    # against the VIEWPORT starting at user-space 0,0 — so once the viewBox is
    # cropped to x=152,y=448 the rect no longer covers the glyphs, the mask
    # reads black there, and the entire wordmark is masked away to nothing.
    # Pin it to the master's own 1024 canvas instead of a percentage.
    light = light.replace(
        '<rect width="100%" height="100%" fill="white"/>',
        '<rect x="0" y="0" width="1024" height="1024" fill="white"/>',
        1,
    )
    if 'width="100%"' in light:
        raise SystemExit("mask backing rect not pinned — master mask changed?")

    # Drop the fixed pixel size and crop to the artwork so CSS width controls
    # the rendered size directly.
    light = light.replace('width="1024" height="1024"', f'viewBox="{VIEWBOX}"', 1)
    if "viewBox" not in light:
        raise SystemExit("viewBox substitution failed — master header changed?")

    with open(OUT_LIGHT, "w") as f:
        f.write(light)
    print(f"wrote {OUT_LIGHT}  ({swapped} glyph fills knocked out to white, viewBox={VIEWBOX})")


if __name__ == "__main__":
    main()
