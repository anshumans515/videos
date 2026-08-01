---
name: motion-graphics
description: Build a still Reels cover/thumbnail for Prospur from a presenter photo and a hook headline, rendered as a single PNG snapshot. Use when the user asks for a cover, thumbnail, or "make a cover for that reel".
---

# motion-graphics

Builds Archetype 4 covers (PLAYBOOK.md §4). Read `/PLAYBOOK.md` in full
before starting — this skill assumes its rules (§1, §4, §9).

## Steps

1. **Confirm the archetype.** A cover/thumbnail request, not a full reel.
   If there's already a rendered reel this cover is for, pull a clean still
   frame from it: `ffmpeg -ss <t> -i output.mp4 -frames:v 1 photo.jpg`.

2. **Set up the project**: copy `templates/04-cover/` to a new project
   folder, drop in `photo.jpg`, write `config.json` (hook_lines, name,
   role) — see the template README.

3. **Respect the crop safety rule**: the hook headline must stay in the
   upper band of the canvas (`assemble.py` already anchors it there) so it
   survives Instagram's centered 4:5 feed crop and 1:1 grid crop — don't
   move it lower without checking both crops.

4. Render as a **snapshot, not a video**:
   ```bash
   python3 assemble.py
   npx hyperframes lint public
   npx hyperframes snapshot public --at 0 -o cover.png
   ```

## Checks before calling it done

- [ ] Hook headline reads fully inside the ~y=285-1635 feed-crop band and
      the ~y=420-1500 grid-crop band
- [ ] Nothing load-bearing sits only below y=1500
- [ ] `npx hyperframes lint public` returns 0 errors
- [ ] Output is a single PNG, not an MP4
