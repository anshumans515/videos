---
name: general-video
description: Build a split-screen B-roll Reel for Prospur from two silent source clips (e.g. spender-vs-saver, before-vs-after) with kinetic text overlay. Use when the user hands you silent B-roll footage, not a person talking to camera.
---

# general-video

Builds Archetype 3 reels (PLAYBOOK.md §4, §8). Read `/PLAYBOOK.md` in full
before starting — this skill assumes its rules (§1–§2, §8, §9).

## Steps

1. **Confirm the archetype.** Silent B-roll, usually contrasting two
   subjects/behaviors (spender vs. saver, before vs. after). If someone is
   speaking to camera, use `talking-head-recut` instead (PLAYBOOK §11).

2. **Identify the two halves** in the source: which segment is the
   "positive"/left side, which is the "negative"/right side. If the source
   has multiple people, isolate **one person per half** — don't try to
   cover the full duration from raw multi-person footage (§8 character
   consistency).

3. **Composite the video** with `templates/03-split-broll/build_clips.sh`
   (implements the ffmpeg recipe in §8 exactly — crop offsets and
   timings are source-specific, tune them). This produces
   `public/input-video.mp4` with the music bed already muxed in.

4. **Set up the project**: copy `templates/03-split-broll/` to a new
   project folder, run `build_clips.sh`, then write `config.json` (labels,
   hook line, optional counter/jar) — see the template README.

5. **Compliance-check**: any counter/jar numeric value must be an
   illustrative motif (a streak, a habit), never a return figure — label
   it `ILLUSTRATIVE ONLY` (§2).

6. Run the standard editing loop (PLAYBOOK §10):
   ```bash
   python3 assemble.py
   npx hyperframes lint public
   npx hyperframes snapshot public --at 2,8,15,22
   PRODUCER_BROWSER_GPU_MODE=hardware \
     npx hyperframes render public --skill=general-video -o output.mp4 --fps 30
   ```

## Checks before calling it done

- [ ] Compliance strip visible for the entire duration (§2)
- [ ] Each half is centered on its subject, not the background (retuned
      crop offsets, §8)
- [ ] Counter/jar values labeled illustrative, not presented as real
      returns (§2)
- [ ] `npx hyperframes lint public` returns 0 errors
