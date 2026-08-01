# SAVER vs SPENDER — Reels cover

Archetype 4 (PLAYBOOK.md §4). Renders to a single PNG, not an MP4.

```bash
python3 assemble.py
npx hyperframes lint public
npx hyperframes snapshot public --at 0
# -> public/snapshots/frame-00-at-0s.png
```

## Why two circles instead of a split-screen still

Instagram crops a cover three ways, and the same PNG has to survive all of
them:

| Surface | Crop | Visible band of the 1920 px canvas |
|---|---|---|
| Reels player | full frame | 0 – 1920 |
| Feed | centred 4:5 | ~285 – 1635 |
| Profile grid | centred 1:1 | ~420 – 1500 |

A stacked split-screen still loses its entire top half to the grid crop and
reads as one arbitrary frame. Two circular portraits both sit inside the
1:1 band, so the comparison — the whole point of the reel — survives every
crop. The hook sits at y≈296 so it clears the 4:5 top edge.

## Source frames

Both portraits are pulled from scene 1 of the source, where the two are shot
in the same spot with the same coffee cup — a matched pair rather than two
unrelated frames:

- `img/anshuman.jpg` — source t=4.65 s, crop 700×700 at (881, 61)
- `img/vedant.jpg` — source t=5.90 s, crop 700×700 at (856, 1924)

Note the bottom-half offset: before the 20.43 s cut the source has Anshuman
on top and Vedant below, so Vedant's crop is offset by a full half-height.

## Known gap

`public/img/prospur-logo.png` is missing — the real wordmark could not be
fetched in this environment, so a typographic lockup is used. Drop the real
PNG at that path and re-run `assemble.py` to swap it in.
