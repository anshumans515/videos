# SAVER vs SPENDER — Reels cover

Archetype 4 (PLAYBOOK.md §4). Renders to a single PNG, not an MP4.

```bash
python3 assemble.py
npx hyperframes lint public
npx hyperframes snapshot public --at 0
# -> public/snapshots/frame-00-at-0s.png
```

## Why two full-body panels instead of a split-screen still

Instagram crops a cover three ways, and the same PNG has to survive all of
them:

| Surface | Crop | Visible band of the 1920 px canvas |
|---|---|---|
| Reels player | full frame | 0 – 1920 |
| Feed | centred 4:5 | ~285 – 1635 |
| Profile grid | centred 1:1 | ~420 – 1500 |

A stacked split-screen still loses its entire top half to the grid crop and
reads as one arbitrary frame. Two side-by-side panels both sit inside the
1:1 band, so the comparison — the whole point of the reel — survives every
crop. The hook sits at y≈246 so it clears the 4:5 top edge.

## Source frames

Both portraits are pulled from scene 1 of the source, where the two are shot
in the same doorway holding the same coffee cup — a matched pair rather than
two unrelated frames, which is what makes the side-by-side read as a
comparison instead of a collage:

- `img/anshuman.jpg` — source t=4.70 s, crop 720×1440 at (600, 180)
- `img/vedant.jpg` — source t=6.00 s, crop 720×1440 at (880, 1800)

Note the bottom-half offset on Vedant: before the 20.43 s cut the source has
Anshuman on top and Vedant below, so his crop is offset by a full
half-height (1620 px) plus the framing adjustment.

## Known gap

`public/img/prospur-logo.png` is missing — the artwork was supplied as an
inline chat image rather than a file, so a plain green mark stands in. Drop
the real PNG at that path and re-run `assemble.py` to swap it in. Prefer a
transparent, white/knockout version — the cover is dark. No "Prospur" text
is set beside it, since the logo is itself a wordmark.
