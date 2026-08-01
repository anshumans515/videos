---
name: talking-head-recut
description: Recut a single-person talking-head MP4 into a Prospur Instagram Reel with karaoke captions, kicker/title, lower-third, and the compliance strip. Use when the user hands you a video of one person speaking to camera and wants a Reel made from it.
---

# talking-head-recut

Builds Archetype 1 reels (PLAYBOOK.md §4). Read `/PLAYBOOK.md` in full
before starting — this skill assumes its rules (§1–§3, §5, §6, §9).

## Steps

1. **Confirm the archetype.** One person, speaking to camera, MP4 input.
   If it's silent B-roll or has no footage at all, stop and use the
   matching archetype instead (PLAYBOOK §11).

2. **Repair audio** (PLAYBOOK §7). Check loudness/peak first:
   ```bash
   ffmpeg -nostats -i in.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +(I|Peak):"
   ```
   Run the standard chain (add `adeclip` first if peaks are near 0 dBFS).
   Two-pass loudness lock, then verify I≈-14 LUFS, peak≤-1.5 dBTP.

3. **Build the base clip**: mux repaired audio back with the brightness-lift
   video filter and dense keyframes (`-g 30 -keyint_min 30`) — exact recipe
   in PLAYBOOK §7. Output to `public/input-video.mp4`.

4. **Transcribe** the *repaired* audio (never an unrepaired quiet clip — it
   hallucinates). Save word-level timestamps as `transcript.json`.

5. **Set up the project**: copy `templates/01-talking-head/` to a new
   project folder, drop in `input-video.mp4` + `transcript.json`, write a
   `config.json` (duration, head_position, kicker, title_lines, name,
   role) — see `templates/01-talking-head/README.md`.

6. **Check compliance before generating anything**: no invented figures, no
   named schemes unless the speaker names them, non-directive card
   phrasing (PLAYBOOK §2).

7. Run the standard editing loop (PLAYBOOK §10):
   ```bash
   python3 assemble.py
   npx hyperframes lint public
   npx hyperframes snapshot public --at 2,8,15,22
   PRODUCER_BROWSER_GPU_MODE=hardware \
     npx hyperframes render public --skill=talking-head-recut -o output.mp4 --fps 30
   ```

## Checks before calling it done

- [ ] Compliance strip visible for the *entire* duration, correct verbatim text (§2)
- [ ] Captions offset by `CAP_OFFSET` (~0.34s) so words land on the audio, not early (§6)
- [ ] No card/caption/compliance text sits over the mouth or eyes (§5)
- [ ] Scrim height matches the clip's `head_position` (§5)
- [ ] `npx hyperframes lint public` returns 0 errors
- [ ] Snapshots at a few timestamps look right before the full render
