# Archetype 4 · still Reels cover

A clean frame of the presenter + a hook headline, rendered as a **single
PNG snapshot**, not an MP4. Skill: `/motion-graphics`. See PLAYBOOK.md §4.

## Input

- `photo.jpg` *(optional — falls back to a dark placeholder panel)* — a
  clean still frame of the presenter. Pull this from the source clip with
  `ffmpeg -ss <t> -i in.mp4 -frames:v 1 photo.jpg`, or use a dedicated
  photo.
- `config.json` *(optional)*:
  ```json
  {
    "photo": "photo.jpg",
    "hook_lines": ["Why one fund", "isn't a plan"],
    "name": "Vedant",
    "role": "Prospur"
  }
  ```

## Instagram crop safety

Instagram crops a cover three different ways, and the same PNG has to read
in all three:

| Surface | Crop | Approx. visible band (of the 1920px canvas) |
|---|---|---|
| Reels player | full frame | 0–1920 |
| Feed | centered 4:5 | ~285–1635 |
| Profile grid | centered 1:1 | ~420–1500 |

Keep the hook headline in the **upper band** (`assemble.py` anchors it at
`top: 250px`) — it survives the 4:5 feed crop. Nothing below y=1500 is
guaranteed visible in the grid, so the wordmark/name-tag placement near the
bottom is decorative, not load-bearing.

## What the assembler builds

- Full-bleed photo with a top/bottom gradient scrim
- A ghost background element (oversized low-opacity ring) purely for
  texture — never load-bearing text
- Hook headline in the upper safe band
- Name tag (bottom-left) + a small ARN credit line
- Prospur wordmark (top-right, white-on-dark)

This composition is intentionally static — one paused GSAP timeline is
still registered per PLAYBOOK §9.10, but there's no motion to snapshot.

## Render

```bash
python3 assemble.py
npx hyperframes lint public
npx hyperframes snapshot public --at 0 -o cover.png
```
